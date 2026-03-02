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
| 1.1 | 2 Mar 2026 | Sección "El Duende es la API". Debate multi-IA vía browser. Tier web > tier API. |

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


---

## 🧠 PRINCIPIO FUNDAMENTAL: EL DUENDE ES LA API

### El concepto

Cuando un duende tiene Claude in Chrome, **él mismo ES la API de cada IA**. No necesita endpoint, no necesita key, no necesita créditos. El browser reemplaza al SDK.

| Método tradicional | Método browser |
|---|---|
| `fetch('api.openai.com', {headers: {Authorization: 'Bearer sk-...'}})` | `navigate('chat.openai.com')` → `type(prompt)` → `read_page()` |
| Requiere API key | Requiere sesión web activa del Arquitecto |
| Paga por token | Gratis (tier web de cada IA) |
| Modelo recortado (API tier) | Modelo completo (web tier) |

### Por qué el tier web es SUPERIOR al tier API

Las IAs dan sus mejores modelos en la interfaz web, no en la API:

| IA | Web (gratis) | API (pagado) |
|---|---|---|
| ChatGPT | GPT-4o completo | GPT-4o (con rate limits y costo/token) |
| DeepSeek | R1 razonamiento completo | R1 (mismo pero $$$) |
| Gemini | 2.0 Flash / 2.5 Pro | 2.0 Flash ($0.075/1M tokens) |
| Grok | Grok-3 | Grok-3 (API limitada, waitlist) |
| Copilot | GPT-4o + Bing + DALL-E | N/A directo |
| Claude | Opus 4.5 (con Pro) | Opus ($15/1M tokens) |

**Conclusión:** Un duende con browser accede a más poder de cómputo que un duende con $100 en créditos API.

### Flujo de debate multi-IA vía browser

```
DUENDE (Claude in Chrome)
    │
    ├── Tab 1: chat.openai.com    → GPT-4o opina
    ├── Tab 2: chat.deepseek.com  → R1 critica a GPT
    ├── Tab 3: gemini.google.com  → Gemini critica a ambos
    ├── Tab 4: grok.com           → Grok da perspectiva X/Twitter
    │
    └── SÍNTESIS: El duende (Claude) consolida todo
```

Cada IA recibe:
1. El tema original
2. Lo que dijeron las otras IAs
3. Instrucción de criticar con datos

El duende orquestador NO opina en las rondas intermedias — solo transporta. Opina AL FINAL en la síntesis.

### Operativa técnica paso a paso

```
Para cada IA:
1. tabs_create_mcp             → Nueva pestaña
2. navigate(url)               → Ir al chat de la IA
3. computer(wait, 3)           → Esperar carga
4. find("message input")       → Encontrar caja de texto
5. computer(type, prompt)      → Escribir el prompt
6. computer(key, "Enter")      → Enviar
7. computer(wait, 15-30)       → Esperar respuesta (varía por IA)
8. get_page_text               → Leer respuesta completa
9. Guardar respuesta en variable

Para cross-posting:
10. navigate(tab siguiente IA)
11. Repetir 4-8 pero el prompt incluye respuestas previas

Para síntesis:
12. El duende (Claude) sintetiza sin browser — es su propia respuesta
```

### Requisitos para el duende activador

- ✅ Claude in Chrome conectado y funcional
- ✅ Arquitecto con sesión activa en al menos 2 IAs web
- ✅ Arquitecto disponible para resolver CAPTCHAs si aparecen
- ❌ NO necesita API keys de ninguna IA externa
- ❌ NO necesita créditos de ninguna IA externa
- ❌ NO necesita Desktop Commander ni Browser Engine (Puppeteer)

### Limitaciones

1. **Velocidad:** ~2-3 min por IA (navigate + type + wait + read) vs 10s por API. Un debate de 3 IAs × 2 rondas toma ~20-30 min.
2. **Rate limits web:** Algunas IAs limitan mensajes/hora en tier free (ChatGPT: ~40/3hrs, DeepSeek: variable)
3. **UI changes:** Si una IA cambia su interfaz, los selectores del duende pueden fallar. Adaptarse con `find()` + `screenshot`.
4. **CAPTCHAs:** El Arquitecto debe resolverlos. El duende pausa y avisa.



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

---

## ADDENDUM: Capa 1b — Browser Engine como Orquestador Multi-IA (2 Mar 2026)

### Descubrimiento

El Browser Engine (Puppeteer + Stealth) puede navegar a ChatGPT, Gemini, Copilot y otras IAs en modo headless, enviar prompts, extraer respuestas y cruzarlas — todo sin Chrome Extension y sin intervención humana.

### Implicación: "El Duende es la API" confirmado con datos

| Método | Costo | Tiempo | Datos |
|--------|-------|--------|-------|
| API de Anthropic | $$ por token | 6-20s | Inventados |
| Puppeteer → tier gratis de IAs | **$0** | 100-160s | **Reales** |

### Script de referencia

`C:\Users\pvrol\browser-duendes\debate-multiai-capa1.js`

### IAs probadas headless (sin login)

| IA | Funciona headless? | Notas |
|----|-------------------|-------|
| ChatGPT | ✅ Sí | Requiere selector `#prompt-textarea` |
| Gemini | ✅ Sí | `div[contenteditable="true"]` |
| Copilot | ⚠️ Parcial | Input no estándar, requiere más trabajo |
| DeepSeek | ✅ Sí (vía Chrome) | Probado con extensión, no headless aún |

### Caso de estudio completo

Ver: `RDE/CASO_ESTUDIO_DEBATE_TACOS.md`
