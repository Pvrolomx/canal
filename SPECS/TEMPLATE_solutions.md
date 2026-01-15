# SPEC: Template Solutions

> Sistema de Templates Verticales - Colmena
> Base para crear sitios profesionales en 10-15 minutos

---

## 🏗️ Estructura Base "Solutions"

Todos los templates Solutions comparten esta estructura:

```
[nombre]-solutions/
├── app/
│   ├── layout.js          ← Metadata + fonts
│   ├── globals.css        ← Estilos (colores editables)
│   ├── page.js            ← Landing + formulario
│   └── api/
│       └── contacto/
│           └── route.js   ← Envío de emails
├── public/
│   ├── manifest.json      ← PWA config
│   ├── logo.png           ← Logo del cliente
│   ├── icon-192.png       ← Icono PWA
│   └── icon-512.png       ← Icono PWA grande
├── package.json
├── next.config.js
├── tailwind.config.js
└── postcss.config.js
```

---

## 🎨 Cómo Personalizar un Template

### Paso 1: Clonar Template Base
```bash
# En GitHub, fork o copia el template
notaria-solutions-template → [cliente]-solutions
```

### Paso 2: Editar CONFIG (en page.js)
```javascript
const CONFIG = {
  nombre: 'Notaría Pública No. 15',      // ← Cambiar
  numero: 'No. 15',                       // ← Cambiar
  titular: 'Lic. Juan Pérez García',      // ← Cambiar
  telefono: '+52 322 123 4567',           // ← Cambiar
  whatsapp: '523221234567',               // ← Cambiar
  email: 'contacto@notaria15.com',        // ← Cambiar
  direccion: 'Av. México 123, Col. Centro', // ← Cambiar
  ciudad: 'Puerto Vallarta, Jalisco',     // ← Cambiar
  horario: 'Lunes a Viernes: 9:00 - 18:00', // ← Cambiar
}
```

### Paso 3: Editar Colores (en tailwind.config.js)
```javascript
colors: {
  'notaria-navy': '#1a365d',   // ← Color principal
  'notaria-gold': '#d4a84b',   // ← Color acento
  'notaria-cream': '#faf9f7',  // ← Color fondo
  'notaria-dark': '#0f172a',   // ← Color texto
}
```

### Paso 4: Editar Servicios (en page.js)
```javascript
const SERVICIOS = [
  { id: 'servicio1', icon: '📜', nombre: {...}, desc: {...} },
  // Agregar/quitar según el giro
]
```

### Paso 5: Subir Logo
- Reemplazar `/public/logo.png`
- Reemplazar `/public/icon-192.png` y `/public/icon-512.png`

### Paso 6: Configurar Email
En Vercel env vars:
- `RESEND_API_KEY` → API key de Resend
- `NOTIFICATION_EMAIL` → Email del cliente

---

## 🏢 Templates por Vertical

### Notaría Solutions ✅ LISTO
**Repo:** `Pvrolomx/notaria-solutions-template`
**Servicios:** Escrituras, Poderes, Testamentos, Actas Constitutivas, Matrimonios, Fe de Hechos, Apostillas
**Colores:** Navy (#1a365d), Gold (#d4a84b)

### Castle Solutions ✅ LISTO
**Repo:** `Pvrolomx/castle-checkin`
**URL:** castlesolutions.mx
**Servicios:** Propiedades, Check-in, Reservas
**Colores:** Gold (#C9A227), Cream (#F5F1E6)

### Legal Solutions (Por crear)
**Servicios:** Áreas de práctica, Consultas, Casos de éxito
**Colores:** Navy/Silver

### Medical Solutions (Por crear)
**Servicios:** Especialidades, Citas, Horarios, Seguros
**Colores:** Blue/White

### Dental Solutions (Por crear)
**Servicios:** Tratamientos, Antes/Después, Precios
**Colores:** Teal/White

### Resto Solutions (Por crear)
**Servicios:** Menú, Reservaciones, Galería
**Colores:** Por definir según cocina

---

## ⚡ Flujo de Ejecución

```
1. Cliente contacta → "Necesito página para mi [giro]"

2. Arquitecto identifica template:
   - Notaría → notaria-solutions-template
   - Abogado → legal-solutions-template
   - etc.

3. Arquitecto manda spec:
   GO: [cliente]-solutions
   TEMPLATE: [vertical]-solutions
   CONFIG:
     nombre: X
     telefono: X
     email: X
     servicios: [lista]
     colores: [hex]

4. Claude:
   - Clona template
   - Edita CONFIG
   - Edita colores
   - Sube logo (si hay)
   - Deploya
   - Reporta URL

5. Tiempo: 10-15 minutos
```

---

## 📋 Checklist de Entrega

- [ ] Landing funcionando
- [ ] Formulario enviando emails
- [ ] Bilingüe (🇲🇽/🇺🇸)
- [ ] PWA instalable
- [ ] Firma Colmena en footer
- [ ] Logo del cliente
- [ ] WhatsApp flotante
- [ ] Mobile responsive
- [ ] SSL activo

---

## 💰 Pricing Sugerido

| Complejidad | Tiempo | Precio |
|-------------|--------|--------|
| Template puro | 10-15 min | $800-1,500 MXN |
| + Personalización | 20-30 min | $1,500-2,500 MXN |
| + Funcionalidad extra | 30-60 min | $2,500-4,000 MXN |
| Custom desde cero | 1-2 hrs | $5,000+ MXN |

---

*Documentación Colmena — C0*
