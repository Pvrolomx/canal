# 🐝 REGLAS DE EJECUCIÓN - COLMENA CLOUD v1
## Sistema de Deploy Autónomo desde la Nube

> **Versión:** 1.0  
> **Fecha:** 17 Enero 2026  
> **Contexto:** Claudes operando desde claude.ai (sin acceso a RPi/Desktop)  
> **Basado en:** REGLAS_DE_EJECUCION_RPI_v1 + experiencia C16, C17, C14 Cloud

---

## 🎯 PRINCIPIO CORE

> **La app es la construcción de la app, no el producto.**

No perseguir app perfecta directamente.  
Perseguir perfección en el PROCESO de construcción.  
App perfecta emerge NATURALMENTE como consecuencia.

---

## 📋 LAS 15 REGLAS CLOUD

### BLOQUE 1: EJECUCIÓN (Reglas 1-4)

#### 1. EJECUTA, NO PREGUNTES
Si tienes duda, toma la decisión y sigue.  
Preguntar = fricción = tiempo perdido.  
Es más fácil pedir perdón que permiso.

#### 2. ESCRIBE COMPLETO, NO PARCIAL
Un archivo se escribe entero de una vez.  
Nada de "continuará..." o chunks parciales.  
Excepción: Archivos >500 líneas (poco común en MVP).

#### 3. SI ALGO FALLA, NO DEBUGGEAR - REHACER
No pierdas tiempo debuggeando en MVP.  
Borra y rehaz desde cero.  
**Excepción:** Apps en producción con usuarios reales.

#### 4. UN PASE
Lo que salga en primer intento, se queda.  
Iteras solo si el usuario lo pide.  
Bonito y rápido no pelean. Perfeccionismo sí.

---

### BLOQUE 2: ARQUITECTURA (Reglas 5-7)

#### 5. ARCHIVOS ATÓMICOS
Cada archivo hace UNA cosa.  
Si falla, se reemplaza entero, no se parchea.  
Componentes pequeños, independientes, reemplazables.

#### 6. SI UN COMANDO FALLA, USA ALTERNATIVA
No debuggues. Usa otra herramienta/método y sigue.  
Ejemplos:
- GitHub API falla → Verificar token y reintentar
- Vercel API falla → Verificar proyecto existe
- Build falla → Revisar imports/dependencias

#### 7. CREDENCIALES SEGURAS
- Tokens NUNCA hardcodeados en código
- Usar variables de entorno
- GitHub rechaza push si detecta tokens

---

### BLOQUE 3: TIEMPO Y CALIDAD (Reglas 8-9)

#### 8. DETECTOR DE FRICCIÓN
Si llevas >15 min sin output visible, PARA.  
Algo está mal. Replantea.  
El tiempo no es límite, es sensor.

#### 9. SMOKE TEST ANTES DE REPORTAR
Antes de dar URL como completada:
- ✅ App carga sin errores
- ✅ Rutas principales funcionan
- ✅ No hay errores críticos en consola
- ⏱️ Tiempo: 30-60 segundos

---

### BLOQUE 4: ESTÁNDARES (Reglas 10-12)

#### 10. FIRMA DEL AGENTE
Cada app debe identificar quién la creó.

**Footer visible (obligatorio):**
```
Hecho por duendes.app 2026
```

**En commits:**
```
feat: initial commit - ProfeApp
```

#### 11. PWA - INSTALAR APP
Toda app debe ser instalable. Requisitos mínimos:

**manifest.json:**
```json
{
  "name": "Nombre App",
  "short_name": "App",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#000000",
  "icons": [
    {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}
  ]
}
```

**Service Worker básico** para cache offline.

**Botón "Instalar App"** visible en la UI.

#### 12. FRAMEWORK PRESET EN VERCEL
Al crear proyecto, verificar que Framework Preset = "Next.js" (no "Other").  
Si está en "Other", todas las rutas dan 404.

---

## 🔧 FLUJO DE DEPLOY CLOUD

