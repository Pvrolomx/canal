# Playwright Implementation Guide for Claude

## 1. Setup Inicial

### Instalación en Windows
```powershell
# Crear carpeta de trabajo
mkdir C:\playwright-tests
cd C:\playwright-tests

# Inicializar npm e instalar Playwright
npm init -y
npm install playwright

# Instalar browsers (Chrome/Chromium)
npx playwright install chromium
```

### Estructura básica de script
```javascript
const { chromium } = require("playwright");

async function main() {
  const browser = await chromium.launch({ headless: false }); // false para ver
  const page = await browser.newPage();
  await page.goto("https://sitio.com");
  // ... acciones
  await browser.close();
}

main().catch(console.error);
```

---

## 2. Errores Comunes y Soluciones

### ERROR 1: Selectores no encontrados
```
TimeoutError: locator('#miElemento') - Timeout 30000ms exceeded
```
**Causa:** ID incorrecto o elemento no existe

**Solución:** Inspeccionar HTML real con DevTools o grep en código fuente
```bash
ssh server "grep -i 'miElemento' ~/proyecto/archivo.html"
```

### ERROR 2: Elementos no interactuables
```
Element is not visible or not enabled
```
**Solución:** Agregar waits antes de interactuar
```javascript
await page.waitForTimeout(1000);
await page.waitForSelector('#elemento', { state: 'visible' });
```

### ERROR 3: Formularios con formato de dinero
```javascript
// MAL: El valor se pierde por formateo
await page.fill('#precio', '1500000');

// BIEN: Usar valor sin formato o esperar
await page.fill('#precio', '1500000');
await page.waitForTimeout(500); // Permitir formateo
```

### ERROR 4: Checkboxes
```javascript
// MAL: click puede fallar si ya está checked
await page.click('#miCheckbox');

// BIEN: usar check() que es idempotente
await page.check('#miCheckbox');
```

### ERROR 5: Extraer valores del DOM
```javascript
// MAL: textContent devuelve null si no existe
const valor = await page.textContent('#resultado');

// BIEN: usar evaluate con fallback
const valores = await page.evaluate(() => {
  const get = (id) => document.getElementById(id)?.textContent || '-';
  return {
    resultado: get('resultado'),
    total: get('total')
  };
});
```

---

## 3. Patrones Útiles

### Limpiar valores monetarios
```javascript
const isrNum = parseFloat(valores.isrFinal.replace(/[$,]/g, '')) || 0;
```

### Screenshots para debug
```javascript
await page.screenshot({ 
  path: 'C:\\playwright-tests\\debug.png', 
  fullPage: true 
});
```

### Múltiples casos en loop
```javascript
const casos = [
  { nombre: 'caso1', valor: 100 },
  { nombre: 'caso2', valor: 200 }
];

for (const c of casos) {
  const page = await context.newPage();
  // ... test
  await page.close();
}
```

### Comparación con tolerancia
```javascript
const diff = Math.abs(resultado - esperado);
const pctDiff = (diff / esperado * 100).toFixed(2);
const status = pctDiff < 1 ? '✅' : '❌';
```

---

## 4. Recomendaciones para Claude

1. **Siempre verificar IDs antes de usar:**
   - Usar grep/ssh para inspeccionar HTML real
   - Los IDs pueden cambiar entre versiones

2. **Agregar waits generosos:**
   - Después de navegación: 2000ms
   - Después de click en botón: 2000-3000ms
   - Entre inputs: 500ms

3. **Usar headless: false durante desarrollo:**
   - Permite ver qué está pasando
   - Cambiar a true para CI/CD

4. **Capturar screenshots en puntos clave:**
   - Antes de acciones críticas
   - Al final del test
   - Cuando hay error

5. **Estructura recomendada de test:**
```javascript
// 1. Setup
const browser = await chromium.launch({ headless: false });
const page = await browser.newPage();

// 2. Navegación
await page.goto(URL);
await page.waitForTimeout(2000);

// 3. Inputs (con waits)
await page.fill('#campo1', valor1);
await page.waitForTimeout(500);

// 4. Acción principal
await page.click('button:has-text("Calcular")');
await page.waitForTimeout(3000);

// 5. Extracción de resultados
const resultados = await page.evaluate(() => {...});

// 6. Validación
console.log('Resultado:', resultados);

// 7. Cleanup
await browser.close();
```

6. **Para sites con autenticación (como Nuvigant):**
   - Hacer registro manual primero
   - Guardar cookies si es posible
   - Usar contexto persistente

7. **Comparar con tolerancia, no igualdad exacta:**
   - Diferencias <1% son aceptables
   - Diferencias de redondeo INPC son normales

---

## 5. Playwright vs Chrome MCP

| Aspecto | Chrome MCP | Playwright |
|---------|------------|------------|
| Velocidad | ~15s/test | ~200ms/test |
| Tool calls | 6+ por test | 1 (script completo) |
| Setup | Ya instalado | Requiere npm install |
| Debug visual | Sí | Sí (headless:false) |
| CI/CD | No | Sí |
| Recomendado | Tests ad-hoc | Tests automatizados |

**Conclusión:** Usar Chrome MCP para exploración inicial, Playwright para suites de tests repetibles.

---

## 6. Ejemplo Completo: Test de Calculadora ISR

```javascript
const { chromium } = require("playwright");

const URL = "https://notaria-solutions.vercel.app/calculadora.html";

const casos = [
  { nombre: "Caso1", tipo: "terreno", fechaAdq: "2019-05-10", valorAdq: "1800000", 
    fechaEnaj: "2024-03-15", precioEnaj: "2500000", esperado: 9215 },
  { nombre: "Caso2", tipo: "mixto", fechaAdq: "2018-08-15", valorAdq: "2400000", 
    fechaEnaj: "2023-06-20", precioEnaj: "3200000", pctTerreno: 30, esperado: 28084 }
];

async function main() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const results = [];

  for (const c of casos) {
    const page = await context.newPage();
    await page.goto(URL);
    await page.waitForTimeout(2000);
    
    // Llenar formulario
    await page.fill("#fechaCompra", c.fechaAdq);
    await page.fill("#precioCompra", c.valorAdq);
    await page.fill("#fechaVenta", c.fechaEnaj);
    await page.fill("#precioVenta", c.precioEnaj);
    
    if (c.tipo === "terreno") {
      await page.click('text="Solo Terreno"');
    } else {
      await page.click('text="Terreno + Construcción"');
      await page.fill("#pctTerreno", String(c.pctTerreno));
      await page.fill("#pctConstruccion", String(100 - c.pctTerreno));
    }
    
    await page.waitForTimeout(500);
    await page.click('button:has-text("Calcular ISR")');
    await page.waitForTimeout(2000);
    
    // Extraer resultado
    const isrFinal = await page.textContent("#resIsrFinal");
    const isrNum = parseFloat(isrFinal.replace(/[$,]/g, ''));
    
    // Validar
    const diff = Math.abs(isrNum - c.esperado);
    const pctDiff = (diff / c.esperado * 100).toFixed(2);
    const status = pctDiff < 1 ? "✅" : "❌";
    
    results.push({ caso: c.nombre, resultado: isrNum, esperado: c.esperado, diff: pctDiff, status });
    await page.close();
  }
  
  // Mostrar resumen
  console.log("| Caso | Resultado | Esperado | Diff | Status |");
  for (const r of results) {
    console.log(`| ${r.caso} | $${r.resultado} | $${r.esperado} | ${r.diff}% | ${r.status} |`);
  }
  
  await browser.close();
}

main().catch(console.error);
```

---

*Documentación generada por C_AMX - Enero 2026*
