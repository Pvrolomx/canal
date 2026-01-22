# SPEC: MPM-Psi

## Descripción
Landing page y sistema de reservas para psicóloga independiente. Permite agendar sesiones, vender talleres/eventos, y cobrar en línea.

## Nombre Proyecto
**MPM-Psi** (MVP Psicóloga)

## URLs Objetivo
- Repo: github.com/Pvrolomx/mpm-psi
- Live: mpm-psi.vercel.app (o dominio personalizado)

## Stack Técnico
- **Framework**: Next.js 14 (App Router)
- **Hosting**: Vercel
- **Agenda**: Calendly embed
- **Pagos**: Stripe Checkout
- **Estilos**: Tailwind CSS
- **Tests**: Playwright

## Funcionalidades MVP

### 1. Landing Page
- Hero con foto y mensaje principal
- Sección "Sobre mí"
- Servicios ofrecidos (cards)
- Testimonios (opcional)
- CTA a agendar/comprar
- Footer con contacto y redes

### 2. Sistema de Citas
- Calendly embed para agendar
- Tipos de cita:
  - Sesión individual (50 min)
  - Primera consulta (30 min gratis o precio reducido)
- Confirmación automática por email

### 3. Tienda/Eventos
- Sección de productos:
  - Talleres grupales
  - Eventos especiales
  - Paquetes de sesiones
- Stripe Checkout para cada producto
- Payment Links o Checkout integrado

### 4. PWA
- Instalable
- manifest.json
- Iconos 192/512

## Estructura de Archivos
```
mpm-psi/
├── app/
│   ├── page.js          # Landing principal
│   ├── servicios/
│   │   └── page.js      # Detalle servicios
│   ├── agendar/
│   │   └── page.js      # Calendly embed
│   ├── tienda/
│   │   └── page.js      # Productos/eventos
│   ├── layout.js
│   └── globals.css
├── components/
│   ├── Hero.jsx
│   ├── Services.jsx
│   ├── Testimonials.jsx
│   ├── CalendlyEmbed.jsx
│   └── ProductCard.jsx
├── public/
│   ├── manifest.json
│   └── icons/
├── tests/
│   └── basic.spec.ts
├── playwright.config.ts
├── package.json
└── .github/
    └── workflows/
        └── playwright.yml
```

## Tests Playwright
```typescript
// tests/basic.spec.ts
- Landing carga correctamente
- Navegación funciona
- Calendly embed visible en /agendar
- Productos visibles en /tienda
- Links de Stripe funcionan
```

## Configuración Requerida

### Calendly
1. Crear cuenta Calendly
2. Configurar tipo de evento
3. Obtener URL de embed

### Stripe
1. Cuenta Stripe activada
2. Crear productos:
   - Sesión individual
   - Taller grupal
   - Paquete X sesiones
3. Obtener Payment Links o API keys

## Diseño
- **Colores**: Tonos calmos (verde salvia, beige, blanco)
- **Tipografía**: Sans-serif legible (Inter, Poppins)
- **Estilo**: Profesional, cálido, confiable
- **Target**: Adultos 25-55 años

## Fases de Desarrollo

### Fase 1: Setup (Día 1)
- [ ] Crear repo mpm-psi
- [ ] Setup Next.js + Tailwind
- [ ] Configurar Playwright
- [ ] Deploy inicial Vercel

### Fase 2: Landing (Día 2-3)
- [ ] Hero section
- [ ] Servicios
- [ ] Sobre mí
- [ ] Footer

### Fase 3: Integraciones (Día 4-5)
- [ ] Calendly embed
- [ ] Stripe productos
- [ ] PWA

### Fase 4: Polish (Día 6-7)
- [ ] Tests completos
- [ ] Responsive
- [ ] SEO básico
- [ ] Dominio (si hay)

## Criterios de Aceptación
1. Landing profesional y responsive
2. Calendly funcional para agendar
3. Al menos 2 productos en Stripe
4. PWA instalable
5. Tests Playwright pasando
6. Deploy en Vercel

## Firma
```
hecho con ❤️ por Duendes 2026
```

---
SPEC v1.0 | C_OG Dictaminador | Colmena 2026