```
1. LEER SPEC
   └── Canal GitHub (mensajes.txt) o instrucción directa

2. CREAR REPO (GitHub API)
   └── POST /user/repos
   └── Token PAT con permisos repo

3. GENERAR CÓDIGO
   └── Archivos completos, atómicos
   └── Incluir manifest.json + iconos + SW

4. PUSH A GITHUB (API)
   └── PUT /repos/{owner}/{repo}/contents/{path}
   └── Un archivo a la vez con content en base64

5. CREAR PROYECTO VERCEL (API)
   └── POST /v10/projects
   └── Conectar repo de GitHub

6. ENV VARS SI NECESARIO (API)
   └── POST /v10/projects/{id}/env
   └── type: "encrypted" para secrets

7. DEPLOY
   └── Automático al conectar repo, o
   └── vercel deploy --prod --token

8. VERIFICAR
   └── Smoke test
   └── Reportar URL
```

---

## 🔑 TOKENS REQUERIDOS

Para operar autónomamente necesitas:

| Token | Permisos | Uso |
|-------|----------|-----|
| **GitHub PAT** | repo, workflow | Crear repos, push código |
| **Vercel Token** | Full account | Crear proyectos, deploy, env vars |

**Importante:** 
- Token básico `ghp_` funciona para push
- Token fine-grained `github_pat_` puede crear repos si tiene permiso

---

## 📊 MÉTRICAS DE ÉXITO

| Métrica | Target |
|---------|--------|
| Tiempo SPEC → Deploy | ≤15 min |
| Archivos reescritos | ≤2 |
| Preguntas al usuario | 0-1 |
| PWA instalable | Sí |
| Firma visible | Sí |

---

## ❌ LO QUE NO APLICA EN CLOUD

Estas reglas son para Desktop/RPi y NO aplican aquí:

- Listeners TCP / Puertos / Firewall
- SSH / SCP / Usuario pvrolo@
- Python vs sed (encoding SSH)
- Configuración de IPs locales
- Hub LAQCA / puente.js

---

## 🚀 CAPACIDADES CLOUD CONFIRMADAS

| Acción | Método | Status |
|--------|--------|--------|
| Crear repo | GitHub API | ✅ |
| Push código | GitHub API | ✅ |
| Crear proyecto Vercel | Vercel API | ✅ |
| Deploy | Vercel CLI/API | ✅ |
| Env vars plain | Vercel API | ✅ |
| Env vars encrypted | Vercel API | ✅ |
| PWA completa | manifest + SW | ✅ |
| Instalar App button | beforeinstallprompt | ✅ |

---

## 💡 COMUNICACIÓN CON ARQUITECTO

**Canal GitHub:** `Pvrolomx/canal/mensajes.txt`

**Convención:**
- `.` en chat = "Revisa el canal"
- Arquitecto escribe instrucciones en canal
- Claude lee y ejecuta

**Reportar resultados:**
- URL de la app
- URL del repo
- Cualquier issue encontrado

---

## 📝 CHECKLIST PRE-DEPLOY

- [ ] Tokens GitHub y Vercel disponibles
- [ ] SPEC claro (qué construir)
- [ ] Nombre del proyecto definido
- [ ] manifest.json incluido
- [ ] Iconos PWA generados (192 + 512)
- [ ] Service worker incluido
- [ ] Botón "Instalar App" en UI
- [ ] Firma en footer

---

## 📝 CHECKLIST POST-DEPLOY

- [ ] App carga correctamente
- [ ] Todas las rutas funcionan
- [ ] PWA es instalable
- [ ] Firma visible en footer
- [ ] URL reportada al Arquitecto

---

*"La app es la construcción de la app, no el producto."*

🐝 **duendes.app Cloud — Deploy autónomo desde la nube**

---

## ⚠️ PERSISTENCIA Y COMMITS (CRÍTICO)

> **Aprendizaje del 17 Ene 2026:** Containers cloud son EFÍMEROS.  
> Si Claude muere/timeout, TODO el trabajo se pierde si no está en GitHub.

### PROBLEMA:
Claude cloud trabaja en container temporal. Si:
- Se acaba el contexto
- Hay timeout
- El usuario cierra el chat
- Cualquier interrupción

→ **TODO el código desaparece** si no fue pusheado.

### SOLUCIÓN - COMMITS FRECUENTES:

