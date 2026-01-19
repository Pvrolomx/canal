# SPEC: COLMENA-TESTING-FRAMEWORK-001
# Framework de Testing Estándar para Proteger Lógica Crítica

## Objetivo
Establecer un sistema de tests automatizados que proteja la lógica
crítica de TODAS las apps de Colmena contra regresiones accidentales.

## Problema
Cambios en módulos secundarios (UI, estilos, utils) rompen
funcionalidad crítica (fórmulas, cálculos, consultas) sin que
nadie se de cuenta hasta que un usuario lo reporta.

## Solución
Tests automáticos que corren EN CADA PUSH, bloqueando merges
si la lógica crítica se ve afectada.

---

## Estructura de Archivos Estándar

```
/proyecto
  /src
    /core              ← LOGICA CRITICA (protegida)
      formulas.js
      calculos.js
      consultas.js
    /ui                ← Cambios libres
    /api               ← Cambios libres
  /tests
    /unit              ← Tests de funciones
    /snapshots         ← Fotos de resultados
    /e2e               ← Tests de usuario
    casos-reales.json  ← Datos verificados
  .github
    /workflows
      test.yml         ← CI/CD automático
```

---

## 1. Tests Unitarios

Verifican que las funciones devuelvan resultados correctos.

### Template: tests/unit/core.test.js

```javascript
import { describe, test, expect } from 'vitest';
import { calcular, obtenerTasa } from '../../src/core/formulas';

describe('Funciones Core', () => {
  
  // Test básico
  test('calcular caso simple', () => {
    const resultado = calcular({ monto: 1000 });
    expect(resultado.total).toBe(770);
  });
  
  // Test con parámetros
  test('calcular con opciones', () => {
    const resultado = calcular({ 
      monto: 1000, 
      regimen: 'resico' 
    });
    expect(resultado.impuesto).toBe(230);
  });
  
  // Test de edge cases
  test('calcular monto cero', () => {
    const resultado = calcular({ monto: 0 });
    expect(resultado.total).toBe(0);
  });
  
  // Test de tasas
  test('tasa ISR con RFC', () => {
    expect(obtenerTasa('isr', { rfc: true })).toBe(0.04);
  });
  
  test('tasa ISR sin RFC', () => {
    expect(obtenerTasa('isr', { rfc: false })).toBe(0.20);
  });
});
```

---

## 2. Tests con Casos Reales

Usar datos REALES verificados como fuente de verdad.

### Template: tests/casos-reales.json

```json
{
  "version": "1.0.0",
  "casos": [
    {
      "id": "airbnb-dana-raphaely",
      "descripcion": "Reservación 4 noches Dana Raphaely",
      "fuente": "CSV Airbnb enero 2026",
      "input": {
        "bruto": 994.30,
        "noches": 4,
        "plataforma": "airbnb",
        "regimen": "conRFC",
        "estado": "jalisco"
      },
      "expected": {
        "comision": 29.83,
        "isrRetenido": 39.77,
        "ivaRetenido": 79.55,
        "gananciaNeta": 845.15
      }
    },
    {
      "id": "isr-caso-icon",
      "descripcion": "Caso Icon vs Careaga",
      "fuente": "Dictamen notaría",
      "input": {
        "precioVenta": 5500000,
        "fechaAdquisicion": "2018-03-15",
        "costoAdquisicion": 3200000
      },
      "expected": {
        "isrFederal": 234567,
        "isrEstatal": 45678
      }
    }
  ]
}
```

### Template: tests/unit/casos-reales.test.js

```javascript
import { describe, test, expect } from 'vitest';
import { calcular } from '../../src/core/formulas';
import casosReales from '../casos-reales.json';

describe('Casos Reales Verificados', () => {
  
  casosReales.casos.forEach(caso => {
    test(caso.descripcion, () => {
      const resultado = calcular(caso.input);
      
      Object.keys(caso.expected).forEach(key => {
        expect(resultado[key]).toBeCloseTo(caso.expected[key], 2);
      });
    });
  });
  
});
```

---

## 3. Tests Snapshot

Detectan CUALQUIER cambio en los resultados.

### Template: tests/snapshots/formulas.test.js

```javascript
import { describe, test, expect } from 'vitest';
import { calcular } from '../../src/core/formulas';

describe('Snapshots de Resultados', () => {
  
  test('snapshot caso estándar', () => {
    const resultado = calcular({
      monto: 1000,
      plataforma: 'airbnb',
      regimen: 'resico'
    });
    
    expect(resultado).toMatchSnapshot();
  });
  
  test('snapshot caso complejo', () => {
    const resultado = calcular({
      monto: 50000,
      plataforma: 'booking',
      regimen: 'actividad_empresarial',
      gastos: 5000
    });
    
    expect(resultado).toMatchSnapshot();
  });
  
});
```

