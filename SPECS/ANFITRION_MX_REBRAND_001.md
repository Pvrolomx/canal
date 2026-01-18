# SPEC: ANFITRION-MX-REBRAND-001
# Rebranding de Calculadora Airbnb a "Anfitrión MX"

## Objetivo
Cambiar el branding de la calculadora a "Anfitrión MX" manteniendo
el dark theme actual y preparando para expansión internacional.

## Nombre y Tagline

**Nombre:** Anfitrión MX
**Tagline:** "Calcula tu ganancia real"
**Versión USA (futuro):** Host MX

## Archivos a Modificar

### 1. public/index.html (o equivalente)

```html
<!-- ANTES -->
<title>Calculadora Airbnb</title>

<!-- DESPUÉS -->
<title>Anfitrión MX - Calcula tu ganancia real</title>

<!-- Meta tags -->
<meta name="description" content="Calcula cuánto realmente ganas con Airbnb en México. Incluye comisiones, ISR, IVA y todos los impuestos.">
<meta name="keywords" content="airbnb, calculadora, mexico, impuestos, isr, iva, anfitrion, host">

<!-- Open Graph -->
<meta property="og:title" content="Anfitrión MX">
<meta property="og:description" content="Calcula tu ganancia real como anfitrión Airbnb en México">
<meta property="og:type" content="website">
```

### 2. Header Principal

```html
<!-- ANTES -->
<h1>Calculadora Airbnb</h1>

<!-- DESPUÉS -->
<header class="app-header">
  <div class="logo-container">
    <span class="logo-icon">🏠</span>
    <h1 class="app-title">Anfitrión MX</h1>
  </div>
  <p class="tagline">Calcula tu ganancia real</p>
</header>
```

### 3. CSS para Header

```css
.app-header {
  text-align: center;
  padding: 1.5rem 1rem;
  border-bottom: 1px solid #333;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.logo-icon {
  font-size: 2rem;
}

.app-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
  letter-spacing: -0.5px;
}

.tagline {
  color: #10b981; /* verde esmeralda */
  font-size: 0.9rem;
  margin-top: 0.25rem;
}
```

### 4. PWA Manifest (manifest.json)

```json
{
  "name": "Anfitrión MX",
  "short_name": "Anfitrión MX",
  "description": "Calcula tu ganancia real como anfitrión Airbnb",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#1a1a2e",
  "theme_color": "#10b981",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### 5. Footer

```html
<footer class="app-footer">
  <p>© 2026 Anfitrión MX</p>
  <p class="disclaimer">
    Esta herramienta ofrece cálculos aproximados con fines informativos.
    No constituye asesoría fiscal, contable ni legal.
  </p>
</footer>
```

### 6. Favicon

Crear favicon simple con emoji casa o icono minimalista.
Colores: Verde esmeralda (#10b981) sobre fondo oscuro (#1a1a2e)

## Paleta de Colores (mantener actual)

| Elemento | Color | Hex |
|----------|-------|-----|
| Fondo | Dark blue | #1a1a2e |
| Cards | Darker | #16213e |
| Acento principal | Esmeralda | #10b981 |
| Texto | Blanco | #ffffff |
| Texto secundario | Gris | #9ca3af |
| Botón primario | Verde | #10b981 |
| Botón hover | Verde claro | #34d399 |

## Elementos a NO Cambiar

- ✅ Dark theme actual
- ✅ Layout del formulario
- ✅ Lógica de cálculo
- ✅ Sistema de créditos
- ✅ Generación de PDF

## Checklist de Implementación

- [ ] Actualizar title y meta tags
- [ ] Cambiar header con nuevo nombre y tagline
- [ ] Actualizar manifest.json para PWA
- [ ] Crear/actualizar favicon
- [ ] Actualizar footer con copyright
- [ ] Verificar que PDF generado muestre nuevo nombre
- [ ] Test en móvil (PWA)

## Preview Esperado

```
┌─────────────────────────────────┐
│         🏠 Anfitrión MX         │
│     Calcula tu ganancia real    │
├─────────────────────────────────┤
│                                 │
│   [Formulario de cálculo...]    │
│                                 │
├─────────────────────────────────┤
│   © 2026 Anfitrión MX           │
│   Disclaimer...                 │
└─────────────────────────────────┘
```

---
Spec creado: 2026-01-18
Autor: C1 (Sleepy)
Prioridad: Media
Siguiente: SPEC de Stripe Payment Links
