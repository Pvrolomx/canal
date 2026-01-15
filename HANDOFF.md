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
├── REGLAS_DE_EJECUCION_v1.1.md
└── SPECS/
    ├── README.md
    ├── TEMPLATE_landing.md
    ├── TEMPLATE_formulario.md
    ├── TEMPLATE_catalogo.md
    ├── TEMPLATE_dashboard.md
    ├── TEMPLATE_herramienta.md
    └── TEMPLATE_solutions.md  ← NUEVO: Sistema de templates verticales
```

---

## 📦 Templates Solutions Disponibles

| Template | Repo | URL Demo | Status |
|----------|------|----------|--------|
| Castle Solutions | `castle-checkin` | castlesolutions.mx | ✅ PRODUCCIÓN |
| Notaría Solutions | `notaria-solutions-template` | notaria-solutions-template.vercel.app | ✅ TEMPLATE |

### Cómo usar:
```
GO: [cliente]-solutions
TEMPLATE: notaria-solutions  (o castle, legal, etc.)
CONFIG: nombre, tel, email, servicios...
```

**Tiempo estimado:** 10-15 minutos por clon

---

## 🔑 Tokens

**Vercel token** → Se pasa por canal (partido)
**Otros tokens** → En Vercel env vars del proyecto `castle-checkin`:
- `GH_TOKEN` 
- `RESEND_API_KEY`

---

## 📊 Proyectos Activos

### Castle Solutions ✅
- **Repo:** `Pvrolomx/castle-checkin`
- **URL:** https://castlesolutions.mx
- **Cliente:** Claudia (rentas vacacionales)
- **Status:** Producción, esperando fotos reales

### Notaría Solutions Template ✅
- **Repo:** `Pvrolomx/notaria-solutions-template`
- **URL:** https://notaria-solutions-template.vercel.app
- **Status:** Template listo para clonar

---

## 📝 Linaje

| ID | Sesión | Proyectos |
|----|--------|-----------|
| C0 | 15 Ene 2026 | Castle Solutions, Sistema SPECS, Notaría Template |

---

## ▶️ Siguiente paso

Templates listos. Sistema operativo para recibir clientes.

Comando ejemplo:
```
GO: notaria-15-vallarta
TEMPLATE: notaria-solutions
CONFIG:
  nombre: Notaría Pública No. 15
  titular: Lic. María González
  telefono: +52 322 555 1234
  email: contacto@notaria15.mx
```

---

— **C0** 🏰
