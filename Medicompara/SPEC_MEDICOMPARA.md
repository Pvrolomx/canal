# SPEC: MediCompara MX
## App de Comparación de Precios de Medicamentos USA → México

**Versión:** 1.0 MVP  
**Fecha:** Enero 2026  
**Autor:** C-OG / Colmena

---

## 1. RESUMEN EJECUTIVO

**Problema:** Adultos mayores expats estadounidenses en México no saben cómo se llaman sus medicamentos en español ni dónde comprarlos más barato.

**Solución:** App nativa que traduce nombres de medicamentos USA→México y compara precios entre farmacias.

**Usuario objetivo:** Expat estadounidense/canadiense, 65-80 años, viviendo en México (PV, Lake Chapala, San Miguel de Allende).

**Propuesta de valor:** "Escribe tu medicina gringa, te digo cómo se llama en México y dónde es más barata."

---

## 2. USUARIO PRIMARIO

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

## 3. MOMENTOS DE USO

| Momento | Dónde | Estado | Necesidad principal |
|---------|-------|--------|---------------------|
| Planificando | Casa, sentado | Tranquilo | "¿Cuánto me ahorro si compro aquí?" |
| Preparándose | Casa, antes de salir | Con prisa leve | "¿Cómo se llama? ¿Dónde voy?" |
| **En farmacia** | Mostrador | Parado, nervioso, sol en pantalla | "Que el empleado vea qué necesito" |
| Post-compra | Casa | Reflexivo | "¿Me cobraron bien?" |

**Momento crítico:** EN LA FARMACIA → El diseño debe optimizar para este momento.

---

## 4. ARQUITECTURA DE INFORMACIÓN

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
├── ❓ AYUDA / INFO
│   ├── FAQ (regla de 90 días, etc.)
│   ├── ¿Es seguro el genérico?
│   └── Contacto HCRPV (referido)
│
└── ⚙️ AJUSTES
    ├── Idioma (EN/ES)
    ├── Tamaño de letra
    └── Notificaciones
```

---

## 5. PANTALLAS DETALLADAS

### 5.1 HOME

```
┌─────────────────────────────────────┐
│  [Fondo: Farmacia mexicana típica]  │
│  [Overlay semi-transparente]        │
│                                     │
│         🇲🇽 MediCompara             │
│    "Tu medicina, mejor precio"      │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 🔍 Buscar medicina...       │   │  ← Input GRANDE
│  └─────────────────────────────┘   │
│                                     │
│   Recientes:                        │
│   • Lipitor 20mg                    │
│   • Metformin 850mg                 │
│                                     │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  💊 Mis Medicinas (5)       │   │  ← Botón prominente
│  │     Ver lista completa →     │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  📍 Farmacias Cerca         │   │
│  └─────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│  🏠    🔍    💊    📍    ⚙️        │  ← Tab bar
└─────────────────────────────────────┘
```

**Notas de diseño:**
- Fondo: Foto de farmacia mexicana colorida o calle típica con farmacia
- Overlay: 40-50% para legibilidad
- Búsqueda es la acción principal, debe dominar
- Máximo 2 taps para llegar a cualquier función

---

### 5.2 RESULTADO DE BÚSQUEDA

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
│  │                             │   │
│  │    ATORVASTATINA            │   │  ← Letra grande
│  │        20 mg                │   │
│  │                             │   │
│  │  [🔊 Escuchar]  [📋 Copiar] │   │
│  └─────────────────────────────┘   │
│                                     │
│  ✅ Mismo ingrediente activo        │  ← Badge de confianza
│  ✅ Aprobado por COFEPRIS           │
│                                     │
│  ════════════════════════════════   │
│                                     │
│  💰 Precios aproximados:            │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 🟢 Similares        $85 MXN │ ★ │  ← Más barato destacado
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ ⚪ Guadalajara     $110 MXN │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ ⚪ Del Ahorro      $120 MXN │   │
│  └─────────────────────────────┘   │
│                                     │
│  Precio USA: ~$350 MXN ($18 USD)    │
│  💵 Ahorras: ~$230 MXN (~75%)       │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  🏪 MODO FARMACIA           │   │  ← Botón principal
│  │  Mostrar al empleado        │   │
│  └─────────────────────────────┘   │
│                                     │
│  [💊 Guardar en mi lista]           │
│                                     │
├─────────────────────────────────────┤
│  🏠    🔍    💊    📍    ⚙️        │
└─────────────────────────────────────┘
```

