# SPEC: ANFITRION-MX-UX-002
# Grid 2 Columnas en Resultados Móvil

## Objetivo
Reducir scroll en móvil mostrando resultados en grid de 2 columnas.

## Problema Actual
- Resultados en 1 columna desperdician espacio horizontal
- Usuario debe scrollear mucho para ver todos los datos

## Solución
CSS Grid responsive que muestra 2 columnas en móvil.

## Implementación

### CSS Grid para Resultados

```css
/* Grid de resultados */
.resultados-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  padding: 1rem;
}

/* Cada item de resultado */
.resultado-item {
  background: #1a1a2e;
  border: 1px solid #374151;
  border-radius: 8px;
  padding: 0.75rem;
  text-align: center;
}

.resultado-item .label {
  font-size: 0.75rem;
  color: #9ca3af;
  margin-bottom: 0.25rem;
}

.resultado-item .valor {
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
}

.resultado-item .valor-usd {
  font-size: 0.75rem;
  color: #6b7280;
}

/* Item que ocupa 2 columnas (ganancia neta ya no necesario) */
.resultado-item.full-width {
  grid-column: span 2;
}

/* Colores por tipo */
.resultado-item.ingreso .valor { color: #10b981; }
.resultado-item.deduccion .valor { color: #ef4444; }
.resultado-item.neutral .valor { color: #f59e0b; }

/* Desktop: 3 columnas */
@media (min-width: 768px) {
  .resultados-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### HTML Estructura

```html
<div class="resultados-grid">
  <div class="resultado-item ingreso">
    <div class="label">Ingreso bruto</div>
    <div class="valor" id="res-ingreso">$1,000</div>
    <div class="valor-usd">≈ $50 USD</div>
  </div>
  
  <div class="resultado-item deduccion">
    <div class="label">Comisión</div>
    <div class="valor" id="res-comision">-$30</div>
    <div class="valor-usd">3%</div>
  </div>
  
  <div class="resultado-item deduccion">
    <div class="label">Ret. ISR</div>
    <div class="valor" id="res-isr">-$40</div>
    <div class="valor-usd">4%</div>
  </div>
  
  <div class="resultado-item deduccion">
    <div class="label">Ret. IVA</div>
    <div class="valor" id="res-iva">-$80</div>
    <div class="valor-usd">8%</div>
  </div>
  
  <div class="resultado-item deduccion">
    <div class="label">IVA a pagar</div>
    <div class="valor" id="res-iva-pagar">-$80</div>
    <div class="valor-usd">8%</div>
  </div>
  
  <div class="resultado-item neutral">
    <div class="label">ISH</div>
    <div class="valor" id="res-ish">$0</div>
    <div class="valor-usd">Airbnb paga</div>
  </div>
</div>
```

## Preview Móvil

```
┌───────────────┬───────────────┐
│ Ingreso bruto │ Comisión      │
│ $1,000 MXN    │ -$30 MXN      │
│ ≈$50 USD      │ 3%            │
├───────────────┼───────────────┤
│ Ret. ISR      │ Ret. IVA      │
│ -$40 MXN      │ -$80 MXN      │
│ 4%            │ 8%            │
├───────────────┼───────────────┤
│ IVA a pagar   │ ISH           │
│ -$80 MXN      │ $0 MXN        │
│ 8%            │ Airbnb paga   │
└───────────────┴───────────────┘
```

## Checklist

- [ ] Crear CSS grid responsive
- [ ] Modificar HTML de resultados
- [ ] Agregar colores por tipo (ingreso/deducción)
- [ ] Probar en móvil 320px, 375px, 414px
- [ ] Verificar en desktop

---
Spec creado: 2026-01-19
Autor: C1 (Sleepy)
Prioridad: Media
Tiempo estimado: 30 minutos
Dependencias: ANFITRION-MX-UX-001