#### 1. CREAR REPO PRIMERO
```
Antes de escribir UNA línea de código:
1. Verificar tokens GitHub/Vercel
2. Crear repo vacío en GitHub
3. Push inicial (aunque sea README)
4. ENTONCES empezar a construir
```

#### 2. COMMITS CADA 10-15 MINUTOS
| Momento | Acción |
|---------|--------|
| Estructura inicial creada | → commit |
| Cada componente terminado | → commit |
| Cada página terminada | → commit |
| Antes de operación larga | → commit |
| API endpoint listo | → commit |

#### 3. SI NO HAY MCP/TOKENS
```
❌ NO empezar a construir en el void
✅ Notificar al usuario INMEDIATAMENTE
✅ Pedir tokens o acordar deploy manual
✅ Usuario puede hacer deploy desde Vercel dashboard
```

### BENEFICIO:
- ✅ Siguiente Claude continúa donde quedó anterior
- ✅ Usuario sabe exactamente dónde está el código
- ✅ No se pierde trabajo por timeouts
- ✅ Rollback posible si algo falla

### CHECKLIST PERSISTENCIA:
- [ ] Repo creado ANTES de construir
- [ ] Primer commit hecho (aunque sea vacío)
- [ ] Commits cada 10-15 min durante build
- [ ] Push final antes de reportar URL

---

## HISTORIAL

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.1 | 17 Ene 2026 | C1 (Sleepy) | + Sección Persistencia y Commits |
| 1.0 | 17 Ene 2026 | Claude (ProfeApp) | Versión inicial cloud |


---

## REGLA #13 CLOUD: DESARROLLO CLOUD-FIRST, RPi VIA GIT PULL
**Agregado:** 7 Febrero 2026 por CD37

### CONTEXTO

Cuando un duende Cloud necesita que codigo llegue al RPi (ej: actualizar archivos en repos locales),
el flujo OBLIGATORIO es:

```
Container Claude -> GitHub API (PUT base64) -> RPi: git pull
```

### NUNCA HACER ESTO DESDE CLOUD:
- Intentar escribir archivos en RPi via SSH heredocs pasados por PowerShell
- Mandar contenido de archivos por el pipe SSH (encoding se corrompe)
- Pedir al usuario que copie/pegue codigo largo manualmente

### FLUJO CORRECTO:

```bash
# 1. Obtener SHA del archivo actual en GitHub
SHA=$(curl -s -H "Authorization: token TOKEN"   "https://api.github.com/repos/Pvrolomx/REPO/contents/path/archivo.js" |   python3 -c "import sys,json; print(json.load(sys.stdin)['sha'])")

# 2. Push archivo nuevo via API
B64=$(base64 /home/claude/archivo.js | tr -d '\n')
curl -s -X PUT   -H "Authorization: token TOKEN"   "https://api.github.com/repos/Pvrolomx/REPO/contents/path/archivo.js"   -d "{\"message\":\"update\",\"content\":\"$B64\",\"sha\":\"$SHA\"}"

# 3. Sync al RPi (si tienes acceso SSH via Desktop Commander)
ssh pvrolo@192.168.1.84 "cd ~/repos/REPO && git checkout main && git pull origin main"
```

### TOKEN
Buscar en /home/pvrolo/colmena/keys/TOKENS.md (seccion GITHUB PAT)
O pedir al humano en el canal general (channel 1)

### BENEFICIO
- UTF-8 perfecto siempre (container Claude es Linux nativo)
- Emojis, acentos, caracteres especiales sin problema
- 2 minutos vs horas de debug de encoding
- El duende gasta contexto en construir, no en plomeria

---

## REGLA #14 CLOUD: VERIFICACIÓN PROPORCIONAL AL RIESGO
**Agregado:** 15 Febrero 2026 por CD42

### PROBLEMA QUE RESUELVE

Los CDs queman tokens y contexto haciendo múltiples llamadas MCP/API para verificar deploys que ya están listos. En el peor caso, las llamadas se cuelgan y el CD se queda atorado sin avanzar.

### LA REGLA

**El costo de verificar no debe exceder el costo de fallar.**

### NIVELES DE VERIFICACIÓN

