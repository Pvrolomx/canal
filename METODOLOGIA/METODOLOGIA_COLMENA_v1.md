# 🐝 METODOLOGÍA COLMENA v1.0
## Cómo pensar, orquestar y validar — más allá de la ejecución

> **Versión:** 1.0
> **Fecha:** 17 Mayo 2026
> **Autor:** Rolo (Arquitecto) + CD Senior (sesión calculadora-fiscal)
> **Complementa:** RDE-Cloud v2, RDE-RPi v2

---

## 🎯 PRINCIPIO CORE

> **Las RDE dicen cómo hacer. La Metodología dice cómo pensar.**

Un duende que solo sigue RDE ejecuta.
Un duende que entiende la Metodología orquesta.
La diferencia es la capacidad de adaptarse cuando el caso no está en el manual.

---

## 🏗️ PARTE 1 — PROTOCOLO SENIOR/JUNIOR/SUPERVISOR

### Los tres roles

| Rol | Función | Cuándo interviene |
|-----|---------|-------------------|
| **Supervisor** | Valida lógica de negocio y arquitectura | Escala desde Senior, discrepancias críticas |
| **Senior** | Puente entre Rolo y Junior. Revisa, aprueba, briefea | Antes de cada push del Junior |
| **Junior** | Ejecuta código bajo supervisión | Siempre, con ✅ del Senior |

### Flujo de trabajo

```
Rolo define tarea
    ↓
Senior recibe y entiende el contexto completo
    ↓
Senior briefea al Junior con alcance exacto
    ↓
Junior propone el código / cambio
    ↓
Senior revisa → ✅ o pide corrección
    ↓
Junior pushea SOLO con ✅
    ↓
Senior reporta a Rolo
    ↓
Rolo prueba y confirma
```

### Reglas del flujo

1. **Las instrucciones del Senior ya vienen autorizadas por Rolo** — el Junior no espera confirmación adicional
2. **Junior nunca pushea sin ✅ del Senior** — sin excepción, aunque el cambio sea de una línea
3. **Senior muestra el código propuesto antes de dar ✅** — el Junior propone, el Senior valida
4. **Supervisor es backup del Senior** — se escala cuando hay discrepancia de lógica de negocio o falla del caso de validación

### Cuándo escalar al Supervisor

- Discrepancia de lógica fiscal, legal o de negocio que el Senior no puede resolver
- El caso de validación falla y no se identifica la causa
- El Junior propone algo que el Senior no sabe si es correcto
- Rolo pide algo que afecta el motor principal de cálculo

---

## 🔄 PARTE 2 — PROTOCOLO DE ROTACIÓN DE MODELOS

### El ciclo Opus → Sonnet

```
[1] Opus entra como Junior breve
        ↓ (1 sesión de orientación)
[2] Opus asciende a Senior
        ↓
[3] Sonnet entra como Junior ejecutor
        ↓ (múltiples sesiones)
[4] Sonnet asciende a Senior
        ↓
[5] Nuevo Opus entra como Junior breve
        ↓
[ciclo continúa]
```

### Por qué funciona

| Modelo | Rol óptimo | Razón |
|--------|-----------|-------|
| **Opus** | Junior breve → Senior | Mapea el sistema completo rápido, detecta edge cases, entiende el "por qué" |
| **Sonnet** | Junior ejecutor | Con briefing preciso del Senior Opus, ejecuta con disciplina por más sesiones a menor costo |

**Opus como Junior breve no es desperdicio — es inversión.**
En poco tiempo mapea el sistema completo. Eso lo convierte en Senior de calidad alta rápidamente.

### Criterio de ascenso

Un Junior asciende cuando demuestra:
- Entiende el motor/lógica central — no solo ejecuta pasos
- Verifica antes de asumir (busca funciones, IDs, nombres reales antes de proponer)
- Reporta honestamente cuando algo no existe o no cuadra
- Propuso al menos una solución no solicitada que fue correcta
- No pusheó cuando tuvo duda

### El HO de ascenso

Cada ascenso genera un HO formal que incluye:
- Estado actual del proyecto (archivos, últimos commits, pendientes)
- Lo que el Junior demostró que justifica el ascenso
- Tareas en cola para el siguiente Junior
- Caso de validación vigente
- Reglas absolutas del proyecto

---

## 🔬 PARTE 3 — PIPELINES POR DOMINIO

### Pipeline de Apps (desarrollo)

```
Rolo define SPEC
    ↓
Senior Opus entiende arquitectura y briefea
    ↓
Junior ejecuta cambios en código
    ↓
Validación: browser con motor JS real
    ↓
Árbitro final: Rolo prueba en browser
```

