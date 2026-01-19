# SPEC: ANFITRION-MX-UX-004
# Nota Informativa - Saneamiento Ambiental PV 2026

## Objetivo
Informar a usuarios de Puerto Vallarta sobre el posible nuevo impuesto
de saneamiento ambiental, SIN incluirlo en el cálculo hasta confirmación.

## Contexto Legal
- Art. 80 ter Ley de Ingresos Puerto Vallarta 2026
- 80% de la UMA por noche de ocupación
- Aplica a rentas en plataformas digitales
- PENDIENTE DE CONFIRMACIÓN DE APLICACIÓN

## Implementación

### 1. Componente de Nota Informativa

```html
<!-- Mostrar solo si estado = Jalisco -->
<div id="nota-saneamiento" class="nota-info hidden">
  <div class="nota-header">
    <span class="nota-icon">⚠️</span>
    <span class="nota-titulo">Aviso: Puerto Vallarta 2026</span>
  </div>
  <div class="nota-contenido">
    <p>
      La Ley de Ingresos de Puerto Vallarta 2026 contempla un 
      impuesto de saneamiento ambiental (~$90 MXN/noche) que 
      podría aplicar a rentas vacacionales en plataformas digitales.
    </p>
    <p class="nota-disclaimer">
      <strong>Pendiente de confirmación.</strong> 
      Este impuesto aún no se incluye en el cálculo.
    </p>
    <a href="#" class="nota-link" onclick="mostrarInfoSaneamiento()">
      Más información →
    </a>
  </div>
</div>
```

### 2. CSS para Nota

```css
.nota-info {
  background: #1e293b;
  border-left: 4px solid #f59e0b;
  border-radius: 0 8px 8px 0;
  padding: 1rem;
  margin: 1rem 0;
}

.nota-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.nota-icon {
  font-size: 1.25rem;
}

.nota-titulo {
  font-weight: 600;
  color: #f59e0b;
}

.nota-contenido p {
  font-size: 0.875rem;
  color: #9ca3af;
  margin: 0.5rem 0;
}

.nota-disclaimer {
  color: #6b7280;
  font-style: italic;
}

.nota-link {
  color: #10b981;
  font-size: 0.875rem;
  text-decoration: none;
}

.nota-link:hover {
  text-decoration: underline;
}
```

### 3. JavaScript - Mostrar Condicionalmente

```javascript
function actualizarNotaSaneamiento() {
  const estado = document.getElementById('ubicacion').value;
  const nota = document.getElementById('nota-saneamiento');
  
  // Mostrar solo para Jalisco
  if (estado === 'jalisco') {
    nota.classList.remove('hidden');
  } else {
    nota.classList.add('hidden');
  }
}

// Listener en cambio de ubicación
document.getElementById('ubicacion')
  .addEventListener('change', actualizarNotaSaneamiento);

// Modal con más información
function mostrarInfoSaneamiento() {
  alert(
    'Impuesto de Saneamiento Ambiental - Puerto Vallarta 2026\n\n' +
    '• Base legal: Art. 80 ter Ley de Ingresos PV 2026\n' +
    '• Monto: 80% de la UMA por noche (~$90 MXN)\n' +
    '• Aplica a: Plataformas digitales (Airbnb, Vrbo, etc.)\n\n' +
    'Este impuesto está publicado pero su aplicación está pendiente de confirmación. ' +
    'Recomendamos consultar con un contador para mayor información.'
  );
}
```

## Flujo de Usuario

1. Usuario selecciona "Jalisco" como ubicación
2. Aparece nota informativa en color amarillo/naranja
3. Nota explica el posible nuevo impuesto
4. Claramente indica "pendiente de confirmación"
5. Link a más información (modal o página externa)

## NO Incluir en Cálculo

Esta nota es SOLO informativa. El impuesto NO se suma
al cálculo hasta que se confirme su aplicación.

## Checklist

- [ ] Crear HTML de nota informativa
- [ ] Crear CSS con estilo de advertencia
- [ ] Implementar lógica condicional (solo Jalisco)
- [ ] Crear modal con más información
- [ ] Probar flujo completo
- [ ] Verificar que NO afecta cálculos

---
Spec creado: 2026-01-19
Autor: C1 (Sleepy)
Prioridad: Baja
Tiempo estimado: 30 minutos
Dependencias: Ninguna
Nota: Solo informativo, no afecta cálculos