| Tipo de deploy | Verificación | NO hacer |
|----------------|-------------|----------|
| **Estático** (HTML/CSS/JS, sin build) | `curl -s URL` → ¿200? Listo | MCP calls, API polling, build logs, sleep loops |
| **Con build** (Next.js, dependencias) | Verificar build logs SI hay cambios en package.json/config. curl + smoke test | Polling excesivo si no hay cambios de dependencias |
| **Con datos/env vars** (Supabase, Stripe) | Verificar env vars configuradas. Smoke test funcional | Asumir que funciona solo porque carga |

### PRINCIPIO

```
git push exitcode=0 + HTML estático → CONFÍA Y SIGUE
git push exitcode=0 + Next.js sin cambios de deps → curl 200 y sigue
git push exitcode=0 + cambios en package.json → ahí sí verifica build logs
```

### CONTEXTO

CD42, 15 Feb 2026: Hizo push de imagen (16KB) a HTML estático. Deploy tomó ~5 segundos. CD se quedó atorado 10+ minutos haciendo llamadas MCP a Vercel que se colgaron, quemando tokens y contexto mientras el sitio ya estaba live.

### RELACIÓN CON OTRAS REGLAS

- Complementa **Regla #8 Cloud** (Detector de Fricción): verificación excesiva ES fricción
- Complementa **Nota C14 Eco** (firewall): no asumir fallo sin verificar resultado final
- Aplica el espíritu de **Regla #8 RPi** ("Verifica al final, no durante") al contexto de deploy

---

## REGLA #15 CLOUD: VERCEL API DIRECTA PARA ENV VARS Y CONFIGURACIÓN
**Agregado:** 24 Febrero 2026 por CD44

### PROBLEMA QUE RESUELVE

Los CDs necesitan crear, leer y actualizar variables de entorno en Vercel (API keys, webhook secrets, tokens encrypted). El MCP de Vercel puede tener limitaciones con operaciones PATCH y con valores encrypted. Usar la REST API directa es más confiable y transparente.

### CREDENCIALES VERCEL

```
Token: buscar en canal general (channel 1) el mensaje con credenciales
Team ID: team_xmFW0blsjqFI5lwt29wBPi8Q
```

### OPERACIONES COMUNES

```bash
# Listar proyectos
curl -s -H "Authorization: Bearer $VERCEL_TOKEN" \
  "https://api.vercel.com/v9/projects?teamId=$TEAM_ID"

# Listar env vars de un proyecto
curl -s -H "Authorization: Bearer $VERCEL_TOKEN" \
  "https://api.vercel.com/v10/projects/$PROJECT_ID/env?teamId=$TEAM_ID"

# Crear env var (encrypted)
curl -s -X POST -H "Authorization: Bearer $VERCEL_TOKEN" \
  "https://api.vercel.com/v10/projects/$PROJECT_ID/env?teamId=$TEAM_ID" \
  -H "Content-Type: application/json" \
  -d '{"key":"NOMBRE","value":"valor","type":"encrypted","target":["production","preview","development"]}'

# Actualizar env var existente (necesita ENV_ID)
# Primero obtener el ID:
ENV_ID=$(curl -s -H "Authorization: Bearer $VERCEL_TOKEN" \
  "https://api.vercel.com/v10/projects/$PROJECT_ID/env?teamId=$TEAM_ID" | \
  python3 -c "import sys,json; [print(e['id']) for e in json.load(sys.stdin).get('envs',[]) if e['key']=='NOMBRE']")

# Luego actualizar:
curl -s -X PATCH -H "Authorization: Bearer $VERCEL_TOKEN" \
  "https://api.vercel.com/v10/projects/$PROJECT_ID/env/$ENV_ID?teamId=$TEAM_ID" \
  -H "Content-Type: application/json" \
  -d '{"value":"nuevo_valor","type":"encrypted"}'
```

### ERRORES COMUNES

| Error | Causa | Solución |
|-------|-------|----------|
| `ENV_CONFLICT` | Variable ya existe | Usar PATCH en vez de POST |
| `404` en env | ENV_ID incorrecto | Listar primero para obtener ID correcto |
| MCP timeout | Vercel MCP se cuelga | Usar curl directo a REST API |

### CUÁNDO USAR QUÉ

