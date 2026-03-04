# 🧠 ORQUESTACIÓN DE DEBATES MULTI-IA - COLMENA v1.0

**Sistema para extraer verdad emergente a través de fricción controlada entre múltiples IAs**

---

## 📋 METADATA

- **Versión:** 1.0
- **Fecha:** 4 Marzo 2026
- **Autor:** Claude Beach House (Orquestador) + 5 IAs Externas (Debatedores)
- **Estado:** PROBADO EN CAMPO (Ronda 1-2, Debate sobre creatividad en Puerto Vallarta)
- **Caso de Estudio:** "¿Nómada vs Horario Fijo para trabajo creativo?"

---

## 🎯 OBJETIVO

Diseñar un **protocolo de debate controlado** donde:
1. **Una IA orquestadora** (Claude) coordina 5-6 IAs externas
2. **Cada IA responde al mismo prompt** en paralelo (sin esperar)
3. **El Arquitecto envía en paralelo** (una sola conexión, muchos clics)
4. **Claude cosecha, sintetiza, identifica fricción**
5. **Próximo prompt es diseñado PROVOCADOR** para forzar contradicción

**Meta final:** Iterar hacia **verdad emergente** que ninguna IA individual habría sacado.

---

## 🏗️ ARQUITECTURA

```
┌─────────────────────────────────────────────────────────────┐
│                  CLAUDE (ORQUESTADOR)                        │
│              (Beach House - Tab Activa)                      │
└─────────────┬───────────────────────────────────────────────┘
              │
              ├─→ [TAB 1] ChatGPT 5.2
              ├─→ [TAB 2] Microsoft Copilot
              ├─→ [TAB 3] Claude Cloud (claude.ai)
              ├─→ [TAB 4] DeepSeek
              ├─→ [TAB 5] Grok
              └─→ [TAB 6] Google Gemini
              
ARQUITECTO (Desktop)
  │
  └─→ Clica ENVIAR en todas las tabs (paralelo)
```

### Componentes Clave

| Componente | Rol | Ubicación |
|---|---|---|
| **Claude Beach House** | Orquestador: postea, cosecha, sintetiza | Este archivo (controlador) |
| **5-6 IAs** | Debatedores: responden al prompt | Tabs diferentes en navegador |
| **Arquitecto** | Control humano: decide ritmo, envía | Desktop del Arquitecto |
| **Protocolo de punto (.)** | Signal: "cosecha ahora" | Chat principal |

---

## 📊 PROTOCOLO DE EJECUCIÓN (3 FASES)

### **FASE 1: POSTEO (Claude sin esperar)**

```
1. Claude lee histórico de debate anterior
   └─ ¿Qué convergió? ¿Qué friccionó?

2. Claude diseña PROMPT PROVOCADOR
   └─ Fuerza contradicción con respuestas previas
   └─ Es legítimo, no es troll

3. Para CADA TAB (rápido, sin drama):
   a) screenshot → leer estado actual
   b) click en input field
   c) type el PROMPT COMPLETO
   d) screenshot → verificar que entró
   └─ NUNCA click "enviar" — eso lo hace el Arquitecto

4. Cuando termina tab 6:
   └─ Claude avisa: "RONDA X POSTEADA — 6/6 ✅"
```

### **FASE 2: ENVÍO (Arquitecto en paralelo)**

```
Arquitecto sigue:
  "Ahora vos clica ENVIAR en las 6 tabs EN PARALELO
   (tab 1 → tab 2 → tab 3 → tab 4 → tab 5 → tab 6)
   No esperes entre tabs. Rápido."

Result:
  ✅ ChatGPT respondiendo
  ✅ Copilot respondiendo
  ✅ Claude Cloud respondiendo
  ✅ DeepSeek respondiendo
  ✅ Grok respondiendo
  ✅ Gemini respondiendo
```

### **FASE 3: COSECHA (Claude reactivo)**

```
Arquitecto escribe: "."

Claude:
  1. Scroll + screenshot cada tab (no get_page_text, es impreciso)
  2. Leer RESPUESTA NUEVA (no histórico)
  3. Compilar 6 respuestas
  4. Identificar:
     - ¿Dónde convergen?
     - ¿Dónde divergen?
     - ¿Qué insight NO dijeron?
  5. Diseñar PROMPT RONDA SIGUIENTE que profundice
  6. Repetir FASE 1
```

---

## 🔧 REGLAS TÉCNICAS CRÍTICAS

### Cómo postear en cada IA (probado en campo)

| IA | Método | Funciona | Notas |
|---|---|---|---|
| **ChatGPT** | click → type → screenshot | ✅ | Más confiable |
| **Copilot** | click → type → screenshot | ✅ | A veces finicky |
| **Claude.ai** | click → type → screenshot | ✅ | Más lento |
| **DeepSeek** | form_input (recomendado) | ✅ | Responde rápido |
| **Grok** | scroll → click → type | ✅ | Input escondido |
| **Gemini** | type + click en bot | ✅ | Div editable |

### ❌ QUÉ NO HACER

- ❌ `wait` largos (>2 seg) — causa desconexión extensión
- ❌ `get_page_text` para cosecha — trae histórico completo, no respuesta nueva
- ❌ `form_input` en ChatGPT — no soporta contenteditable
- ❌ Esperar respuestas antes de mover a siguiente tab
- ❌ Click en "enviar" — lo hace el Arquitecto
- ❌ Asumir que las IAs entendieron igual — siempre friccionan diferente

### ✅ QUÉ SÍ HACER

- ✅ **Scroll + screenshot** para cosecha (visual, más preciso)
- ✅ **click → type → screenshot** en cada tab (orden crítico)
- ✅ **Esperar punto (.)** para activarse (no ansía)
- ✅ **Diseñar prompts que fuercen contradicción** (la fricción = verdad)
- ✅ **Iterar N veces** (no parar en Ronda 1)

