# 🌐 REGLAS DEL BROWSER (RDB) - COLMENA v1.0
## Sistema de Automatización Browser + API para Duendes
**Versión:** 1.0
**Fecha:** 1 Marzo 2026
**Autor:** Arquitecto + Claude Opus (claude.ai)
**Estado:** VALIDADO con prueba real (Debate Engine 3 duendes, búsqueda vuelos, stealth scraping)

---

## 📊 HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 1 Mar 2026 | Documento inicial. Browser Engine, Claude in Chrome, Colmena Debate Engine |

---

## 🎯 PRINCIPIO CORE

**El duende que tiene browser tiene manos.**

Sin browser, un duende solo puede pensar y hablar. Con browser puede:
- Navegar sitios, llenar formularios, hacer scraping
- Controlar Chrome del usuario (Claude in Chrome)
- Llamar APIs directamente (Anthropic, GitHub, Vercel)
- Poner a OTROS duendes a trabajar vía API

---

## 📋 ARQUITECTURA: 3 CAPAS DE BROWSER

### CAPA 1: Browser Engine (Puppeteer + Stealth)
**Qué es:** Servidor Node.js local que controla Chrome headless.
**Dónde corre:** PC Windows del Arquitecto (localhost:3847)
**Para qué sirve:** Scraping masivo, navegación sin sesión, datos públicos.

**Setup:**
```
Ubicación: C:\Users\pvrol\browser-duendes\
Server: server.js (puerto 3847)
Dependencias: puppeteer-extra, puppeteer-extra-plugin-stealth
Chrome: C:\Program Files\Google\Chrome\Application\chrome.exe
```

**Iniciar:**
```bash
cd C:\Users\pvrol\browser-duendes
node server.js
# Responde en http://localhost:3847
```

**Capacidades:**
- ✅ Scraping sitios públicos (Google Flights, Volaris, noticias)
- ✅ Bypass Cloudflare (stealth plugin instalado)
- ✅ Screenshots automatizados
- ✅ Ejecución de scripts .js personalizados
- ❌ NO puede pasar login walls (no tiene sesión)
- ❌ NO puede resolver CAPTCHAs
- ❌ NO puede interactuar con sitios que requieren autenticación

**Stealth Plugin (IMPORTANTE):**
El server.js usa puppeteer-extra con StealthPlugin para evadir detección de bots:
```javascript
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
```
Sin esto, Cloudflare y otros WAFs bloquean el browser.

---

### CAPA 2: Claude in Chrome (Extensión)
**Qué es:** Extensión oficial de Anthropic que da control del Chrome REAL del usuario.
**Dónde corre:** Chrome del Arquitecto (cualquier PC)
**Para qué sirve:** Tareas interactivas que requieren sesión del usuario.

**Setup:**
```
Extensión: "Claude" por Anthropic
Chrome Web Store: buscar "Claude" por claude.com
Versión probada: 1.0.56
Requiere: Plan Pro/Max/Team/Enterprise de Claude
```

**Capacidades:**
- ✅ Navegar con sesiones activas del usuario (Airbnb, SAT, INM, bancos)
- ✅ Llenar formularios complejos
- ✅ Leer contenido de páginas autenticadas
- ✅ Tomar screenshots
- ✅ Hacer click, scroll, typing
- ✅ El usuario resuelve CAPTCHAs, el duende continúa
- ❌ NO puede ingresar passwords (el usuario debe teclearlos)
- ❌ NO puede hacer click en "Submit" sin confirmación explícita
- ❌ NO puede manejar e.firma/FIEL

**Herramientas disponibles (MCP tools):**
```
tabs_context_mcp  → Ver pestañas abiertas
tabs_create_mcp   → Crear pestaña nueva
navigate          → Ir a URL
computer          → Click, scroll, screenshot, type
read_page         → Leer DOM/accessibility tree
find              → Buscar elementos por texto
form_input        → Llenar campos de formulario
get_page_text     → Extraer texto de página
javascript_tool   → Ejecutar JS en la página
```

---

### CAPA 3: API Directa (Sin Browser)
**Qué es:** Llamadas HTTP directas a APIs desde el container de Claude o desde scripts Node.
**Dónde corre:** Anywhere — container Claude, PC local, RPi
**Para qué sirve:** Lo más rápido. Sin UI, sin navegación, pura data.

