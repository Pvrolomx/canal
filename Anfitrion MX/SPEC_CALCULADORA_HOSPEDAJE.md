# SPEC: Calculadora de Hospedaje Airbnb/Vrbo

**Fecha:** 2026-01-20  
**Proyecto:** airbnb-calculadora  
**Repo:** github.com/Pvrolomx/airbnb-calculadora  
**URL Actual:** https://airbnb-calculadora.vercel.app  
**Respaldo:** /home/pvrolo/colmena/apps/airbnb-calculadora (RPI)

---

## 1. RESUMEN EJECUTIVO

Calculadora fiscal para hosts de plataformas de hospedaje (Airbnb, Vrbo, Booking). Calcula ganancia neta por reserva incluyendo:
- Comisiones de plataforma
- Retenciones IVA/ISR según régimen fiscal mexicano
- ISH (Impuesto Sobre Hospedaje) por 31 estados
- Conversión dual MXN/USD con tipo de cambio Banxico

### Ventaja Competitiva Única
**NINGÚN competidor (AirDNA, Airbtics, PriceLabs, Lodgify) tiene cálculo fiscal mexicano completo.**

---

## 2. ARQUITECTURA ACTUAL

```
/airbnb-calculadora
├── api/
│   └── fx-usd.js           # API Banxico para tipo de cambio
├── src/
│   ├── calculo.ts          # Motor de cálculo base
│   ├── calculo-plataformas.ts  # Extensión multi-plataforma
│   ├── plataformas.ts      # Constantes de comisiones
│   ├── server.ts           # Express API
│   └── __tests__/
│       └── calculo.test.ts # Tests Jest
├── public/
│   ├── index.html          # UI (64KB - todo inline)
│   ├── dual-currency.js    # Módulo de moneda
│   ├── credits.js          # Sistema de créditos
│   ├── pdf-generator.js    # Generador de reportes
│   └── script.js           # Script principal
└── vercel.json
```

---

## 3. LÓGICA FISCAL ACTUAL (CONSERVAR 100%)

### 3.1 Comisiones por Plataforma
```javascript
AIRBNB: 3%           // Split-fee
AIRBNB_SIMPLIFIED: 15.5%  // Host-only fee
VRBO: 8%
BOOKING: 15%
OTRA: 0%             // Reserva directa
```

### 3.2 Retenciones según Régimen Fiscal
| Régimen | ISR | IVA | Notas |
|---------|-----|-----|-------|
| SIN_RFC | 20% | 16% | Airbnb retiene todo |
| RESICO | 4% | 8% | Host paga 8% IVA adicional |
| ACT_EMPRESARIAL | 4% | 8% | Host paga 8% IVA adicional |

### 3.3 ISH por Estado (31 estados)
**Con convenio Airbnb (Airbnb paga, host NO):**
- CDMX 5%, JALISCO 3%, QROO 4%, YUCATAN 5%
- BCS 5%, EDOMEX 3%, OAXACA 3%, SINALOA 3%
- SONORA 2%, CHIAPAS 2%, PUEBLA 3%, GUERRERO 4%

**Sin convenio (Host paga):**
- NAYARIT 5%, BC 5%, NL 3%, QUERETARO 2.5%
- MICHOACAN 3%, COLIMA 2%, AGUASCALIENTES 3%
- (y 12 estados más)

### 3.4 Fórmula Principal
```
1. ingreso_bruto = tarifa_noche × noches + limpieza
2. comision_plataforma = ingreso_bruto × tasa_plataforma
3. retenciones = ISR + IVA (según régimen)
4. ingreso_neto = ingreso_bruto - comision - retenciones
5. gastos = limpieza_real + consumibles + otras_comisiones
6. ish_a_pagar = tiene_convenio ? 0 : impuesto_local
7. impuestos_adicionales = IVA_host + ish_a_pagar
8. ganancia_neta = ingreso_neto - gastos - impuestos_adicionales
```

---

## 4. PROBLEMAS IDENTIFICADOS

### 4.1 🔴 CRÍTICO: Módulo de Moneda
**Bug:** USD seleccionado muestra MXN primero

**Actual:**
```javascript
formatDualAmount(mxnAmount) {
  if (currentCurrency === 'USD') {
    return `$${usdFormatted} USD ... ≈ $${mxnFormatted} MXN`;
  }
}
```

**El problema:** El backend siempre devuelve MXN, pero la conversión/display está inconsistente.

### 4.2 🟡 MEDIO: UI Móvil
- Ganancia neta hasta el final (~2.5 pantallas scroll)
- Desglose no colapsable
- "Number of nights" en inglés

### 4.3 🟢 BAJO: Mejoras Futuras
- Impuesto saneamiento ambiental PV 2026 (80% UMA/noche)
- Nueva tarifa agua SEAPAL 2026
- Modo proyección anual

---

## 5. SPEC DE CAMBIOS

### 5.1 Módulo Currency (REHACER)

**Archivo:** `public/dual-currency.js`

**Funciones requeridas:**

