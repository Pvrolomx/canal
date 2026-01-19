# SPEC: AIRBNB-CALC-FIX-001
# Corrección de Fórmulas de Retención - Calculadora Airbnb

## Contexto
La calculadora actual usa un valor hardcoded de 2.5% para impuestos.
Análisis de datos reales (CSV de pagos Airbnb México) reveló que
las retenciones reales son significativamente diferentes.

## Datos Verificados (CSV enero 2026)

### CON RFC (régimen actual de la cuenta)
| Concepto | Porcentaje | Base |
|----------|------------|------|
| Comisión Airbnb | 3% | Ingreso bruto |
| ISR retenido | 4% | Ingreso bruto |
| IVA retenido | 8% | Ingreso bruto |
| **Total deducciones** | **15%** | |

### SIN RFC (penalización)
| Concepto | Porcentaje | Base |
|----------|------------|------|
| Comisión Airbnb | 3% | Ingreso bruto |
| ISR retenido | 20% | Ingreso bruto |
| IVA retenido | 16% | Ingreso bruto |
| **Total deducciones** | **39%** | |

### ISH (Impuesto Sobre Hospedaje)
- Jalisco: 3%
- Airbnb lo cobra al huésped (pass-through)
- Anfitrión recibe y paga al estado
- Efecto neto: $0 (neutro para el anfitrión)

## Archivos a Modificar

### 1. src/calculo.ts (o equivalente)

Reemplazar constante hardcoded:
```typescript
// ANTES (incorrecto)
const tasa_impuesto = 0.025;

// DESPUÉS (correcto)
const TASAS_RETENCION = {
  CON_RFC: {
    comision: 0.03,
    isr: 0.04,
    iva: 0.08,
    total: 0.15
  },
  SIN_RFC: {
    comision: 0.03,
    isr: 0.20,
    iva: 0.16,
    total: 0.39
  }
};
```

### 2. Función de cálculo principal

```typescript
interface CalculoAirbnbInput {
  ingreso_bruto: number;
  tiene_rfc: boolean;
  gastos_deducibles?: number;
  tarifa_limpieza?: number;
}

interface CalculoAirbnbOutput {
  ingreso_bruto: number;
  comision_airbnb: number;
  retencion_isr: number;
  retencion_iva: number;
  total_retenciones: number;
  ingreso_neto: number;
  gastos: number;
  ganancia_neta: number;
  // Desglose para UI
  desglose: {
    concepto: string;
    monto: number;
    porcentaje: string;
  }[];
}

function calcularReservaAirbnb(input: CalculoAirbnbInput): CalculoAirbnbOutput {
  const tasas = input.tiene_rfc ? TASAS_RETENCION.CON_RFC : TASAS_RETENCION.SIN_RFC;
  
  const comision = input.ingreso_bruto * tasas.comision;
  const isr = input.ingreso_bruto * tasas.isr;
  const iva = input.ingreso_bruto * tasas.iva;
  const total_retenciones = comision + isr + iva;
  
  const ingreso_neto = input.ingreso_bruto - total_retenciones;
  const gastos = input.gastos_deducibles || 0;
  const ganancia_neta = ingreso_neto - gastos;
  
  return {
    ingreso_bruto: input.ingreso_bruto,
    comision_airbnb: round2(comision),
    retencion_isr: round2(isr),
    retencion_iva: round2(iva),
    total_retenciones: round2(total_retenciones),
    ingreso_neto: round2(ingreso_neto),
    gastos: gastos,
    ganancia_neta: round2(ganancia_neta),
    desglose: [
      { concepto: 'Comisión Airbnb', monto: -comision, porcentaje: '3%' },
      { concepto: 'Retención ISR', monto: -isr, porcentaje: input.tiene_rfc ? '4%' : '20%' },
      { concepto: 'Retención IVA', monto: -iva, porcentaje: input.tiene_rfc ? '8%' : '16%' },
    ]
  };
}

function round2(n: number): number {
  return Math.round(n * 100) / 100;
}
```

### 3. UI - Agregar selector de RFC

En el formulario HTML/React:
```html
<div class="form-group">
  <label>¿Tienes RFC registrado en Airbnb?</label>
  <select id="tiene-rfc" name="tiene_rfc">
    <option value="true" selected>Sí, tengo RFC</option>
    <option value="false">No tengo RFC</option>
  </select>
  <small class="help-text">
    Sin RFC las retenciones son significativamente mayores (39% vs 15%)
  </small>
</div>
```

### 4. UI - Mostrar desglose detallado

Agregar sección de resultados que muestre:
```html
<div class="desglose-retenciones">
  <h4>Desglose de Retenciones</h4>
  <table>
    <tr>
      <td>Ingreso bruto</td>
      <td class="monto">$1,000.00</td>
    </tr>
    <tr class="deduccion">
      <td>(-) Comisión Airbnb (3%)</td>
      <td class="monto negativo">-$30.00</td>
    </tr>
    <tr class="deduccion">
      <td>(-) Retención ISR (4%)</td>
      <td class="monto negativo">-$40.00</td>
    </tr>
    <tr class="deduccion">
      <td>(-) Retención IVA (8%)</td>
      <td class="monto negativo">-$80.00</td>
    </tr>
    <tr class="total">
      <td><strong>Tu pago neto</strong></td>
      <td class="monto"><strong>$850.00</strong></td>
    </tr>
  </table>
</div>
```

## Ejemplo de Cálculo

### Input
- Renta por noche: $150 USD
- Noches: 5
- Limpieza: $50 USD
- Total bruto: $800 USD
- Tiene RFC: Sí

### Output esperado (CON RFC)
| Concepto | Cálculo | Monto |
|----------|---------|-------|
| Ingreso bruto | | $800.00 |
| Comisión Airbnb | 800 × 3% | -$24.00 |
| Retención ISR | 800 × 4% | -$32.00 |
| Retención IVA | 800 × 8% | -$64.00 |
| **Total retenciones** | | **-$120.00** |
| **Pago neto** | | **$680.00** |

### Output esperado (SIN RFC)
| Concepto | Cálculo | Monto |
|----------|---------|-------|
| Ingreso bruto | | $800.00 |
| Comisión Airbnb | 800 × 3% | -$24.00 |
| Retención ISR | 800 × 20% | -$160.00 |
| Retención IVA | 800 × 16% | -$128.00 |
| **Total retenciones** | | **-$312.00** |
| **Pago neto** | | **$488.00** |

## Validación

Comparar resultados con CSV real:
- Reservación HMWK8R39MM (4 noches, Dana Raphaely)
- Ingresos brutos: $994.30
- Comisión: $29.83 (3.00% ✓)
- ISR: $39.77 (4.00% ✓)
- IVA: $79.55 (8.00% ✓)

## Notas Adicionales

1. **ISH no afecta al anfitrión**: Airbnb lo cobra al huésped y lo pasa
   como pass-through. El anfitrión lo recibe y lo paga al estado.
   Efecto neto = $0.

2. **IVA generado vs retenido**: Airbnb genera 16% de IVA pero solo
   retiene 8% (la mitad). El otro 8% es responsabilidad del anfitrión
   declararlo/pagarlo.

3. **Angel Host**: Si usas property manager, ellos manejan impuestos
   diferente (comisión ~15-18%, sin retenciones directas).

## Prioridad: ALTA

La calculadora actual subestima impuestos por ~5x, dando información
incorrecta a usuarios sobre sus ganancias reales.

---
Spec creado: 2026-01-18
Autor: C1 (Sleepy)
Basado en: Análisis de CSV real de pagos Airbnb México
