# 🔄 HANDOFF - Colmena

> Última actualización: **C0** | 15 Ene 2026

---

## 🏗️ Sistema Colmena OPS

### Estructura del Repo Canal
```
Pvrolomx/canal/
├── mensajes.txt           ← Comandos del Arquitecto
├── HANDOFF.md             ← Estado actual (este archivo)
├── BIENVENIDA_COLMENA.md  ← Onboarding para nuevos Claudes
├── REGLAS_DE_EJECUCION_v1.1.md ← Las reglas del juego
└── SPECS/                 ← Especificaciones de proyectos
    ├── README.md
    ├── TEMPLATE_landing.md
    ├── TEMPLATE_formulario.md
    ├── TEMPLATE_catalogo.md
    ├── TEMPLATE_dashboard.md
    └── TEMPLATE_herramienta.md
```

### Comandos Estándar
| Comando | Acción |
|---------|--------|
| `GO: [proyecto]` | Ejecutar spec de SPECS/[proyecto].md |
| `STATUS` | Reportar estado actual |
| `FIX: [issue]` | Corregir algo específico |
| `ADD: [feature]` | Agregar feature a proyecto existente |

---

## 🔑 Cómo conseguir los tokens

**Paso 1:** Arquitecto pasa token de Vercel por canal (partido en 2)

**Paso 2:** Usar Vercel token para leer los otros:
```bash
curl -s "https://api.vercel.com/v9/projects/prj_E2lZttCaFz5VmiL0FY3xY6oTxDkY/env?teamId=team_xmFW0blsjqFI5lwt29wBPi8Q" \
  -H "Authorization: Bearer [VERCEL_TOKEN]"
```

**Tokens en Vercel env vars:**
- `GH_TOKEN` → GitHub API
- `RESEND_API_KEY` → Email API

---

## 📍 Proyecto Activo: Castle Solutions

**Repo:** `Pvrolomx/castle-checkin`  
**URL:** https://castlesolutions.biz  
**Status:** ✅ DONE (landing + checkin + PWA)

### Pendiente:
- ⏳ Fotos reales de propiedades
- ⏳ WhatsApp real
- ⏳ Links a Airbnb

---

## 📊 Registro de Proyectos

| Proyecto | Cliente | Tipo | Status | Claude | URL |
|----------|---------|------|--------|--------|-----|
| castle-checkin | Claudia | formulario | ✅ DONE | C0 | castlesolutions.biz |

---

## 📝 Linaje de Claudes

| ID | Sesión | Proyectos |
|----|--------|-----------|
| C0 | 15 Ene 2026 | Castle Solutions, Sistema SPECS |

---

## ▶️ Siguiente paso

Sistema listo. Esperando próximo `GO: [proyecto]`

---

*Actualizar con cada movimiento significativo.*

— **C0** 🏰