**Criterio de validación:** número/resultado correcto en browser.
El test harness externo (Python, scripts) es aproximación — no es árbitro.
El árbitro es siempre el motor real en el entorno real.

### Pipeline Jurídico (investigación legal)

```
Opus Senior genera prompt disparador (el "Trump")
    ↓
La Colmena responde en paralelo (6-12 IAs)
    ↓
Respuestas compiladas en MD
    ↓
MD cargado a NotebookLM
    ↓
Opus Senior genera prompt de análisis para NotebookLM
    ↓
Sonnet Verificador valida cada cita/tesis/artículo
    ↓
Árbitro final: Rolo lee el MD y da visto bueno
```

**Criterio de validación:** fuente real verificable.
Una tesis que no existe en el registro oficial → descartada, sin importar cuántas IAs la citaron.

### Pipeline Médico (investigación clínica)

Mismo esquema que jurídico. El Verificador Sonnet valida:
- Dosis contra fuente primaria (vademécum, ficha técnica)
- Referencias contra PubMed / fuente citada
- Contraindicaciones contra prospecto oficial

**Criterio de validación:** fuente primaria oficial verificable.

### Tabla comparativa de dominios

| Dominio | Árbitro de validación | Error más caro | Verificador |
|---------|----------------------|----------------|-------------|
| Apps | Browser + motor real | Romper el motor de cálculo | Senior revisa código |
| Jurídico | Fuente legal real (SCJN, DOF, CPCJ) | Cita fabricada en expediente | Sonnet Verificador |
| Médico | Fuente primaria oficial | Dosis incorrecta | Sonnet Verificador |

---

## 📋 PARTE 4 — REGLA DE NO MEZCLA DE DOMINIOS

**Una sesión = un dominio.**

No mezclar desarrollo de apps con investigación jurídica en la misma sesión.
Las herramientas mentales, los criterios de validación y los riesgos son distintos.

Cuando Rolo cambia de dominio → nueva sesión, nuevo HO si aplica.

---

## 🗣️ PARTE 5 — EL HO COMO MECANISMO DE TRANSFERENCIA

El HO (Handoff) es lo que hace que el sistema no dependa de la memoria de ningún duende.

### Un HO bien escrito incluye

Para **apps:**
- Repo, rama, URL live, tokens
- Estado de cada archivo (✅ funcional / ⛔ no tocar)
- Últimos commits relevantes
- IDs críticos que no se tocan
- Caso de validación con resultado esperado
- Pendientes en cola

Para **investigación:**
- Tema y pregunta central
- Fuentes ya verificadas vs pendientes de verificar
- Citas confirmadas vs descartadas (con razón)
- Próximo prompt sugerido para La Colmena
- Estado del debate (rondas completadas, pendientes)

### Regla del HO

> **Si el siguiente duende no puede continuar solo con el HO, el HO está incompleto.**

El HO no es un resumen — es un punto de arranque autónomo.

---

## 📊 PARTE 6 — ASIGNACIÓN DE MODELOS

| Tarea | Modelo recomendado | Razón |
|-------|-------------------|-------|
| Junior en terreno conocido (ejecutar spec claro) | Sonnet | Eficiente, económico, suficiente |
| Junior en terreno ambiguo (improvisar solución) | Opus | Razonamiento profundo necesario |
| Senior / Supervisor | Opus | El error de criterio es más caro que el de ejecución |
| Verificador jurídico/médico | Sonnet | Tarea estructurada, no requiere razonamiento creativo |
| Debate Colmena (generación de perspectivas) | Mix | Diversidad de modelos genera mejor fricción |
| Análisis de debate compilado | Opus | Síntesis de perspectivas contradictorias |

---

## 🔑 PARTE 7 — VOCABULARIO OFICIAL

| Término | Significado |
|---------|-------------|
| **HO** | Handoff — documento de transferencia entre duendes |
| **CD** | Claude Duende — instancia activa |
| **RDE** | Reglas de Ejecución de La Colmena |
| **EA** | Expat Advisor MX |
| **CS** | Castle Solutions |
| **GH** | GitHub |
| **VC** | Vercel |
| **SB** | Supabase |
| **PI** | Raspberry Pi |
| **Trump** | Prompt disparador que activa La Colmena en un debate |
| **El Arquitecto** | Rolo — tiene la última palabra en todo |
| **La Colmena** | El stack completo de IAs trabajando en conjunto |

---

## 📅 HISTORIAL

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 17 May 2026 | Documento inicial — protocolo Senior/Junior/Supervisor, rotación Opus/Sonnet, pipelines por dominio, regla de no mezcla, HO como mecanismo de transferencia |

---

*"Las RDE dicen cómo hacer. La Metodología dice cómo pensar."*

🐝 **La Colmena — Orquestación inteligente · Mayo 2026**