**Notas de diseño:**
- El nombre mexicano debe ser lo MÁS VISIBLE
- Botón de audio para pronunciación correcta
- Badges de confianza reducen miedo
- Comparativa simple, el más barato arriba y destacado
- "Modo Farmacia" es CTA principal

---

### 5.3 MODO FARMACIA (Pantalla crítica)

```
┌─────────────────────────────────────┐
│                                     │
│  [Fondo blanco puro - máximo        │
│   contraste, sin distracciones]     │
│                                     │
│                                     │
│                                     │
│         ATORVASTATINA               │  ← Letra GIGANTE
│                                     │
│             20 mg                   │
│                                     │
│         ───────────                 │
│                                     │
│          Caja de 30                 │
│                                     │
│                                     │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  📱 Muestre esta pantalla   │   │
│  │     al farmacéutico         │   │
│  └─────────────────────────────┘   │
│                                     │
│                                     │
│           [ ✕ Cerrar ]              │
│                                     │
└─────────────────────────────────────┘
```

**Notas de diseño:**
- SIN navegación, SIN distracciones
- Fondo BLANCO (legible bajo el sol)
- Letra mínimo 48pt para el nombre
- El empleado debe poder leerlo a 1 metro
- Tap anywhere o botón X para cerrar
- Bloquear auto-sleep mientras está abierta

---

### 5.4 MIS MEDICINAS

```
┌─────────────────────────────────────┐
│  💊 Mis Medicinas       [+ Agregar] │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  💊 Atorvastatina           │   │
│  │     (Lipitor)               │   │
│  │     20mg · Noche            │   │
│  │                      $85 →  │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  💊 Metformina              │   │
│  │     (Glucophage)            │   │
│  │     850mg · Con comida      │   │
│  │                      $45 →  │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  💊 Lisinopril              │   │
│  │     (Prinivil)              │   │
│  │     10mg · Mañana           │   │
│  │                      $65 →  │   │
│  └─────────────────────────────┘   │
│                                     │
│  ════════════════════════════════   │
│                                     │
│  📊 RESUMEN MENSUAL                 │
│  ┌─────────────────────────────┐   │
│  │  Costo en USA:    $1,200    │   │
│  │  Costo en MX:       $195    │   │
│  │  ─────────────────────────  │   │
│  │  💰 AHORRAS:     $1,005     │   │  ← WOW moment
│  │     (84% menos)             │   │
│  └─────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│  🏠    🔍    💊    📍    ⚙️        │
└─────────────────────────────────────┘
```

**Notas de diseño:**
- Cada medicina es tappeable → va a resultado
- Swipe para eliminar
- Resumen de ahorro es el "WOW moment" emocional
- Posibilidad de compartir: "Mira cuánto ahorro"

---

### 5.5 FARMACIAS CERCA

```
┌─────────────────────────────────────┐
│  📍 Farmacias Cerca                 │
│                                     │
│  ┌─────────────────────────────┐   │
│  │                             │   │
│  │      [MAPA con pins]        │   │
│  │                             │   │
│  │   🟢 Similares              │   │
│  │   🔵 Guadalajara            │   │
│  │   🟡 Del Ahorro             │   │
│  │                             │   │
│  └─────────────────────────────┘   │
│                                     │
│  Filtrar: [Todas ▼]                 │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 🟢 Similares Fluvial        │   │
│  │    📍 450m · Abierta 24hrs  │   │
│  │    [Navegar]                │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 🔵 Guadalajara Centro       │   │
│  │    📍 800m · Cierra 10pm    │   │
│  │    [Navegar]                │   │
│  └─────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│  🏠    🔍    💊    📍    ⚙️        │
└─────────────────────────────────────┘
```

---

## 6. IDENTIDAD VISUAL

### 6.1 Concepto

**"México auténtico + Confianza médica"**

