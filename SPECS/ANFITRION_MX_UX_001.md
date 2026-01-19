# SPEC: ANFITRION-MX-UX-001
# UI Simplificada - Ganancia Neta Primero

## Objetivo
Reorganizar la jerarquía visual para mostrar la ganancia neta
como resultado principal, con desglose colapsable opcional.

## Problema Actual
- Usuario debe hacer ~2.5 pantallas de scroll
- Ganancia neta aparece hasta el final
- Score móvil: 5.8/10

## Solución
Mostrar ganancia neta prominente arriba, desglose oculto por default.

## Implementación

### 1. Nuevo Componente de Resultado Principal

```html
<!-- RESULTADO PRINCIPAL - Aparece primero -->
<div id="resultado-principal" class="resultado-hero hidden">
  <div class="ganancia-container">
    <span class="ganancia-label">💰 Tu ganancia neta</span>
    <div class="ganancia-monto">
      <span id="ganancia-neta-mxn">$0.00</span>
      <span class="moneda">MXN</span>
    </div>
    <div class="ganancia-usd">
      ≈ <span id="ganancia-neta-usd">$0.00</span> USD
    </div>
  </div>
  
  <button id="toggle-desglose" class="btn-desglose">
    ▼ Ver desglose completo
  </button>
</div>

<!-- DESGLOSE COLAPSABLE -->
<div id="desglose-container" class="desglose hidden collapsed">
  <!-- Aquí va el grid de resultados actual -->
</div>
```

### 2. CSS para Resultado Principal

```css
.resultado-hero {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border: 2px solid #10b981;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  margin: 1.5rem 0;
}

.ganancia-label {
  font-size: 1rem;
  color: #9ca3af;
  display: block;
  margin-bottom: 0.5rem;
}

.ganancia-monto {
  font-size: 2.5rem;
  font-weight: 700;
  color: #10b981;
}

.ganancia-monto .moneda {
  font-size: 1.25rem;
  color: #9ca3af;
  margin-left: 0.25rem;
}

.ganancia-usd {
  font-size: 1rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.btn-desglose {
  background: transparent;
  border: 1px solid #374151;
  color: #9ca3af;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 1.5rem;
  transition: all 0.2s;
}

.btn-desglose:hover {
  border-color: #10b981;
  color: #10b981;
}

/* Desglose colapsable */
.desglose {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
}

.desglose.expanded {
  max-height: 1000px;
}
```

### 3. JavaScript para Toggle

```javascript
function toggleDesglose() {
  const desglose = document.getElementById('desglose-container');
  const btn = document.getElementById('toggle-desglose');
  
  if (desglose.classList.contains('collapsed')) {
    desglose.classList.remove('collapsed');
    desglose.classList.add('expanded');
    btn.textContent = '▲ Ocultar desglose';
  } else {
    desglose.classList.remove('expanded');
    desglose.classList.add('collapsed');
    btn.textContent = '▼ Ver desglose completo';
  }
}

// Event listener
document.getElementById('toggle-desglose')
  .addEventListener('click', toggleDesglose);
```

### 4. Modificar función calcular()

```javascript
function calcular() {
  // ... cálculos existentes ...
  
  // Mostrar resultado principal PRIMERO
  document.getElementById('ganancia-neta-mxn').textContent = 
    formatMoney(gananciaNeta);
  document.getElementById('ganancia-neta-usd').textContent = 
    formatMoney(gananciaNeta / tipoCambio);
  
  document.getElementById('resultado-principal').classList.remove('hidden');
  
  // Scroll suave al resultado
  document.getElementById('resultado-principal')
    .scrollIntoView({ behavior: 'smooth', block: 'center' });
  
  // Llenar desglose (pero mantenerlo oculto)
  // ... código existente para llenar grid ...
}
```

## Flujo de Usuario

### Antes (actual)
1. Llena formulario
2. Click calcular
3. Scroll... scroll... scroll...
4. Ve ganancia neta al final

### Después (nuevo)
1. Llena formulario
2. Click calcular
3. VE GANANCIA NETA INMEDIATAMENTE
4. (Opcional) Click "Ver desglose" si quiere detalles

## Archivos a Modificar

1. **index.html** (o calculadora principal)
   - Agregar estructura HTML del resultado principal
   - Mover resultados actuales dentro de desglose-container

2. **styles.css**
   - Agregar estilos de resultado-hero
   - Agregar estilos de desglose colapsable

3. **script.js** (o JS principal)
   - Agregar función toggleDesglose
   - Modificar calcular() para mostrar resultado primero

## Checklist

- [ ] Crear HTML de resultado principal
- [ ] Crear CSS para ganancia-hero
- [ ] Implementar toggle de desglose
- [ ] Modificar función calcular()
- [ ] Probar en móvil
- [ ] Verificar scroll suave funciona

## Preview Móvil Esperado

```
┌─────────────────────────────────┐
│  [Formulario...]                │
│                                 │
│  [Calcular]                     │
├─────────────────────────────────┤
│  💰 Tu ganancia neta            │
│  ══════════════════════════     │
│  $770.00 MXN                    │
│  ≈ $38.50 USD                   │
│                                 │
│  [▼ Ver desglose completo]      │
└─────────────────────────────────┘
```

---
Spec creado: 2026-01-19
Autor: C1 (Sleepy)
Prioridad: Alta
Tiempo estimado: 1-2 horas
Dependencias: Ninguna
