# 🧭 GUÍA DE DECISIÓN BROWSER — COLMENA v1.0
## Cuándo Usar Qué: Manual Práctico para Duendes

**Versión:** 1.0
**Fecha:** 3 Marzo 2026
**Autor:** Arquitecto + Claude Opus (claude.ai)
**Canal origen:** 4366

---

## PRINCIPIO FUNDAMENTAL

La Colmena tiene 3 capas de browser. Ninguna es mejor que otra. La pregunta correcta no es "¿cuál uso?" sino **"¿qué está haciendo el Arquitecto en este momento?"**

- **Arquitecto presente con tiempo** → Claude in Chrome
- **Arquitecto ocupado** → Puppeteer o API Directa
- **Arquitecto dormido/ausente** → Solo Puppeteer (cron) o API Directa (cron)

---

## LAS 3 CAPAS

| Capa | Qué es | Requiere Arquitecto | Requiere login | Velocidad |
|------|--------|---------------------|----------------|-----------|
| **Puppeteer Headless** | Chrome invisible, sin sesiones | NO | NO | Rápida (14s para 323K chars) |
| **Claude in Chrome** | Chrome real del Arquitecto | SÍ | SÍ (usa sus sesiones) | Media (depende de la página) |
| **API Directa** | Llamadas HTTP a Anthropic API | NO | N/A | Muy rápida (27s debate 3 duendes) |

---

## ESCENARIOS DE DECISIÓN

### 1. "Quiero saber qué dicen las IAs sobre un tema"

| Situación | Herramienta | Por qué |
|-----------|-------------|---------|
| Arquitecto presente, quiere voces reales | Claude in Chrome | Navega ChatGPT, Gemini, DeepSeek, Copilot con sesiones activas. Obtiene respuestas genuinas de cada IA. |
| Arquitecto ocupado, quiere resultado rápido | API Directa (Debate Engine) | Crea duendes con roles distintos, debate en 30-90 segundos. Son todos Claudes, misma base, diferentes sombreros. |
| Ya existen conversaciones previas | Puppeteer | Extrae share links de chats ya hechos. 323K chars en 14 segundos. |

### 2. "Necesito investigar algo en la web"

| Situación | Herramienta | Por qué |
|-----------|-------------|---------|
| Búsqueda pública sin login | Puppeteer | Stealth plugin pasa Cloudflare. Abre múltiples sitios en paralelo. Menos de 1 minuto. |
| Precios de socio o tarifas con login | Claude in Chrome | Necesita las sesiones activas del Arquitecto (ej: Viva Aerobus con Doters). |
| Sitios de gobierno con protecciones | Claude in Chrome | SICOR, registros públicos, sitios con JavaScript defensivo — más seguro con browser real. |

### 3. "Quiero que los duendes trabajen mientras duermo"

| Situación | Herramienta | Por qué |
|-----------|-------------|---------|
| Monitoreo de precios competencia | Puppeteer (cron) | Script Node.js cada 6h revisa Airbnb, Booking, VRBO. Precios públicos, no necesita login. |
| Análisis recurrente o reportes | API Directa (cron) | Debate Engine procesa temas, postea resultados en chat.duendes.app. |
| Cualquier cosa con login | **NO SE PUEDE** | Claude in Chrome solo existe cuando el Arquitecto existe. |

### 4. "Quiero leer conversaciones históricas"

| Situación | Herramienta | Por qué |
|-----------|-------------|---------|
| Chat con share link | Puppeteer | ChatGPT, Copilot, Claude — todos probados. Velocidad imbatible. |
| Chat SIN share link | Claude in Chrome | Navega historial de chats del Arquitecto, busca por keywords. |
| DeepSeek (cualquier caso) | Claude in Chrome | CAPTCHA bloquea Puppeteer headless. Sin excepción. |

### 5. "Quiero construir o deployar algo"

| Situación | Herramienta | Por qué |
|-----------|-------------|---------|
| Deploy, push, config dominio | MCP + API (sin browser) | Vercel MCP, GitHub API, bash. Los browsers no aplican para tu infraestructura. |
| Verificar visualmente un deploy | Claude in Chrome | Screenshot rápido del sitio en vivo. |

### 6. "Quiero que un duende haga algo en mi cuenta"

| Situación | Herramienta | Por qué |
|-----------|-------------|---------|
| Reservar, comprar, llenar formulario | Claude in Chrome + Arquitecto | SIEMPRE con supervisión. Cualquier acción que toque cuenta, dinero o datos. |

---

## TABLA DE DECISIÓN RÁPIDA

| Arquitecto está... | Necesita... | Usa... |
|---------------------|-------------|--------|
| Presente, con tiempo | Debate multi-IA real | Claude in Chrome |
| Presente, con tiempo | Navegar con login | Claude in Chrome |
| Presente, con tiempo | Acción en su cuenta | Claude in Chrome |
| Ocupado | Scraping público | Puppeteer |
| Ocupado | Debate rápido | API Directa |
| Ocupado | Leer share links | Puppeteer |
| Dormido | Monitoreo de precios | Puppeteer (cron) |
| Dormido | Análisis recurrente | API Directa (cron) |
| Dormido | Cualquier cosa con login | **No se puede** |
| Donde sea | Deploy/build | MCP + API (sin browser) |

---

## PROBLEMAS CONOCIDOS POR CAPA

### Puppeteer
- DeepSeek lo bloquea con CAPTCHA (usar Claude in Chrome)
- No puede usar dos instancias con el mismo perfil Chrome
- Stealth plugin no es 100% (Skyscanner tiene detección secundaria)
- Si la PC se apaga, se muere. No hay fallback cloud.

### Claude in Chrome
- Se desconecta cada ~20 min inactivo (Arquitecto reconecta con 1 click)
- Solo ve tabs de su grupo MCP
- CAPTCHAs y passwords los resuelve el Arquitecto manualmente
- Screenshot → find → click es más lento que API

### API Directa
- Balance limitado ($2.56 al momento de escribir esto)
- Solo modelos Anthropic — no hay voces de GPT, Gemini, DeepSeek
- Model strings cambian sin aviso (verificar antes de usar)

---

## NOTA PARA DUENDES

No intentes usar una capa para lo que no sirve. Si no tienes al Arquitecto presente, no intentes Claude in Chrome. Si necesitas login, no pierdas tokens con Puppeteer. Si necesitas voces reales de otras IAs, no simules con API.

Pregúntate: **¿El Arquitecto está aquí?** Eso decide todo.

---

🐝 Sistema Colmena — Browser Decision Guide v1.0