**Nota:** La primera vez genera el snapshot.
Después, si el resultado cambia, el test FALLA.
Si el cambio es intencional: `npm test -- -u` actualiza snapshots.

---

## 4. Tests E2E (End-to-End)

Simulan usuario real interactuando con la app.

### Template: tests/e2e/calculadora.spec.js

```javascript
import { test, expect } from '@playwright/test';

test.describe('Calculadora', () => {
  
  test('usuario calcula reserva básica', async ({ page }) => {
    await page.goto('/');
    
    // Llenar formulario
    await page.fill('#precio', '1000');
    await page.fill('#noches', '5');
    await page.selectOption('#plataforma', 'airbnb');
    
    // Calcular
    await page.click('#btn-calcular');
    
    // Verificar resultado
    const ganancia = await page.textContent('#ganancia-neta');
    expect(ganancia).toContain('770');
  });
  
  test('PDF se genera correctamente', async ({ page }) => {
    await page.goto('/');
    await page.fill('#precio', '1000');
    await page.click('#btn-calcular');
    
    // Verificar botón PDF existe
    const btnPDF = page.locator('#btn-pdf');
    await expect(btnPDF).toBeVisible();
  });
  
});
```

---

## 5. GitHub Actions - CI/CD

### Template: .github/workflows/test.yml

```yaml
name: Proteger Lógica Crítica

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout código
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Instalar dependencias
        run: npm ci
      
      - name: Correr tests unitarios
        run: npm run test:unit
      
      - name: Correr tests de casos reales
        run: npm run test:casos
      
      - name: Verificar snapshots
        run: npm run test:snapshots
      
      - name: Tests E2E (opcional)
        run: npm run test:e2e
        continue-on-error: true

  # BLOQUEAR SI TESTS FALLAN
  check:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Tests pasaron
        run: echo "✅ Lógica crítica protegida"
```

---

## 6. Configuración package.json

```json
{
  "scripts": {
    "test": "vitest",
    "test:unit": "vitest run tests/unit",
    "test:casos": "vitest run tests/unit/casos-reales.test.js",
    "test:snapshots": "vitest run tests/snapshots",
    "test:e2e": "playwright test",
    "test:watch": "vitest watch",
    "test:coverage": "vitest run --coverage"
  },
  "devDependencies": {
    "vitest": "^1.0.0",
    "@playwright/test": "^1.40.0"
  }
}
```

---

## 7. Branch Protection en GitHub

Settings → Branches → Add rule:

- Branch name pattern: `main`
- ☑️ Require a pull request before merging
- ☑️ Require status checks to pass
  - Select: "test" (del workflow)
- ☑️ Require branches to be up to date

**Resultado:** No se puede hacer push directo a main,
y los tests DEBEN pasar para mergear.

---

## Checklist de Implementación por App

### Setup Inicial (una vez)
- [ ] Instalar vitest: `npm install -D vitest`
- [ ] Crear estructura de carpetas tests/
- [ ] Agregar scripts a package.json
- [ ] Crear .github/workflows/test.yml
- [ ] Activar branch protection en GitHub

### Por Módulo Crítico
- [ ] Identificar funciones críticas
- [ ] Crear 3-5 tests unitarios
- [ ] Agregar 2-3 casos reales verificados
- [ ] Crear 1-2 snapshots

### Mantenimiento
- [ ] Agregar test por cada bug encontrado
- [ ] Actualizar casos-reales.json cuando hay datos nuevos
- [ ] Revisar snapshots cuando hay cambios intencionales

---

## Apps a Implementar

| App | Módulo Crítico | Prioridad |
|-----|---------------|-----------|
| airbnb-calculadora | calculo-plataformas.ts | Alta |
| notaria-solutions | formulas ISR | Alta |
| astro3 | módulo consulta | Alta |
| legal-solutions | cálculos pasos | Media |
| RES | matching algorithm | Media |

---

## Tiempo Estimado

| Tarea | Tiempo |
|-------|--------|
| Setup inicial (primera app) | 2 horas |
| Setup apps adicionales | 30 min c/u |
| Tests por módulo crítico | 1 hora |
| Mantenimiento mensual | 30 min |

---

**Spec creado:** 2026-01-19
**Autor:** C1 (Sleepy)
**Prioridad:** Alta
**Aplica a:** Todas las apps de Colmena