**APIs disponibles confirmadas:**
```
Anthropic API    → Orquestar otros duendes (DEBATE ENGINE)
GitHub API       → Push código, leer repos, crear repos
Vercel API       → Deploy, env vars, proyectos
Google Flights   → Vía scraping con Browser Engine
```

---

## 🐝 COLMENA DEBATE ENGINE

### QUÉ ES
Sistema que pone a N duendes (instancias de Claude vía API) a debatir un tema, criticarse mutuamente, y generar un plan de acción consolidado. Sin browser. Sin UI. Pura velocidad.

### CÓMO FUNCIONA
```
1. El orquestador define TEMA + DUENDES (nombre + system prompt)
2. Ronda 0: Todos los duendes generan propuesta inicial (PARALELO)
3. Ronda 1-N: Cada duende lee las propuestas de los otros y critica (PARALELO)
4. Síntesis: Un duende "Orquestador" consolida en plan de acción
5. Output: JSON con todo el debate + plan final
```

### VELOCIDAD MEDIDA
```
Haiku 3:        27.5 segundos (3 duendes, 3 rondas, 13 calls)
Sonnet 4.5:     86.6 segundos (3 duendes, 2 rondas, 10 calls)
```
Haiku es 3x más rápido pero las críticas son superficiales.
Sonnet es más lento pero genera desacuerdos reales con datos.

### CONFIGURACIÓN API

**API Key:** Almacenada en `.env` o en `/home/pvrolo/colmena/keys/TOKENS.md`
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

**Modelos disponibles (confirmado 1 Mar 2026):**
```
claude-sonnet-4-5-20250929  → RECOMENDADO para debates (calidad/costo)
claude-opus-4-20250514      → Máxima calidad, más caro
claude-sonnet-4-20250514    → Alternativa Sonnet
claude-haiku-4-5-20251001   → Rápido y barato
claude-3-haiku-20240307     → Legacy, funciona, más barato
```

**IMPORTANTE:** Los model strings viejos (`claude-3-5-sonnet-20241022`, etc.) dan `not_found_error`. Usar los strings de arriba.

**Headers requeridos:**
```javascript
headers: {
  'Content-Type': 'application/json',
  'x-api-key': API_KEY,
  'anthropic-version': '2023-06-01'
}
```

### SCRIPT DE REFERENCIA

**Ubicación:** `C:\Users\pvrol\browser-duendes\colmena-debate.js`

**Estructura mínima de un duende:**
```javascript
const DUENDE = {
  nombre: 'Duende Analista',
  system: 'Eres el Duende Analista de Castle Solutions...'
};
```

**Llamada API mínima:**
```javascript
async function askDuende(duende, messages) {
  const resp = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': API_KEY,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 800,
      system: duende.system,
      messages: messages
    })
  });
  const data = await resp.json();
  return data.content.map(c => c.text || '').join('');
}
```

**Paralelismo (CLAVE):**
```javascript
// Todos los duendes responden al mismo tiempo
const respuestas = await Promise.all(
  DUENDES.map(d => askDuende(d, mensajes))
);
```

### INSTRUCCIONES PARA EL DUENDE ACTIVADOR

El duende que corra el Debate Engine necesita:

**PRE-REQUISITOS:**
1. ✅ Acceso a la API de Anthropic (key en .env o en contexto)
2. ✅ Node.js disponible (container Claude, PC local, o RPi)
3. ✅ El script `colmena-debate.js` o equivalente

**PARA CORRER DESDE CONTAINER CLAUDE (SIN PC):**
```javascript
// El duende escribe el script inline y lo ejecuta con bash_tool
// No necesita Desktop Commander ni Browser Engine
// Solo necesita la API key y fetch()
```

**PARA CORRER DESDE PC LOCAL:**
```bash
cd C:\Users\pvrol\browser-duendes
node colmena-debate.js
# Output en consola + JSON guardado en /debates/
```

**PARA PERSONALIZAR UN DEBATE:**
Editar estas variables en el script:
```javascript
const TEMA = 'Descripción del tema a debatir...';
const RONDAS = 2;  // 2-3 recomendado
const DUENDES = [
  { nombre: 'Rol 1', system: 'Prompt del duende 1...' },
  { nombre: 'Rol 2', system: 'Prompt del duende 2...' },
  // Agregar los que quieras
];
```

**TIPS PARA SYSTEM PROMPTS EFECTIVOS:**
- Incluir "Max N palabras" (150-200 funciona bien)
- Incluir instrucción de crítica: "Cuando critiques, sé específico en..."
- Dar contexto del negocio: "Castle Solutions, 11 propiedades VR PV"
- Cada duende debe tener PERSPECTIVA DISTINTA, no solo "tono" distinto