| Operación | MCP Vercel | REST API directa |
|-----------|-----------|-------------------|
| Deploy | ✅ Preferir | ✅ Alternativa |
| Listar proyectos | ✅ | ✅ |
| Crear/leer env vars | ⚠️ Puede fallar | ✅ Preferir |
| Actualizar env vars (PATCH) | ❌ No soporta | ✅ Obligatorio |
| Env vars encrypted | ⚠️ Inconsistente | ✅ Preferir |
| Build logs | ✅ | ✅ |

### FETCH DE CONTENIDO DESPLEGADO

| Necesitas | Método | NO hacer |
|-----------|--------|----------|
| Ver source code del proyecto | `git clone` / `git pull` del repo | `Vercel:web_fetch_vercel_url` que se cuelga |
| Ver página live (HTML renderizado) | `curl -s https://dominio.com` | Múltiples intentos con MCP si el primero falla |
| Comparar cambios recientes | `git pull` + `git diff` | Fetch repetido de páginas completas |

**Contexto:** CD44, 25 Feb 2026 — Durante QA de astro4, intentó fetch de app.html vía `Vercel:web_fetch_vercel_url`. La llamada se colgó sin respuesta. Se resolvió con `git pull` + `git diff` que trajo los cambios en segundos.

### PRINCIPIO

> **Si el MCP funciona, úsalo. Si necesitas PATCH, encrypted, o el MCP se cuelga, usa curl directo a la REST API. No pierdas tiempo debuggeando el MCP.**

> **El repo en GitHub ES la fuente de verdad. Si necesitas inspeccionar código, clona el repo — no intentes extraerlo de la página desplegada.**

---

---

## APENDICE PWA: INSTALACION AUTOMATICA (Agregado 20 Mar 2026)

### PROBLEMA
El manifest.json y Service Worker NO son suficientes para que Chrome
muestre el prompt de instalacion en Android. Chrome requiere 2 visitas
con 5+ minutos entre ellas. Muchos usuarios nunca ven el prompt.

### SOLUCION: Boton de Instalacion Manual (OBLIGATORIO)

```javascript
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    document.getElementById('install-btn').classList.remove('hidden');
});
function installApp() {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(r => {
        if (r.outcome === 'accepted') document.getElementById('install-btn').classList.add('hidden');
        deferredPrompt = null;
    });
}
window.addEventListener('appinstalled', () => {
    document.getElementById('install-btn').classList.add('hidden');
});
```

HTML:
```html
<button id="install-btn" onclick="installApp()" class="hidden">Instalar App</button>
```

### SERVICE WORKER: NETWORK-FIRST (OBLIGATORIO)

NUNCA cache-first para HTML/API. Causa que updates no se vean.
Aprendido con fantasma.duendes.app el 20-Mar-2026.

```javascript
const CACHE_NAME = 'app-v2';
self.addEventListener('fetch', event => {
    if (event.request.url.includes('/api/') || event.request.url.endsWith('/')) {
        event.respondWith(
            fetch(event.request).then(resp => {
                caches.open(CACHE_NAME).then(c => c.put(event.request, resp.clone()));
                return resp;
            }).catch(() => caches.match(event.request))
        );
    } else {
        event.respondWith(caches.match(event.request).then(r => r || fetch(event.request)));
    }
});
self.addEventListener('activate', event => {
    event.waitUntil(caches.keys().then(n => Promise.all(n.filter(x => x !== CACHE_NAME).map(x => caches.delete(x)))));
    self.clients.claim();
});
```

### SI CACHE VIEJO BLOQUEA UPDATES
```javascript
navigator.serviceWorker.getRegistrations().then(r => r.forEach(x => x.unregister()));
caches.keys().then(n => n.forEach(x => caches.delete(x)));
```

### MANIFEST CRITICO
- display: "standalone" (NO "browser")
- purpose: "any maskable" en iconos
- start_url: "/" presente
- name + short_name ambos

### CHECKLIST PWA ACTUALIZADO
- [ ] manifest.json con display:standalone + iconos maskable
- [ ] SW con network-first para HTML/API
- [ ] Boton "Instalar App" con beforeinstallprompt
- [ ] CACHE_NAME versionado
