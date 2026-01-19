# MediCompara MX

## App de Comparación de Precios de Medicamentos USA → México

---

### 🎯 ¿Qué es?

App nativa para adultos mayores expats (estadounidenses/canadienses en México) que traduce nombres de medicamentos y compara precios entre farmacias mexicanas.

**Tagline:** *"Escribe tu medicina gringa, te digo cómo se llama en México y dónde es más barata."*

---

### 📁 Documentos en esta carpeta

| Archivo | Descripción |
|---------|-------------|
| `SPEC_MEDICOMPARA.md` | Especificación completa de diseño y UX |
| `INVESTIGACION_MERCADO.md` | Research de mercado, competencia, APIs, regulación |
| `README.md` | Este archivo |

---

### 👤 Usuario Objetivo

- **Quién:** Expat estadounidense/canadiense, 65-80 años
- **Dónde:** Puerto Vallarta, Lake Chapala, San Miguel de Allende, Mérida
- **Problema:** No sabe cómo se llaman sus medicamentos en México, no sabe dónde es más barato
- **Techo tecnológico:** WhatsApp (la app debe ser igual o más simple)

---

### 💰 Oportunidad de Negocio

- 1.6M de estadounidenses viven en México
- 21% de adultos mayores USA omiten medicamentos por costo
- Medicamentos en México cuestan 40-70% menos
- GoodRx (modelo similar en USA) genera $792M/año con 40% margen

---

### 🛠 Stack Sugerido

**Opción A (Cross-platform):**
- React Native o Flutter
- Node.js / Python backend
- PostgreSQL
- APIs: RxNorm, openFDA, Google Maps

**Opción B (Nativo):**
- iOS: SwiftUI
- Android: Kotlin + Jetpack Compose
- Backend compartido

---

### 📱 Features MVP

1. **Búsqueda** por nombre de medicamento USA
2. **Equivalente mexicano** con pronunciación de audio
3. **Comparativa de precios** (Similares, Del Ahorro, Guadalajara, San Pablo)
4. **Modo Farmacia** - Pantalla para mostrar al empleado (letra gigante)
5. **Mi lista** de medicinas guardadas con resumen de ahorro
6. **Mapa** de farmacias cercanas
7. **Bilingüe** EN/ES

---

### 🚫 NO incluir en MVP

- Sustancias controladas (opioides, benzos)
- E-commerce / venta directa
- Consultas médicas / telemedicina
- Envío a USA

---

### 📊 Fuentes de Datos

| Fuente | Uso | Costo |
|--------|-----|-------|
| RxNorm API | Equivalencias USA→genérico | Gratis |
| openFDA | Info de medicamentos | Gratis |
| Scraping farmacias MX | Precios | ScraperAPI free tier o manual |
| Google Maps | Ubicaciones | Free tier |

---

### 🔗 Links Relacionados

- **HCRPV (Healthcare Resources PV):** Potencial partner para referidos médicos
- **Mi Salud PV:** App hermana para pacientes expats → `mi-salud-pv.vercel.app`

---

### 📞 Contacto

**Proyecto:** Colmena 2026  
**Autor del SPEC:** C-OG

---

*Hecho con 🧡 - Enero 2026*
