# SPEC: MediCompara MX
## App de Comparación de Precios de Medicamentos USA → México

**Versión:** 1.1  
**Fecha:** Enero 2026  
**Autor:** C-OG / Colmena

---

## 0. ASSETS REQUERIDOS

### Imagen de fondo principal
**Archivo:** `Cover Medicompara 3.png`  
**Ubicación:** `github.com/Pvrolomx/canal/Medicompara/`  
**Dimensiones:** 1024x1536 (vertical, optimizada para móvil)  
**Uso:** Background de home screen con overlay

![Cover](https://raw.githubusercontent.com/Pvrolomx/canal/main/Medicompara/Cover%20Medicompara%203.png)

**Características de la imagen:**
- Farmacia mexicana estilo "pueblo mágico"
- Cielo limpio (~40% superior) para UI
- Bokeh/difuminado en fondo
- Tonos cálidos terracota
- Cruz verde de farmacia visible
- Espacio para overlay y texto

---

## 1. CONSTRUCCIÓN INCREMENTAL

### Deploy 1: Solo imagen de fondo
```
- index.html con imagen fullscreen
- Overlay gradient oscuro (50-60%)
- Logo "MediCompara" centrado
- Texto "Próximamente" o barra de búsqueda dummy
- PWA manifest básico
```

### Deploy 2: Home + Búsqueda
```
- Barra de búsqueda funcional
- Base de datos de 10 medicamentos
- Resultado básico (nombre MX)
```

### Deploy 3: Modo Farmacia
```
- Pantalla fullscreen letra gigante
- Botón de audio (pronunciación)
```

### Deploy 4: Mi Lista + Precios
```
- Guardar medicinas
- Comparativa de precios
- Resumen de ahorro
```

### Deploy 5: Farmacias + PWA completa
```
- Mapa de farmacias
- Instalación PWA
- Ajustes de idioma
```

---

## 2. RESUMEN EJECUTIVO

**Problema:** Adultos mayores expats estadounidenses en México no saben cómo se llaman sus medicamentos en español ni dónde comprarlos más barato.

**Solución:** App nativa que traduce nombres de medicamentos USA→México y compara precios entre farmacias.

**Usuario objetivo:** Expat estadounidense/canadiense, 65-80 años, viviendo en México (PV, Lake Chapala, San Miguel de Allende).

**Propuesta de valor:** "Escribe tu medicina gringa, te digo cómo se llama en México y dónde es más barata."

---

## 3. USUARIO PRIMARIO

### Perfil: "Don Robert"

| Atributo | Detalle |
|----------|---------|
| Edad | 72 años |
| Origen | Arizona, USA |
| Residencia | Puerto Vallarta, 10 meses/año |
| Idioma | Inglés nativo, español básico |
| Dispositivo | iPhone (regalo de su hijo) |
| Techo tecnológico | WhatsApp |
| Medicamentos | 5-6 diarios |
| Limitaciones | Vista reducida, memoria no tan buena |

### Contexto emocional
- **Frustración:** No lo entienden en la farmacia
- **Miedo:** Comprar "algo malo" por error
- **Desconfianza:** ¿El genérico mexicano es igual?
- **Motivación:** Ahorrar dinero (pensión limitada)

---

## 4. MOMENTOS DE USO

| Momento | Dónde | Estado | Necesidad principal |
|---------|-------|--------|---------------------|
| Planificando | Casa, sentado | Tranquilo | "¿Cuánto me ahorro si compro aquí?" |
| Preparándose | Casa, antes de salir | Con prisa leve | "¿Cómo se llama? ¿Dónde voy?" |
| **En farmacia** | Mostrador | Parado, nervioso, sol en pantalla | "Que el empleado vea qué necesito" |
| Post-compra | Casa | Reflexivo | "¿Me cobraron bien?" |

**Momento crítico:** EN LA FARMACIA → El diseño debe optimizar para este momento.

---

## 5. ARQUITECTURA DE INFORMACIÓN

```
MediCompara
│
├── 🏠 HOME
│   ├── Barra de búsqueda (prominente)
│   ├── Últimas búsquedas (acceso rápido)
│   └── Acceso a "Mis Medicinas"
│
├── 🔍 BÚSQUEDA / RESULTADO
│   ├── Nombre USA → Nombre MX (prominente)
│   ├── Comparativa de precios (3-4 farmacias)
│   ├── Botón "Modo Farmacia"
│   └── Botón "Guardar en mi lista"
│
├── 💊 MIS MEDICINAS
│   ├── Lista de medicinas guardadas
│   ├── Resumen de ahorro mensual
│   └── Acceso rápido a cada una
│
├── 🏪 MODO FARMACIA
│   ├── Nombre MX en letra ENORME
│   ├── Dosis
│   ├── Instrucción: "Muestre al farmacéutico"
│   └── (Pantalla optimizada para mostrar)
│
├── 📍 FARMACIAS CERCA
│   ├── Mapa con ubicaciones
│   ├── Filtro por cadena
│   └── Navegación a Google Maps
│
└── ⚙️ AJUSTES
    ├── Idioma (EN/ES)
    ├── Tamaño de letra
    └── Notificaciones
```

---

## 6. PANTALLAS DETALLADAS

### 6.1 HOME (con imagen de fondo)

```
┌─────────────────────────────────────┐
│                                     │
│  [IMAGEN: Cover Medicompara 3.png]  │
│  [Overlay gradient 50% oscuro]      │
│                                     │
│         🇲🇽 MediCompara             │  ← Logo blanco
│    "Tu medicina, mejor precio"      │  ← Texto blanco
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 🔍 Buscar medicina...       │   │  ← Input con fondo blanco
│  └─────────────────────────────┘   │
│                                     │
│   Recientes:                        │  ← Texto blanco/gris claro
│   • Lipitor 20mg                    │
│   • Metformin 850mg                 │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  💊 Mis Medicinas (5)       │   │  ← Cards semi-transparentes
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  📍 Farmacias Cerca         │   │
│  └─────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│  🏠    🔍    💊    📍    ⚙️        │  ← Tab bar sólido
└─────────────────────────────────────┘
```

**CSS para imagen de fondo:**
```css
.home-screen {
  background-image: url('/hero-bg.png');
  background-size: cover;
  background-position: center bottom;
}

.home-overlay {
  background: linear-gradient(
    to bottom,
    rgba(0,0,0,0.6) 0%,
    rgba(0,0,0,0.4) 50%,
    rgba(0,0,0,0.7) 100%
  );
}
```

### 6.2 RESULTADO DE BÚSQUEDA

```
┌─────────────────────────────────────┐
│  ← Atrás          🇺🇸/🇲🇽 toggle   │
│                                     │
│  Tu búsqueda:                       │
│  LIPITOR 20mg                       │
│                                     │
│  ════════════════════════════════   │
│                                     │
│  En México pide:                    │
│  ┌─────────────────────────────┐   │
│  │    ATORVASTATINA            │   │  ← Letra grande
│  │        20 mg                │   │
│  │  [🔊 Escuchar]  [📋 Copiar] │   │
│  └─────────────────────────────┘   │
│                                     │
│  ✅ Mismo ingrediente activo        │
│  ✅ Aprobado por COFEPRIS           │
│                                     │
│  💰 Precios aproximados:            │
│  ┌─────────────────────────────┐   │
│  │ 🟢 Similares        $85 MXN │ ★ │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ ⚪ Guadalajara     $110 MXN │   │
│  └─────────────────────────────┘   │
│                                     │
│  💵 Ahorras: ~$230 MXN (~75%)       │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  🏪 MODO FARMACIA           │   │
│  └─────────────────────────────┘   │
│                                     │
│  [💊 Guardar en mi lista]           │
│                                     │
└─────────────────────────────────────┘
```

### 6.3 MODO FARMACIA (Pantalla crítica)

```
┌─────────────────────────────────────┐
│                                     │
│  [Fondo BLANCO puro]                │
│                                     │
│                                     │
│         ATORVASTATINA               │  ← 48-64pt BOLD
│                                     │
│             20 mg                   │  ← 32pt
│                                     │
│         ───────────                 │
│                                     │
│          Caja de 30                 │
│                                     │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  📱 Muestre esta pantalla   │   │
│  │     al farmacéutico         │   │
│  └─────────────────────────────┘   │
│                                     │
│           [ ✕ Cerrar ]              │
│                                     │
└─────────────────────────────────────┘
```

**Notas críticas:**
- Fondo BLANCO (legible bajo el sol)
- Sin navegación, sin distracciones
- Bloquear auto-sleep
- El empleado debe leerlo a 1 metro

---

## 7. IDENTIDAD VISUAL

### 7.1 Paleta de colores

| Uso | Color | Código |
|-----|-------|--------|
| Primario | Verde farmacia | #059669 |
| Secundario | Azul profundo | #1e3a5f |
| Acento | Naranja mexicano | #f97316 |
| Fondo | Blanco/Crema | #fafaf9 |
| Texto | Gris oscuro | #1f2937 |

### 7.2 Tipografía

| Uso | Tamaño | Peso |
|-----|--------|------|
| Títulos | 24-32pt | Bold |
| Nombre medicina MX | 28-36pt | Bold |
| Modo Farmacia | 48-64pt | Bold |
| Cuerpo | 18-20pt | Regular |
| Mínimo | 16pt | - |

---

## 8. ACCESIBILIDAD

| Requerimiento | Implementación |
|---------------|----------------|
| Texto escalable | Respetar config sistema |
| Alto contraste | Ratio mínimo 4.5:1 |
| Touch targets | Mínimo 48x48pt |
| VoiceOver/TalkBack | Labels descriptivos |

---

## 9. TECH STACK

```
Frontend: Next.js + Tailwind CSS
Deploy: Vercel
PWA: manifest.json + service worker
Audio: Web Speech API
Storage: localStorage
```

---

## 10. BASE DE DATOS INICIAL (MVP)

```javascript
const medicamentos = [
  { usa: 'Lipitor', mx: 'Atorvastatina', dosis: '20mg', precioMX: 85 },
  { usa: 'Metformin', mx: 'Metformina', dosis: '850mg', precioMX: 45 },
  { usa: 'Lisinopril', mx: 'Lisinopril', dosis: '10mg', precioMX: 65 },
  { usa: 'Omeprazole', mx: 'Omeprazol', dosis: '20mg', precioMX: 55 },
  { usa: 'Amlodipine', mx: 'Amlodipino', dosis: '5mg', precioMX: 50 },
  { usa: 'Losartan', mx: 'Losartán', dosis: '50mg', precioMX: 70 },
  { usa: 'Simvastatin', mx: 'Simvastatina', dosis: '20mg', precioMX: 75 },
  { usa: 'Levothyroxine', mx: 'Levotiroxina', dosis: '50mcg', precioMX: 40 },
  { usa: 'Gabapentin', mx: 'Gabapentina', dosis: '300mg', precioMX: 95 },
  { usa: 'Hydrochlorothiazide', mx: 'Hidroclorotiazida', dosis: '25mg', precioMX: 35 },
]
```

---

## 11. MÉTRICAS DE ÉXITO

| Métrica | Objetivo MVP |
|---------|--------------|
| Búsquedas completadas | 80%+ |
| Uso de Modo Farmacia | 50%+ |
| Medicinas guardadas | 3+ por usuario |
| Retención D7 | 40%+ |

---

**FIN DEL SPEC v1.1**

*"Escribe tu medicina gringa, te digo cómo se llama en México y dónde es más barata."*

---
Hecho con 🧡 por C-OG - Colmena 2026
