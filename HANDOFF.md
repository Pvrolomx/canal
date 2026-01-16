# 🔄 HANDOFF - Colmena

> Última actualización: **C20** | 16 Ene 2026

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
    ├── TEMPLATE_solutions.md
    ├── TEMPLATE_miclase.md    ← NUEVO: App para profesores
    ├── SPEC profe.md
    └── HANDOFF profe.md
```

---

## 📦 Templates Disponibles

| Template | Repo | URL Demo | Status | Uso |
|----------|------|----------|--------|-----|
| Castle Solutions | `castle-checkin` | castlesolutions.mx | ✅ PROD | Rentas vacacionales |
| Notaría Solutions | `notaria-solutions-template` | notaria-solutions-template.vercel.app | ✅ TEMPLATE | Notarías |
| **MiClase** | `miclase` | miclase-eight.vercel.app | ✅ TEMPLATE | **Profesores universitarios** |

---

## 📚 NUEVO: Template MiClase

### Qué es
App de gestión para profesores universitarios con:
- Login por roles (Profe/Alumno)
- Crear grupos con código
- **QR dinámico** para asistencia (cambia cada 2 min)
- Scanner QR para alumnos
- PWA instalable

### Cómo usar
```
GO: [cliente]-miclase
TEMPLATE: miclase
CONFIG:
  appName: "ClaseUDG"
  institucion: "Universidad de Guadalajara"
  dominioEmail: "@udg.mx"
  colorPrimary: "#1e40af"
```

### Casos de uso
- Universidad completa
- Profesor individual  
- Preparatoria/Secundaria

**Tiempo estimado:** 5-10 minutos por clon

**SPEC completo:** `SPECS/TEMPLATE_miclase.md`

---

## 🔑 Tokens

**Vercel token** → Se pasa por canal (partido)
**GitHub token** → ghp_ + segunda parte en canal

---

## 📊 Proyectos Activos

### Castle Solutions ✅
- **Repo:** `Pvrolomx/castle-checkin`
- **URL:** https://castlesolutions.mx
- **Status:** Producción

### Notaría Solutions Template ✅
- **Repo:** `Pvrolomx/notaria-solutions-template`
- **URL:** https://notaria-solutions-template.vercel.app
- **Status:** Template listo

### MiClase ✅ NUEVO
- **Repo:** `Pvrolomx/miclase`
- **URL:** https://miclase-eight.vercel.app
- **Status:** Template listo para clonar

---

## 📝 Linaje

| ID | Sesión | Proyectos |
|----|--------|-----------|
| C0 | 15 Ene 2026 | Castle Solutions, Sistema SPECS, Notaría Template |
| C20 | 16 Ene 2026 | **MiClase** - Template para profesores |

---

## ▶️ Próximos Pasos

Templates listos:
1. Solutions (negocios locales)
2. **MiClase (profesores)** ← NUEVO

Comando ejemplo para clonar MiClase:
```
GO: asistencia-udg
TEMPLATE: miclase
CONFIG:
  appName: "Asistencia UDG"
  institucion: "Universidad de Guadalajara"
  colorPrimary: "#1e3a8a"
```

---

— **C20** 📚
