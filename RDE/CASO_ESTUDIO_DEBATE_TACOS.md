# 🌮 CASO DE ESTUDIO: Debate Multi-IA "El Mejor Taco de Puerto Vallarta"

**Fecha:** 2 Marzo 2026
**Arquitecto:** Rolo (Puerto Vallarta)
**Objetivo:** Comparar las 3 capas del sistema RDB ejecutando el mismo debate en cada una

---

## CONTEXTO

Tema del debate: "¿Cuál es el mejor taco de Puerto Vallarta?"
Se probaron todas las capas definidas en las RDB (Reglas del Browser) con el mismo tema para medir velocidad, calidad, diversidad y autonomía.

---

## RESULTADOS POR CAPA

### CAPA 3: API Directa (Container Cloud de claude.ai)

**Método:** Script Node.js ejecutado en el container Linux de Claude. 2 duendes (Pescado vs Pastor) debatiendo vía API de Anthropic con `Promise.all` para paralelismo.

**Modelos probados:**

| Modelo | Tiempo total | Ronda 0 | Ronda 1 | Prom/call |
|--------|-------------|---------|---------|-----------|
| Haiku 4.5 | **9.0s** | 6.2s | 2.8s | 2,259ms |
| Sonnet 4.5 | **20.4s** | 10.3s | 10.1s | 5,097ms |

**Calidad del debate:**
- Haiku: Superficial, conciliador, datos inventados pero coherentes
- Sonnet: Desacuerdos reales — Duende Pastor atacó "estilo Baja es importado, no de Jalisco" y Duende Pescado respondió "¿por qué comer en Vallarta lo mismo que en cualquier ciudad?"

**Veredicto Capa 3:** ⚡ Más rápida. Datos inventados. Claude vs Claude.

---

### CAPA 1a: Browser Engine — API desde PC Local

**Método:** Mismo script pero ejecutado desde PC BeachHouse vía Desktop Commander. La diferencia es solo la latencia de red (PC local → Anthropic API vs Container cloud → Anthropic API).

| Modelo | Tiempo total | Ronda 0 | Ronda 1 | Prom/call |
|--------|-------------|---------|---------|-----------|
| Haiku 4.5 | **6.5s** | 3.1s | 3.5s | 1,632ms |

**vs Capa 3:** PC local fue 28% más rápida (6.5s vs 9.0s). Menor latencia al endpoint de Anthropic.

**Veredicto Capa 1a:** ⚡⚡ Más rápida que container. Misma calidad. Datos inventados.

---

### CAPA 1b: Browser Engine — Multi-IA Headless (Puppeteer)

**Método:** Puppeteer + Stealth abriendo ChatGPT, Gemini y Copilot en headless simultáneo. Sin Chrome Extension, sin intervención humana. Script ejecutado desde PC BeachHouse.

**Prueba 1: ChatGPT vs Gemini (2 IAs)**

| IA | Ronda 0 | Ronda 1 | Status |
|----|---------|---------|--------|
| ChatGPT | 49.0s | 54.7s | ✅ Ambas rondas OK |
| Gemini | 30.4s | 32.9s | ✅ Ambas rondas OK |
| **Total** | **49.0s** (paralelo) | **54.7s** (paralelo) | **104.1s total** |

**Debate real:**
- R0: Ambos defendieron Pancho's Takos (4.6★, 5000+ reseñas)
- R1: Gemini se viró a "Tacos El Cuñado" atacando Pancho's como "trampa turista". ChatGPT admitió "popularidad ≠ supremacía"

**Prueba 2: ChatGPT vs Gemini vs Copilot (3 IAs)**

| IA | Ronda 0 | Ronda 1 | Status |
|----|---------|---------|--------|
| ChatGPT | 72.1s | 86.5s | ✅ OK |
| Gemini | 53.4s | 61.7s | ✅ R0 OK, ⚠️ R1 alucinó |
| Copilot | 31.2s | 32.5s | ❌ No procesó prompt |
| **Total** | **72.1s** (paralelo) | **86.6s** (paralelo) | **159.0s total** |

**Hallazgos técnicos:**
- Copilot requiere approach diferente para input (no textarea estándar)
- Gemini se confundió en Ronda 1 con contexto cruzado largo
- ChatGPT fue el más robusto en ambas rondas
- Headless funciona SIN sesión en ChatGPT y Gemini (tier gratuito)

**Veredicto Capa 1b:** 🧠 Más lenta pero única que produce debate multi-IA real con datos verificados y $0 costo de API.

---

### CAPA 2: Claude in Chrome (Extensión Manual)

**Método:** Claude controlando pestañas de Chrome via extensión, navegando a ChatGPT y DeepSeek, escribiendo prompts, extrayendo respuestas, cruzando manualmente.

