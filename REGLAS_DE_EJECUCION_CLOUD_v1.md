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

## 📋 LAS 12 REGLAS CLOUD

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
Hecho con 🧡 por Colmena 2026
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

🐝 **Colmena Cloud — Deploy autónomo desde la nube**

---

## HISTORIAL

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 17 Ene 2026 | Claude (ProfeApp) | Versión inicial cloud |