```javascript
// 1. Fetch tipo de cambio con cache
async function fetchTipoCambio() {
  // Cache 1 hora en localStorage
  // Fallback: 20.00 MXN/USD
  // Fuente: /api/fx-usd (Banxico)
}

// 2. Conversión bidireccional
function convertir(monto, de, a) {
  // de: 'MXN' | 'USD'
  // a: 'MXN' | 'USD'
}

// 3. Formateo según selección del usuario
function formatearDual(monto, monedaOrigen) {
  // Si usuario seleccionó USD:
  //   → "$50.00 USD" (grande)
  //   → "≈ $1,000 MXN" (pequeño, gris)
  // Si usuario seleccionó MXN:
  //   → "$1,000 MXN" (grande)
  //   → "≈ $50.00 USD" (pequeño, gris)
}
```

**Lógica de conversión:**
1. Formulario captura en moneda seleccionada
2. Antes de calcular: convertir TODO a MXN
3. Motor calcula en MXN (no tocar)
4. Display: mostrar moneda seleccionada primero

### 5.2 Mejoras UI Móvil (OPCIONAL)

**Prioridad Alta:**
1. Corregir "Number of nights" → "Número de noches"
2. Ganancia neta PRIMERO después de calcular
3. Grid 2 columnas en móvil para resultados

**Prioridad Media:**
4. Desglose colapsable por default
5. Mover info contextual a modal

---

## 6. ARCHIVOS A MODIFICAR

| Archivo | Acción | Riesgo |
|---------|--------|--------|
| public/dual-currency.js | REESCRIBIR | Bajo |
| public/index.html | EDITAR (UI) | Medio |
| src/calculo.ts | NO TOCAR | N/A |
| api/fx-usd.js | CONSERVAR | N/A |

---

## 7. CRITERIOS DE ACEPTACIÓN

### 7.1 Módulo Currency
- [ ] USD seleccionado → Display muestra USD primero
- [ ] MXN seleccionado → Display muestra MXN primero
- [ ] Tipo de cambio se cachea 1 hora
- [ ] Fallback funciona si Banxico falla
- [ ] Indicador de TC visible en UI

### 7.2 Cálculos (NO deben cambiar)
- [ ] Caso RESICO Jalisco: mismos números
- [ ] Caso SIN_RFC Nayarit: mismos números
- [ ] Caso VRBO sin RFC: mismos números

### 7.3 UI
- [ ] Mobile: ganancia neta visible sin scroll excesivo
- [ ] Labels en español cuando MXN seleccionado
- [ ] Labels en inglés cuando USD seleccionado

---

## 8. ESTIMACIÓN

| Tarea | Tiempo |
|-------|--------|
| Reescribir dual-currency.js | 2 horas |
| Ajustes UI móvil | 1 hora |
| Testing manual | 30 min |
| Deploy y verificar | 30 min |
| **TOTAL** | **4 horas** |

---

## 9. NOTAS PARA EJECUCIÓN

1. **NO tocar `src/calculo.ts`** - La lógica fiscal está perfecta
2. **NO tocar `api/fx-usd.js`** - El API de Banxico funciona
3. **RESPALDAR `public/index.html`** antes de editar
4. Probar en móvil después de cada cambio
5. Verificar que los números no cambien

---

## APÉNDICE A: Casos de Prueba

### Caso 1: RESICO en Jalisco (con convenio)
```
Input: 
  tarifa: $2,000/noche, 3 noches, limpieza $500
  plataforma: Airbnb (3%)
  régimen: RESICO
  estado: Jalisco

Expected:
  Ingreso bruto: $6,500
  Comisión Airbnb: $195
  Retención ISR (4%): $260
  Retención IVA (8%): $520
  ISH: $0 (convenio)
  IVA adicional (8%): $520
```

### Caso 2: SIN_RFC en Nayarit (sin convenio)
```
Input:
  tarifa: $1,500/noche, 2 noches, limpieza $300
  plataforma: Airbnb
  régimen: SIN_RFC
  estado: Nayarit

Expected:
  Ingreso bruto: $3,300
  Comisión: $99
  Retención ISR (20%): $660
  Retención IVA (16%): $528
  ISH (5%): $165 (host paga)
```

---

**Autor:** OG (Claude)  
**Para revisión de:** Jefe  
**Ejecutor sugerido:** Sleepy/Zángano

---

## 10. HALLAZGO CRÍTICO POST-VERIFICACIÓN

### ⚠️ CÓDIGO REAL vs LEGACY

| Archivo | Status |
|---------|--------|
| public/index.html línea 1057 | **PRODUCCIÓN** |
| src/calculo.ts | ❌ LEGACY - NO USAR |
| src/calculo-plataformas.ts | ❌ LEGACY - NO USAR |

**El TypeScript está INCOMPLETO:**
- No tiene ISH por 31 estados
- No tiene convenio Airbnb
- No tiene lógica diferenciada VRBO/Booking

### Implicaciones para Ejecución

1. **IGNORAR** la carpeta src/ completamente
2. **TRABAJAR** solo con public/index.html y public/dual-currency.js
3. La lógica fiscal correcta está en el HTML inline

### Flujo Real en Producción

\\\
Usuario → public/index.html
         ↓
         form submit (línea 1514)
         ↓
         calcularReservaLocal() (línea 1057)
         ↓
         Resultado mostrado en DOM
         
API única: /api/fx-usd → Tipo de cambio Banxico
\\\

**Verificado:** 2026-01-20 por OG