---

## 📈 EJEMPLO: DEBATE SOBRE CREATIVIDAD EN PUERTO VALLARTA

### Ronda 1: Convergencia
**Pregunta:** "¿Cuál es el mejor horario para trabajo creativo?"

**Convergencia 6/6:**
- 2-4 horas después de despertar = ventana dorada
- Cronotipo = variable importante
- Bloque ininterrumpido > hora exacta

**Insight:** Todos están de acuerdo, pero por razones DIFERENTES (algunos dicen fatiga cognitiva, otros dicen cortisol, otros dicen fatiga de decisión).

### Ronda 2: FRICCIÓN FORZADA
**Pregunta Provocadora:** "En Vallarta (playa, interrupciones), ¿nómada resetea fatiga o la aumenta?"

**Divergencia 5/5:**
| IA | Posición |
|---|---|
| **DeepSeek** | Nómada SÍ funciona (novo = reset) |
| **Grok** | Híbrido 2-3 lugares (estructura) |
| **ChatGPT** | Dos fases: fijo para crear, movimiento para idear |
| **Copilot** | 2-3 pre-decididos (hábito, no decisión) |
| **Gemini** | Fijo SÍ, reset es fisiológico (mar 15min) |

**Fricción productiva:**
- ¿El reset es neurológico o psicológico?
- ¿Nómada REDUCE fatiga de decisión o la AUMENTA con logística?
- ¿"Reset" significa dormir, cambiar lugar, o caminar?

### Ronda 3 (PRÓXIMA): SÍNTESIS FORZADA
**Pregunta Meta:** "Combinando DeepSeek (novo=reset) + Claude (ruido moderado) + Grok (estructura), ¿cuál es el protocolo ÓPTIMO que NINGUNO propuso?"

**Expected:** Insight emergente que requiere haber entendido + transcendido todas las posiciones.

---

## 🧠 INSIGHTS CLAVE (APRENDIDOS EN CAMPO)

### 1. **No es debate performativo**
- No es "vemos qué piensa cada IA"
- ES "iteramos para encontrar verdad que emerge cuando friccionan"
- Ronda 1 = divergencia probable
- Ronda 2+ = convergencia + contradicción productiva

### 2. **La fricción es el dato**
- Cuando 2 IAs se contradicen = oportunidad de profundidad
- El próximo prompt debe EXPLOTAR esa contradicción
- No ir a consenso — ir a comprensión más profunda

### 3. **Claude (Orquestador) es crítico**
- No participa en el debate (está en chat diferente)
- Pero DISEÑA los prompts que fuerzan fricción
- Sin buena orquestación = desorden
- Con buena orquestación = emergencia de verdad

### 4. **Arquitecto controla RITMO, Claude controla PROFUNDIDAD**
- Arquitecto decide cuándo parar/continuar (punto)
- Claude decide qué preguntar después (basado en fricción)
- Separación de poderes = mejor sinergia

---

## 🔄 LOOP DE ITERACIÓN

```
RONDA N
  │
  ├─→ Claude postea prompt en 6 tabs
  │
  ├─→ Arquitecto envía en paralelo
  │
  ├─→ [Respuestas llegan]
  │
  ├─→ Arquitecto dice "."
  │
  ├─→ Claude cosecha + sintetiza
  │    ├─ Convergencias (verdad probable)
  │    ├─ Divergencias (fricción productiva)
  │    └─ Gaps (lo que no dijeron)
  │
  └─→ Claude diseña RONDA N+1
      └─ Prompt que FUERCE contradicción con N
      └─ Vuelve a RONDA N

[Repeat hasta insight emergente]
```

---

## 📋 CHECKLIST PARA ORQUESTADOR

- [ ] Leí histórico de rondas anteriores
- [ ] Identifiqué convergencias y divergencias
- [ ] Diseñé prompt que FUERCE fricción (no es neutral)
- [ ] Prompt es legítimo (no troll)
- [ ] Tengo 6 tabs abiertas y listas
- [ ] Esperé punto (.) — no asumo que cosecho automático
- [ ] Scrolleé antes de leer (visual > get_page_text)
- [ ] Sintetizaré antes de próxima ronda

---

## 🎬 NEXT STEPS

**Ronda 3 (próxima):**
Pregunta que fuerce síntesis emergente:
> "Combinando DeepSeek (novo=reset) + Claude (ruido moderado) + Grok (2-3 anclas), ¿cuál sería el protocolo ÓPTIMO para Puerto Vallarta que NINGUNO propuso sola?"

**Meta:** Que las 6 se den cuenta que necesitan READ las otras para responder.

---

## 📚 REFERENCIAS

- **RDB_BROWSER_ENGINE_v1.md** — Reglas base del Browser
- **GUIA_DECISION_BROWSER_v1.md** — Decisiones de qué browser usar
- **REGLAS_DE_EJECUCION_CLOUD_v1.md** — Cómo ejecutar desde la nube
- **CASO_ESTUDIO_DEBATE_TACOS.md** — Otro caso (más sobre estilo comida)

---

## ✍️ HISTORIAL DE CAMBIOS

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 4 Mar 2026 | Documento inicial. Rondas 1-2 completadas. Protocolo validado. |

---

**AUTOR:** Claude Beach House (Orquestador)
**COLABORADORES:** ChatGPT 5.2, Copilot, Claude Cloud, DeepSeek, Grok, Gemini
**ARQUITECTO:** Puerto Vallarta, Jalisco

---

🧠 **"El duende que tiene browser tiene manos. El orquestador que tiene 6 browsers tiene verdad."** — Colmena v2
