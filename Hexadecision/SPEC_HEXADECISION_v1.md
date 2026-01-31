# HEXADECISION - SPEC v1.0
## I-Ching Algorítmico con Análisis de Cambio

---

## 1. VISIÓN DEL PRODUCTO

**Tagline:** "El oráculo que puedes verificar"

**Concepto:** App de consulta I-Ching donde los hexagramas se generan mediante algoritmos matemáticos deterministas (no azar). El usuario puede reproducir y verificar cualquier lectura.

**Diferenciador:** Mientras otras apps de I-Ching usan RNG (random), Hexadecision usa hashes criptográficos. Misma pregunta + mismo momento = misma respuesta. Siempre.

---

## 2. ARQUITECTURA TÉCNICA

### Stack Propuesto
- **Frontend:** HTML/CSS/JS vanilla (como Astro4) o React
- **Backend:** Vercel Serverless (Node.js)
- **LLM:** Claude API (para interpretaciones contextualizadas)
- **Base de datos:** JSON estático (64 hexagramas + significados)
- **Dominio:** hexadecision.app o hexadecision.duendes.app

### Flujo de Datos
```
[Usuario] → Pregunta + Timestamp
    ↓
[Hash SHA-256] → Número 0-63
    ↓
[Lookup Table] → Hexagrama Primario
    ↓
[XOR con segundo hash] → Hexagrama Transformado
    ↓
[Claude API] → Interpretación contextualizada
    ↓
[UI] → Visualización + Animación de cambio
```

---

## 3. ALGORITMO CENTRAL

### 3.1 Generación de Hexagrama
```javascript
const crypto = require('crypto');

function generarHexagrama(pregunta, seed = 0) {
  const texto = `${pregunta}${seed}`;
  const hash = crypto.createHash('sha256').update(texto).digest('hex');
  const numero = parseInt(hash.slice(0, 8), 16) % 64;
  return numero;
}
```

### 3.2 Cálculo de Transformación
```javascript
function calcularLectura(pregunta) {
  const primario = generarHexagrama(pregunta, 0);
  const secundario = generarHexagrama(pregunta, 1);
  
  const cambio = primario ^ secundario;  // XOR
  const lineasMoviles = (cambio).toString(2).split('1').length - 1;
  const intensidadCambio = Math.round((lineasMoviles / 6) * 100);
  
  return {
    hexagramaPrimario: primario,
    hexagramaSecundario: secundario,
    binarioPrimario: primario.toString(2).padStart(6, '0'),
    binarioSecundario: secundario.toString(2).padStart(6, '0'),
    lineasMoviles,
    intensidadCambio,
    lineasQueCAMbian: identificarLineasMoviles(cambio)
  };
}

function identificarLineasMoviles(cambio) {
  const binario = cambio.toString(2).padStart(6, '0');
  return binario.split('').map((bit, i) => bit === '1' ? i + 1 : null).filter(Boolean);
}
```

### 3.3 Propiedades Matemáticas
| Propiedad | Fórmula | Resultado |
|-----------|---------|-----------|
| Total hexagramas | 2^6 | 64 |
| Bits por hexagrama | log2(64) | 6 |
| Líneas móviles máx | popcount(63) | 6 |
| Distancia Hamming máx | 6 | 100% cambio |

---

## 4. BASE DE DATOS DE HEXAGRAMAS

### Estructura JSON
```json
{
  "hexagramas": [
    {
      "numero": 1,
      "nombreChino": "乾",
      "nombreEspanol": "El Cielo / Lo Creativo",
      "nombreIngles": "The Creative",
      "binario": "111111",
      "trigramaInferior": "Cielo",
      "trigramaSuperior": "Cielo",
      "palabraClave": "Fuerza creativa, iniciativa",
      "imagen": "El movimiento del cielo es poderoso",
      "juicio": "Lo Creativo obra elevado éxito",
      "lineas": [
        {"posicion": 1, "texto": "Dragón oculto. No actúes."},
        {"posicion": 2, "texto": "Dragón en el campo. Ventajoso ver al gran hombre."},
        // ... 6 líneas
      ],
      "relacionados": [44, 33, 12, 25, 6, 10]  // hexagramas que resultan de líneas móviles
    }
    // ... 64 hexagramas
  ]
}
```

---

## 5. INTERFAZ DE USUARIO

### 5.1 Pantalla Principal
```
┌─────────────────────────────────────┐
│          HEXADECISION               │
│     "El oráculo que verificas"      │
├─────────────────────────────────────┤
│                                     │
│   ┌─────────────────────────────┐   │
│   │ ¿Cuál es tu pregunta?       │   │
│   │ ___________________________ │   │
│   └─────────────────────────────┘   │
│                                     │
│         [ CONSULTAR ]               │
│                                     │
└─────────────────────────────────────┘
```