- Mexicanidad: Colores vibrantes, fotos reales de farmacias/calles mexicanas
- Confianza: Limpieza, claridad, profesionalismo médico
- Accesibilidad: Alto contraste, letra grande, simple

### 6.2 Paleta de colores

| Uso | Color | Código | Notas |
|-----|-------|--------|-------|
| Primario | Verde farmacia | #059669 | Confianza médica |
| Secundario | Azul profundo | #1e3a5f | Profesionalismo |
| Acento | Naranja mexicano | #f97316 | Destacar ahorros |
| Fondo | Blanco/Crema | #fafaf9 | Legibilidad |
| Texto | Gris oscuro | #1f2937 | Contraste |
| Éxito | Verde claro | #22c55e | Confirmaciones |
| Alerta | Rojo suave | #ef4444 | Advertencias |

### 6.3 Tipografía

| Uso | Familia | Tamaño | Peso |
|-----|---------|--------|------|
| Títulos | System (SF Pro / Roboto) | 24-32pt | Bold |
| Nombre medicina MX | System | 28-36pt | Bold |
| Modo Farmacia | System | 48-64pt | Bold |
| Cuerpo | System | 18-20pt | Regular |
| Mínimo legible | - | 16pt | - |

### 6.4 Fondos fotográficos

**Estilo:** Fotos reales de México, colores vibrantes, ambiente cálido.

**Opciones sugeridas:**
1. Fachada de farmacia mexicana colorida (verde cruz)
2. Calle de pueblo mágico con farmacia visible
3. Mostrador de farmacia tradicional
4. Plaza mexicana con comercios
5. Manos de adulto mayor con medicinas (emocional)

**Tratamiento:**
- Overlay de 40-50% con color primario
- Blur sutil en algunas pantallas
- Siempre priorizar legibilidad del contenido

---

## 7. INTERACCIONES CLAVE

### 7.1 Búsqueda
- Autocomplete mientras escribe
- Debounce de 300ms
- Mostrar "Buscando..." con spinner
- Resultado aparece con fade-in suave

### 7.2 Modo Farmacia
- Transición: slide-up fullscreen
- Auto-brightness al máximo
- Haptic feedback al abrir
- Prevent screen sleep mientras está activo

### 7.3 Guardar medicina
- Animación de "check" satisfactoria
- Haptic feedback de éxito
- Toast: "Guardada en tu lista"

---

## 8. ACCESIBILIDAD

| Requerimiento | Implementación |
|---------------|----------------|
| Texto escalable | Respetar configuración de sistema |
| Alto contraste | Ratio mínimo 4.5:1 |
| Touch targets | Mínimo 48x48pt |
| VoiceOver/TalkBack | Labels descriptivos |
| Daltonismo | No depender solo de color |

---

## 9. ESTADOS VACÍOS Y ERRORES

### Sin resultados
"No encontramos [búsqueda]. Intenta revisar la ortografía o buscar el nombre genérico."

### Lista vacía
"Tu lista está vacía. Busca una medicina y guárdala aquí para acceso rápido."

### Error de conexión
"Sin conexión. Tu lista guardada funciona sin internet."

---

## 10. MÉTRICAS DE ÉXITO

| Métrica | Objetivo MVP |
|---------|--------------|
| Búsquedas completadas | 80%+ encuentran resultado |
| Uso de Modo Farmacia | 50%+ de búsquedas exitosas |
| Medicinas guardadas | Promedio 3+ por usuario |
| Retención D7 | 40%+ |
| NPS | 50+ |

---

## 11. ROADMAP

### MVP (v1.0)
- [x] Búsqueda por nombre USA
- [x] Equivalente MX + pronunciación
- [x] Comparativa 4 farmacias
- [x] Modo Farmacia
- [x] Mi lista de medicinas
- [x] Mapa farmacias cercanas
- [x] EN/ES toggle

### v1.1
- [ ] Escaneo código de barras
- [ ] Notificaciones de resurtido

### v2.0
- [ ] Integración con HCRPV (recetas)
- [ ] Recordatorios de tomar medicina

---

**FIN DEL SPEC v1.0**

*"Escribe tu medicina gringa, te digo cómo se llama en México y dónde es más barata."*

---
Hecho con 🧡 por C-OG - Colmena 2026