---

## 🔧 CUÁNDO USAR QUÉ

| Tarea | Herramienta | Razón |
|-------|-------------|-------|
| Scraping masivo (30+ fuentes) | Browser Engine | Sin login, paralelo, headless |
| Buscar vuelos/precios | Browser Engine | Google Flights accesible sin login |
| Llenar formulario SAT/INM | Claude in Chrome | Requiere sesión del usuario |
| Booking en Airbnb/VRBO | Claude in Chrome | Requiere sesión autenticada |
| Debate entre duendes | API Directa | Más rápido, sin browser overhead |
| Deploy a Vercel | API Directa | curl/fetch, no necesita UI |
| Push a GitHub | API Directa | Token + API, más confiable que git CLI |
| Auditar dashboard Airbnb | Claude in Chrome | Datos detrás de login |
| Resolver CAPTCHA | Claude in Chrome + Usuario | Duende pausa, usuario resuelve |
| Monitoreo comp set | Browser Engine | Scraping periódico sin intervención |

---

## ⚠️ LIMITACIONES CONOCIDAS

1. **Claude in Chrome se desconecta** si la conversación está inactiva mucho tiempo. Hay que reconectar desde el ícono en toolbar.

2. **Browser Engine no pasa login walls.** Si un sitio requiere autenticación, usar Claude in Chrome.

3. **API Key de Anthropic tiene tiers.** Verificar modelos disponibles en console.anthropic.com/settings/limits antes de asumir que un modelo funciona.

4. **SSH al RPi desde Desktop Commander** no maneja bien passwords interactivos. Usar ssh2 (npm) con Node.js, o configurar SSH keys.

5. **Stealth plugin no es 100%.** Algunos sitios (Skyscanner) tienen detección secundaria post-Cloudflare. Necesitan delays largos (5-10s).

6. **Los model strings cambian.** Anthropic actualiza nombres de modelos. Si da `not_found_error`, verificar strings actuales en la consola.

---

## 📊 MÉTRICAS DE LA PRUEBA (1 Mar 2026)

| Métrica | Browser Engine | Claude in Chrome | API Directa |
|---------|---------------|-----------------|-------------|
| Setup time | 0 (ya corriendo) | 2 min (instalar ext) | 0 |
| Búsqueda vuelos | 45s (Google Flights) | N/A | N/A |
| Debate 3 duendes Haiku | N/A | N/A | 27.5s |
| Debate 3 duendes Sonnet | N/A | N/A | 86.6s |
| Lectura chat claude.ai | N/A | 2-3 min (screenshots) | N/A |
| Stealth Cloudflare bypass | ✅ | N/A | N/A |

---

## 🔄 RELACIÓN CON OTRAS RDE

- **Regla #3 (Python siempre, sed nunca):** Aplica también para scripts de browser. Node.js > bash para scraping.
- **Regla #15 (Credenciales en .env):** API keys NUNCA hardcoded en scripts. Usar .env.
- **Regla #20 (Arquitectura híbrida):** El Debate Engine es la evolución cloud de esta regla. Duendes cloud pueden correr debates sin PC local.
- **Regla #25 (Desarrollo en nube):** El Debate Engine corre desde container Claude. No necesita PC local.

---

## 💡 PRÓXIMOS PASOS

1. **Integrar Debate Engine con chat.duendes.app** — Los resultados del debate se posteen automáticamente al canal
2. **Scheduled debates** — Cron job que corre debates sobre temas recurrentes (pricing semanal, comp set)
3. **Duende Activador persistente** — Un duende con acceso a Browser Engine + API que pueda ser triggered desde el Hub
4. **Multi-modal debates** — Duendes que reciban imágenes (screenshots de comp set) además de texto

---

## 📝 NOTA FINAL

El Browser Engine + Claude in Chrome + API Directa son tres herramientas complementarias, no competidoras. El duende inteligente sabe cuál usar según la tarea:

- **¿Necesitas datos públicos masivos?** → Browser Engine
- **¿Necesitas la sesión del usuario?** → Claude in Chrome
- **¿Necesitas velocidad pura?** → API Directa

"El duende que tiene browser tiene manos. El duende que tiene API tiene ejército."

— Arquitecto, Colmena 2026

🐝 Sistema Colmena — Browser Edition