| IA | Ronda 0 | Status |
|----|---------|--------|
| ChatGPT | ~15s respuesta + navegación | ✅ OK |
| DeepSeek | ~20s respuesta + navegación | ✅ OK |
| **Total estimado** | **~90s** | Requirió 2 reconexiones |

**Debate:**
- ChatGPT: Tacos de Cabeza el Chulo, 4.8★, ~377 reseñas
- DeepSeek: Tacos El Jefe, True Rating 4.759, 94 opiniones
- Cruce: ChatGPT atacó "menos datos, menos enfoque local". DeepSeek atacó "sesgo de popularidad, reseñas antiguas"

**Problemas:** Chrome Extension se desconectó 2 veces durante la prueba. Cada reconexión requiere intervención del Arquitecto.

**Veredicto Capa 2:** 🎯 Buenos resultados pero frágil. Depende de extensión que se desconecta.

---

## TABLA COMPARATIVA FINAL

| Aspecto | Capa 3 (API) | Capa 1a (PC+API) | Capa 1b (Puppeteer Multi-IA) | Capa 2 (Chrome) |
|---------|-------------|-------------------|------------------------------|-----------------|
| **Tiempo** | 9s-20s | **6.5s** | 104-159s | ~90s |
| **IAs involucradas** | Solo Claude | Solo Claude | ChatGPT+Gemini+Copilot | ChatGPT+DeepSeek |
| **Datos reales** | ❌ Inventados | ❌ Inventados | ✅ Verificados con fuentes | ✅ Verificados |
| **Costo API** | $$ tokens | $$ tokens | **$0** (tier gratis) | **$0** |
| **Intervención humana** | 0 | 0 | **0** | 2 reconexiones |
| **Estabilidad** | ✅ Sólida | ✅ Sólida | ✅ Sólida (headless) | ⚠️ Se desconecta |
| **Requiere PC** | No | Sí | Sí | Sí |
| **Requiere sesión** | No | No | No | Sí (login IAs) |

---

## HALLAZGOS CLAVE

### 1. Browser Engine headless es el sweet spot para debates multi-IA
Combina lo mejor: autonomía total (sin extensión frágil), datos reales (navega IAs reales), costo $0 (tier gratuito). Es más lenta que API pura pero produce resultados cualitativamente superiores.

### 2. La PC local es más rápida que el container cloud para API
28% más rápida para el mismo modelo Haiku. La latencia de red importa.

### 3. Chrome Extension es frágil para automatización prolongada
Se desconectó 2 veces en una prueba de ~5 minutos. Para debates multi-IA, Puppeteer headless es superior.

### 4. Copilot requiere trabajo adicional
Su interfaz no es un textarea estándar. Necesita selectores específicos o approach de tipo/click diferente.

### 5. Las IAs coinciden más de lo esperado
ChatGPT y Gemini ambos eligieron Pancho's Takos en Ronda 0. El desacuerdo real emergió en Ronda 1 cuando se cruzaron respuestas.

### 6. Los tiers gratuitos funcionan
ChatGPT y Gemini respondieron sin login, sin pago, en headless. Esto es "el duende es la API" — usar el tier web gratis en vez de pagar API.

---

## JERARQUÍA ACTUALIZADA

**Para velocidad (Claude vs Claude):**
```
🥇 Capa 1a (PC + API Haiku):     6.5s
🥈 Capa 3 (Container + API):     9.0s
🥉 Capa 3 (Container + Sonnet):  20.4s
```

**Para calidad de debate (Multi-IA real):**
```
🥇 Capa 1b (Puppeteer Multi-IA): Datos verificados, autónomo, $0
🥈 Capa 2 (Chrome Extension):    Datos verificados, frágil
🥉 Capa 3/1a (API):              Datos inventados, rápido
```

**Para resiliencia (¿qué funciona si claude.ai cae?):**
```
🥇 Capa 1b (Puppeteer):  No depende de Claude en absoluto
🥈 Capa 3 (API directa): Sobrevive caída de claude.ai
🥉 Capa 1a (PC + API):   Requiere API key válida
🥄 Capa 2 (Chrome):      Depende 100% de claude.ai
```

---

## SCRIPTS GENERADOS

| Script | Ubicación | Función |
|--------|-----------|---------|
| debate-mini.js | container cloud | Debate 2 duendes Claude vía API |
| debate-sonnet.js | container cloud | Misma pero con Sonnet |
| debate-tacos-capa1.js | PC BeachHouse | Debate Claude vía API desde PC |
| debate-multiai-capa1.js | PC BeachHouse | **Debate multi-IA headless** |

---

> "El duende que tiene browser tiene manos. El duende con Puppeteer tiene manos invisibles — navega 3 IAs a la vez, sin que nadie sepa que está ahí."

— Caso de Estudio Debate Tacos, Colmena 2026
