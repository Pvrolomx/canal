# 📚 TEMPLATE: MiClase

> App de gestión para profesores universitarios

---

## 🚀 USO RÁPIDO

```
GO: [nombre-proyecto]
TEMPLATE: miclase
CONFIG:
  appName: "ClaseUDG"
  institucion: "Universidad de Guadalajara"
  dominioEmail: "@udg.mx"
  colorPrimary: "#1e40af"
  colorSecondary: "#7c3aed"
  profesorNombre: "Dr. García"  (opcional, si es app personal)
```

**Tiempo estimado:** 5-10 minutos

---

## 📦 REPO BASE

- **Template:** `github.com/Pvrolomx/miclase`
- **Stack:** Next.js 14 + Tailwind + PWA
- **Demo:** https://miclase-eight.vercel.app

---

## 🎨 VARIABLES DE PERSONALIZACIÓN

| Variable | Default | Descripción |
|----------|---------|-------------|
| `appName` | MiClase | Nombre de la app |
| `appSlogan` | Tu clase, simplificada | Slogan en landing |
| `institucion` | (vacío) | Nombre de universidad |
| `dominioEmail` | (vacío) | Ej: @udg.mx para validar |
| `colorPrimary` | #2563eb | Color profesor (azul) |
| `colorSecondary` | #7c3aed | Color alumno (morado) |
| `profesorNombre` | (vacío) | Si es app de 1 solo profe |
| `qrDuracion` | 120 | Segundos antes de regenerar QR |

---

## 📁 ARCHIVOS A MODIFICAR

### 1. `CONFIG.ts` (raíz)
Archivo central de configuración. Cambiar valores aquí.

### 2. `app/layout.tsx`
- Cambiar `title` y `description` en metadata
- Cambiar `themeColor`

### 3. `app/page.tsx` (landing)
- Cambiar textos del hero
- Cambiar colores si es necesario
- Logo de institución

### 4. `tailwind.config.js`
- Cambiar colores `primary` y `secondary`

### 5. `public/manifest.json`
- Cambiar `name`, `short_name`
- Cambiar `theme_color`, `background_color`

### 6. `public/` (iconos)
- Reemplazar `icon-192.png` y `icon-512.png` con logo

---

## 🔧 PROCESO DE CLONACIÓN

```bash
# 1. Crear nuevo repo
POST github.com/user/repos → nombre: "[cliente]-miclase"

# 2. Copiar archivos del template
GET github.com/Pvrolomx/miclase/contents → copiar todo

# 3. Modificar CONFIG.ts con datos del cliente

# 4. Modificar archivos según CONFIG

# 5. Push a nuevo repo

# 6. Deploy en Vercel
POST vercel.com/v10/projects → conectar repo

# 7. Entregar URL
```

---

## 📋 CHECKLIST PRE-ENTREGA

- [ ] Nombre de app cambiado en todos lados
- [ ] Colores personalizados
- [ ] Logo de institución (si aplica)
- [ ] Dominio de email configurado (si aplica)
- [ ] PWA manifest actualizado
- [ ] Iconos reemplazados
- [ ] Footer con créditos correctos
- [ ] URL funcionando en Vercel

---

## 💡 CASOS DE USO

### A) Universidad completa
```
appName: "AsistenciaUDG"
institucion: "Universidad de Guadalajara"
dominioEmail: "@udg.mx"
registroAbierto: true
```

### B) Profesor individual
```
appName: "Clase Dr. García"
profesorNombre: "Dr. Juan García"
soloAlumnos: true  (profes no se registran)
```

### C) Preparatoria
```
appName: "AsistenciaPrepa5"
institucion: "Preparatoria No. 5"
colorPrimary: "#dc2626"  (rojo escolar)
```

---

## 🏷️ FIRMA

Al entregar, el footer debe decir:
```
Creado por [CX] | Colmena 2026
```

---

*Template creado por C20 | Colmena 2026*