### 5.2 Pantalla de Resultado
```
┌─────────────────────────────────────┐
│  HEXAGRAMA ACTUAL    →   HEXAGRAMA  │
│      ════════            FUTURO     │
│      ══ ══ ══            ════════   │
│      ════════      →     ══    ══   │
│      ══ ══ ══            ════════   │
│      ════════            ══    ══   │
│      ══ ══ ══            ════════   │
│                                     │
│  #47 El Agotamiento → #6 El Conflicto
│                                     │
│  Intensidad de cambio: ████░░ 67%   │
│  Líneas móviles: 2, 4, 5            │
│                                     │
├─────────────────────────────────────┤
│  INTERPRETACIÓN:                    │
│  [Claude genera texto contextual    │
│   basado en pregunta + hexagramas]  │
│                                     │
├─────────────────────────────────────┤
│  🔍 Ver matemáticas  📤 Compartir   │
└─────────────────────────────────────┘
```

### 5.3 Panel "Ver Matemáticas"
```
┌─────────────────────────────────────┐
│  VERIFICACIÓN MATEMÁTICA            │
├─────────────────────────────────────┤
│  Pregunta: "¿Debo aceptar el trabajo?"
│  Hash SHA-256: a7f3e2...            │
│  Primeros 8 chars: a7f3e2b1         │
│  Decimal: 2818212529                │
│  mod 64 = 47                        │
│                                     │
│  Hexagrama #47 = 101111 binario     │
│                                     │
│  Seed 1 hash: b2c4d1...             │
│  mod 64 = 6                         │
│  XOR: 101111 ^ 000110 = 101001      │
│                                     │
│  [Copiar para verificar]            │
└─────────────────────────────────────┘
```

---

## 6. API ENDPOINTS

### POST /api/consulta
**Request:**
```json
{
  "pregunta": "¿Debo aceptar el trabajo?",
  "idioma": "es"
}
```

**Response:**
```json
{
  "hexagramaPrimario": {
    "numero": 47,
    "nombre": "El Agotamiento",
    "binario": "101111"
  },
  "hexagramaSecundario": {
    "numero": 6,
    "nombre": "El Conflicto",
    "binario": "101001"
  },
  "lineasMoviles": [2, 4, 5],
  "intensidadCambio": 67,
  "interpretacion": "Claude genera texto...",
  "verificacion": {
    "hashPrimario": "a7f3e2b1...",
    "hashSecundario": "b2c4d1e5...",
    "reproducible": true
  }
}
```

### GET /api/hexagrama/:numero
Retorna datos completos de un hexagrama específico.

---

## 7. PROMPT PARA CLAUDE (Interpretaciones)

```
Eres un sabio intérprete del I-Ching que combina la tradición milenaria con claridad moderna.

CONTEXTO:
- Pregunta del usuario: {pregunta}
- Hexagrama primario: #{numero} - {nombre}
- Hexagrama de transformación: #{numero2} - {nombre2}
- Líneas móviles: {lineas}
- Intensidad de cambio: {intensidad}%

INSTRUCCIONES:
1. Interpreta el hexagrama primario en relación directa con la pregunta
2. Explica qué significan las líneas móviles específicas
3. Describe la transformación hacia el segundo hexagrama
4. Concluye con una recomendación práctica y concreta
5. Usa un tono sabio pero accesible, no místico ni vago
6. Máximo 200 palabras

Si la pregunta es incoherente o son solo caracteres random, responde:
"No entendí tu pregunta. ¿Puedes reformularla de forma más clara?"
```

---

## 8. MONETIZACIÓN

### Modelo Freemium
| Tier | Precio | Límites |
|------|--------|---------|
| Free | $0 | 3 consultas/día, interpretación básica |
| Pro | $4.99/mes | Ilimitado, interpretación profunda, historial |
| Lifetime | $29.99 | Todo Pro para siempre |

### Código de Donación (como Astro4)
- Donación mínima desbloquea 30 consultas adicionales
- Código generado: 8 caracteres alfanuméricos

---

## 9. MVP - FASE 1 (1 semana)

### Entregables
1. Landing page con input de pregunta
2. Algoritmo de generación funcionando
3. JSON con 64 hexagramas (datos básicos)
4. Endpoint /api/consulta con Claude
5. UI de resultado con hexagrama visual
6. Panel de verificación matemática
7. Deploy en Vercel

### NO incluir en MVP
- Historial de consultas
- Sistema de pagos
- Múltiples idiomas
- Animaciones elaboradas
- PWA/offline

---

## 10. DIFERENCIACIÓN VS COMPETENCIA

| Feature | Hexadecision | Apps típicas I-Ching |
|---------|--------------|---------------------|
| Generación | Determinista (hash) | Random |
| Verificable | ✅ Sí | ❌ No |
| Reproducible | ✅ Misma pregunta = mismo resultado | ❌ Siempre diferente |
| Interpretación | Claude contextual | Texto estático |
| Transparencia | Muestra las matemáticas | Caja negra |

---

## 11. RECURSOS NECESARIOS

### Datos
- [ ] JSON de 64 hexagramas con traducciones ES/EN
- [ ] Significados de las 6 líneas para cada hexagrama
- [ ] Relaciones entre hexagramas (trigramas)

### Assets
- [ ] Iconos de líneas (yin/yang)
- [ ] Fuente para caracteres chinos
- [ ] Favicon

### Cuentas
- [ ] Repo GitHub (Pvrolomx/hexadecision)
- [ ] Proyecto Vercel
- [ ] Subdominio o dominio

---

*Spec creado: 2026-01-31*
*Versión: 1.0*
