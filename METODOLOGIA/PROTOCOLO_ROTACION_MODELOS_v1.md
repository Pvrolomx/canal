# 🔄 PROTOCOLO DE ROTACIÓN DE MODELOS v1.0
## Asignación óptima de Opus y Sonnet en La Colmena

> **Versión:** 1.0
> **Fecha:** 17 Mayo 2026
> **Autor:** Rolo (Arquitecto) + CD Senior (sesión calculadora-fiscal)
> **Parte de:** `METODOLOGIA/METODOLOGIA_COLMENA_v1.md`

---

## 🎯 PRINCIPIO

> **Opus razona. Sonnet ejecuta. El ciclo transfiere conocimiento.**

No se trata de qué modelo es "mejor" —
se trata de qué modelo es óptimo para cada momento del ciclo.

---

## 🔄 EL CICLO

```
┌─────────────────────────────────────────────────────────────┐
│                    CICLO DE ROTACIÓN                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [1] OPUS entra como Junior                                │
│        • 1 sesión de orientación profunda                   │
│        • Mapea el sistema completo por dentro               │
│        • Detecta edge cases que el briefing no menciona     │
│        ↓                                                    │
│   [2] OPUS asciende a Senior                                │
│        • Genera HO de ascenso detallado                     │
│        • Briefea al siguiente Junior con los "por qué"      │
│        • Revisa, aprueba, no ejecuta                        │
│        ↓                                                    │
│   [3] SONNET entra como Junior ejecutor                     │
│        • Múltiples sesiones bajo supervisión del Senior     │
│        • Ejecuta specs claros con disciplina                │
│        • Más económico para trabajo sostenido               │
│        ↓                                                    │
│   [4] SONNET asciende a Senior                              │
│        • Genera HO de ascenso                               │
│        • Nuevo Opus entra como Junior breve                 │
│        ↓                                                    │
│   [5] Ciclo continúa ──────────────────────────────────────┘
│
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 CRITERIOS DE ASCENSO

Un Junior asciende cuando demuestra **todos** los siguientes:

### Criterios técnicos
- [ ] Entiende el motor/lógica central — no solo ejecuta pasos mecánicamente
- [ ] Verifica nombres reales antes de proponer (funciones, IDs, rutas)
- [ ] Propuso al menos una solución no solicitada que fue correcta
- [ ] Corrió la validación con el método correcto (browser/fuente real, no aproximación)

### Criterios de protocolo
- [ ] Nunca pusheó sin ✅ del Senior
- [ ] Reportó honestamente cuando algo no existía o no cuadraba
- [ ] Escaló al Senior cuando tuvo duda en lugar de improvisar
- [ ] Su reporte de push incluyó SHA, diff stat y validación

### Señal de ascenso inequívoca
> El Junior resolvió un problema que **no estaba en el briefing**
> usando razonamiento propio — y lo resolvió bien.

---

## 🎭 PERFILES POR ROL

### Opus como Junior (orientación)
**Duración:** 1 sesión
**Objetivo:** Mapear el sistema por dentro antes de dirigirlo

Lo que hace que otros Juniors no hacen:
- Cuestiona los nombres de funciones antes de usarlos
- Detecta qué test harness es impreciso vs qué motor está roto
- Propone validaciones end-to-end sin que se lo pidan
- Su reporte de push es un documento, no una línea

**Señal de que está listo para ascender:**
Resolvió algo que no estaba en el spec y lo documentó.

---

### Sonnet como Junior (ejecución)
**Duración:** Múltiples sesiones
**Objetivo:** Ejecutar specs claros con velocidad y disciplina

Funciona bien cuando:
- El Senior le da alcance exacto y IDs exactos
- La tarea es aplicar un patrón conocido
- No requiere improvisar la solución

Necesita escalar cuando:
- El nombre de una función o ID no existe en el código real
- El resultado de validación se sale del rango esperado
- La tarea afecta el motor principal

---

### Opus como Senior
**Duración:** Indefinida (vive en el HO)
**Objetivo:** Revisar, aprobar, briefear — no ejecutar

Sus instrucciones al Junior incluyen:
- Qué tocar y qué no tocar (con razón)
- El caso de validación y el rango aceptable
- Las funciones/IDs reales que el Junior debe usar
- El criterio de escalada al Supervisor

---

## 💰 ECONOMÍA DEL CICLO

| Fase | Modelo | Costo relativo | Valor generado |
|------|--------|---------------|----------------|
| Junior orientación | Opus | Alto (1 sesión) | Mapeo profundo del sistema |
| Senior | Opus | Alto (por sesión) | Criterio de aprobación de calidad |
| Junior ejecutor | Sonnet | Bajo (muchas sesiones) | Volumen de trabajo sostenido |
| Verificador | Sonnet | Bajo | Validación estructurada de fuentes |

**La inversión en Opus Junior es recuperada por la calidad del briefing que genera como Senior.**
Un Senior Opus que entiende el sistema de adentro briefea mejor → el Junior Sonnet comete menos errores → menos iteraciones → menor costo total.

---

## 📊 TABLA DE ASIGNACIÓN RÁPIDA

| Situación | Modelo | Rol |
|-----------|--------|-----|
| Proyecto nuevo — primer duende | Opus | Junior breve → Senior |
| Tarea rutinaria con spec claro | Sonnet | Junior ejecutor |
| Tarea ambigua sin spec completo | Opus | Junior o Senior |
| Revisión de código antes del push | Opus | Senior |
| Validación de citas jurídicas | Sonnet | Verificador |
| Validación de referencias médicas | Sonnet | Verificador |
| Debate Colmena — generación | Mix | Participantes |
| Síntesis de debate compilado | Opus | Analista |
| Pipeline NotebookLM — prompt | Opus | Senior generador |

---

## 📝 FORMATO DEL HO DE ASCENSO

Todo ascenso genera un HO con esta estructura mínima:

```markdown
# HO — ASCENSO · DE JUNIOR A SENIOR
**Para:** Duende que ascendió
**De:** Supervisor / CD sesión anterior
**Fecha:** DD/MM/YYYY
**Proyecto:** nombre del proyecto

## Lo que demostraste
[qué hizo el Junior que justifica el ascenso]

## Tu nuevo rol
[qué cambia, qué no cambia]

## Estado del proyecto
[archivos, últimos commits, pendientes]

## El Junior nuevo
[qué necesita saber antes de arrancar]

## Reglas que ahora haces cumplir
[las mismas RDE, pero ahora las aplicas al Junior]

## Cuándo escalar al Supervisor
[criterios específicos del proyecto]
```

---

## ⚠️ LO QUE NO CAMBIA CON EL ASCENSO

El ascenso cambia el rol, no las reglas.

Un Senior que fue Junior de este proyecto sigue respetando:
- Las mismas RDE de ejecución
- Los mismos IDs intocables
- El mismo caso de validación
- La misma jerarquía: Rolo tiene la última palabra

**La diferencia es que ahora las hace cumplir, no solo las sigue.**

---

## 📅 HISTORIAL

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 17 May 2026 | Documento inicial — ciclo Opus/Sonnet, criterios de ascenso, perfiles por rol, economía del ciclo, formato HO ascenso |

---

*"Opus razona. Sonnet ejecuta. El ciclo transfiere conocimiento."*

🐝 **La Colmena — Rotación inteligente de modelos · Mayo 2026**
