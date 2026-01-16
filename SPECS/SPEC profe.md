# SPEC: App de Gestión para Profesores Universitarios

> Documento de especificaciones v1.0

---

## 1. Problema

### Los 5 Dolores Principales del Profesor Universitario

| # | Dolor | Lo que piensa el profe |
|---|-------|------------------------|
| 1 | **Tiempo perdido** | "Paso más tiempo en papeleo que enseñando" |
| 2 | **Dispersión de información** | "Tengo todo regado en 10 lugares diferentes" |
| 3 | **Comunicación invadida** | "Los alumnos me escriben al WhatsApp a cualquier hora" |
| 4 | **Herramientas complicadas** | "Es más fácil seguir con mi Excel" |
| 5 | **Doble captura** | "Al final tengo que pasarlo todo al sistema de la universidad" |

### Situación Actual

La mayoría de los profesores universitarios usan una combinación improvisada de:

- **Excel** → para calificaciones
- **WhatsApp** → para comunicación (invadiendo su privacidad)
- **Correo electrónico** → para recibir tareas
- **Papel** → para pasar lista
- **Google Drive** → para almacenar todo

**El problema:** Todo está disperso, nada se conecta, y pierden mucho tiempo.

### Dolores al Usar Herramientas Existentes

| Dolor | Descripción |
|-------|-------------|
| Curva de aprendizaje | Interfaces complicadas, demasiadas funciones innecesarias |
| Dependencia de internet | La app no carga en el salón, pérdida de datos |
| Costo | Suscripciones anuales que el profe paga de su bolsillo |
| Fragmentación | Una app para cada cosa, nada se conecta |
| Compatibilidad | El sistema de la universidad no acepta los formatos |
| Adopción | Los alumnos no usan la plataforma, terminan en WhatsApp |

---

## 2. Solución

### Propuesta de Valor

Una **app única, modular y offline-first** que centraliza la gestión del profesor universitario sin complicaciones.

### Características Clave

| Característica | Por qué importa |
|----------------|-----------------|
| **Simple** | Que lo aprenda en 10 minutos |
| **Todo en uno** | Sin brincar entre apps |
| **Offline primero** | Funciona sin internet, sincroniza después |
| **Comunicación con límites** | Avisos sin dar tu WhatsApp personal |
| **Exportación fácil** | Compatible con el sistema de la universidad |
| **Económico** | Gratis o muy barato |
| **Modular** | Activa solo lo que necesitas |

---

## 3. Usuarios

### Una App, Dos Roles

```
APP
 │
 ├── Login como PROFE → Ve interfaz de profe
 │
 └── Login como ALUMNO → Ve interfaz de alumno
```

### Autenticación

- Login con correo institucional (@universidad.edu.mx)
- El dominio o selección al registro define el rol
- Login persistente (una vez y ya)

### Permisos por Rol

| Función | Profe | Alumno |
|---------|:-----:|:------:|
| Generar QR de asistencia | ✅ | ❌ |
| Escanear QR | ❌ | ✅ |
| Ver lista de asistencia del grupo | ✅ | ❌ |
| Ver MI historial de asistencia | ❌ | ✅ |
| Capturar calificaciones | ✅ | ❌ |
| Ver MIS calificaciones | ❌ | ✅ |
| Enviar avisos | ✅ | ❌ |
| Recibir avisos | ❌ | ✅ |
| Subir tareas | ❌ | ✅ |
| Recibir/calificar tareas | ✅ | ❌ |
| Exportar reportes | ✅ | ❌ |

### Roles Futuros (Escalabilidad)

- **Coordinador:** Ve reportes de múltiples profesores
- **Admin institucional:** Gestiona usuarios y configuración global

---

## 4. Arquitectura

### Principios de Diseño

| Principio | Descripción |
|-----------|-------------|
| **Modular** | Cada función es un módulo independiente |
| **Agregar no rompe** | Nuevos módulos no afectan los existentes |
| **Quitar no rompe** | Desactivar módulos no afecta el resto |
| **Offline-first** | Funciona sin internet, sincroniza cuando hay conexión |
| **Una sola app** | Dos interfaces según el rol del usuario |

### Estructura Modular

```
APP BASE (login + perfil + grupos)
   │
   ├── 📋 Módulo ASISTENCIA
   │
   ├── 📊 Módulo CALIFICACIONES
   │
   ├── 💬 Módulo COMUNICACIÓN
   │
   ├── 📁 Módulo TAREAS
   │
   ├── 📅 Módulo CALENDARIO
   │
   └── 📄 Módulo REPORTES
```

### Core (Siempre Existe)

- Login / Registro
- Perfil de usuario
- Gestión de grupos / materias
- Vinculación profe ↔ alumno

**Todo lo demás es módulo opcional.**

### Requerimientos Técnicos

| Requerimiento | Especificación |
|---------------|----------------|
| **Plataformas** | iOS y Android (app nativa o React Native/Flutter) |
| **Offline** | Base de datos local que sincroniza con servidor |
| **Sincronización** | Cuando detecta conexión, sube cambios pendientes |
| **API** | REST o GraphQL, modular por función |
| **Base de datos** | Separación lógica por módulo |
| **Feature flags** | Activar/desactivar módulos sin actualizar app |

---

## 5. Módulos

### 5.1 Módulo: Asistencia

#### Descripción
Sistema de registro de asistencia mediante código QR dinámico.

#### Flujo Principal

```
1. PROFE abre app → genera QR de sesión
   - QR válido por la duración de la clase
   - QR cambia cada 2-3 minutos (anti-fraude)

2. ALUMNO escanea con su app:
   → ✅ Éxito: "Asistencia registrada 8:15am"
   → ❌ Error: "Error al registrar" (queda en log)
   → ⏰ Tarde: "Asistencia registrada 8:25am (retardo)"

3. PROFE ve en tiempo real:
   → 35/40 alumnos presentes
   → 3 retardos
   → 2 errores registrados
```

#### Mecánica del QR

- El celular del profe muestra el QR en el escritorio
- El alumno se para, escanea, regresa a su lugar
- Quien no escanea, no tiene asistencia
- Si falla el escaneo, queda registro del error (no puede reclamar después)

#### Configuraciones

| Opción | Descripción |
|--------|-------------|
| Ventana de asistencia | Ej: 8:00 - 8:10 |
| Ventana de retardo | Ej: 8:11 - 8:20 |
| Después de ventana | No se puede escanear |
| QR de salida (opcional) | Para clases largas |

#### Datos que Registra

- ID del alumno
- ID de la sesión/clase
- Timestamp exacto
- Status (presente, retardo, error)
- Log de errores

---

### 5.2 Módulo: Calificaciones

#### Descripción
Registro y cálculo de calificaciones por materia.

#### Funcionalidades Profe

- Crear rubros (exámenes, tareas, participación, proyectos)
- Asignar ponderaciones (ej: exámenes 40%, tareas 30%, etc.)
- Capturar calificaciones por alumno
- Cálculo automático de promedios
- Ver alumnos en riesgo de reprobar
- Exportar a Excel/CSV

#### Funcionalidades Alumno

- Ver sus calificaciones por materia
- Ver promedio actual
- Ver desglose por rubro

---

### 5.3 Módulo: Comunicación

#### Descripción
Sistema de avisos unidireccional (profe → alumnos) sin exponer datos personales.

#### Funcionalidades Profe

- Enviar aviso a todo el grupo
- Enviar aviso a alumno específico
- Programar avisos
- Ver confirmación de lectura (opcional)

#### Funcionalidades Alumno

- Recibir notificaciones push
- Ver historial de avisos
- Marcar como leído

#### Lo que NO es

- No es chat bidireccional
- No es WhatsApp
- El profe no recibe mensajes de alumnos (por diseño)

---

### 5.4 Módulo: Tareas

#### Descripción
Sistema de asignación y entrega de trabajos.

#### Funcionalidades Profe

- Crear tarea con descripción y fecha límite
- Recibir entregas
- Ver quién entregó y quién no
- Calificar entregas
- Dar retroalimentación

#### Funcionalidades Alumno

- Ver tareas pendientes
- Subir archivos (PDF, Word, imágenes)
- Ver fecha límite
- Ver calificación y retroalimentación

---

### 5.5 Módulo: Calendario

#### Descripción
Agenda compartida de eventos de la materia.

#### Eventos

- Fechas de exámenes
- Fechas de entrega de tareas
- Cambios de horario
- Días sin clase

#### Funcionalidades

- Profe crea eventos
- Alumnos ven calendario
- Notificaciones de recordatorio

---

### 5.6 Módulo: Reportes

#### Descripción
Generación de documentos exportables.

#### Tipos de Reportes

| Reporte | Contenido |
|---------|-----------|
| Acta de calificaciones | Lista de alumnos con calificación final |
| Reporte de asistencia | Faltas y retardos por alumno |
| Boleta individual | Desglose de calificaciones de un alumno |
| Resumen de grupo | Estadísticas generales |

#### Formatos de Exportación

- PDF
- Excel (.xlsx)
- CSV

---

## 6. Flujos Principales

### 6.1 Flujo: Registro de Usuario

```
1. Usuario descarga app
2. Selecciona "Crear cuenta"
3. Ingresa correo institucional
4. Recibe código de verificación
5. Selecciona rol (Profesor / Alumno)
6. Completa perfil básico
7. Accede a la app
```

### 6.2 Flujo: Profe Crea Grupo

```
1. Profe va a "Mis grupos"
2. Toca "Crear grupo"
3. Ingresa: nombre de materia, horario, semestre
4. Sistema genera código de grupo (ej: "CAL-2025-A7B3")
5. Profe comparte código con alumnos
```

### 6.3 Flujo: Alumno se Une a Grupo

```
1. Alumno va a "Unirse a grupo"
2. Ingresa código del grupo
3. Sistema valida código
4. Alumno aparece en lista del profe
```

### 6.4 Flujo: Tomar Asistencia (QR)

```
1. Profe abre grupo → "Tomar asistencia"
2. App genera QR dinámico en pantalla
3. Profe coloca celular en escritorio
4. Alumnos se levantan y escanean (primeros 5-10 min)
5. App registra: éxito, retardo o error
6. Profe ve lista en tiempo real
7. Al cerrar sesión, asistencia queda guardada
```

### 6.5 Flujo: Capturar Calificaciones

```
1. Profe abre grupo → "Calificaciones"
2. Selecciona rubro (ej: "Examen 1")
3. Ve lista de alumnos
4. Ingresa calificación por alumno
5. Sistema calcula promedios automáticamente
6. Datos se sincronizan al servidor
```

---

## 7. Requerimientos No Funcionales

### Rendimiento

| Métrica | Objetivo |
|---------|----------|
| Tiempo de carga inicial | < 3 segundos |
| Escaneo de QR | < 1 segundo |
| Sincronización | Transparente, en background |

### Seguridad

- Autenticación con tokens JWT
- Datos encriptados en tránsito (HTTPS)
- Datos sensibles encriptados en reposo
- Sesiones con expiración

### Disponibilidad

- Funciona 100% offline para funciones críticas
- Sincroniza cuando hay conexión
- Manejo de conflictos de sincronización

### Compatibilidad

- iOS 13+
- Android 8+
- Diseño responsive para tablets

---

## 8. MVP (Versión Mínima Viable)

### Alcance del MVP

```
CORE
├── Login / Registro
├── Perfil de usuario
├── Crear / unirse a grupos
└── Vinculación profe ↔ alumno

MÓDULO ASISTENCIA
├── Generar QR dinámico (profe)
├── Escanear QR (alumno)
├── Registro de asistencia con timestamp
├── Log de errores
├── Vista de asistencia en tiempo real (profe)
└── Historial de asistencia (alumno)
```

### Fuera del MVP

- Calificaciones
- Comunicación/Avisos
- Tareas
- Calendario
- Reportes

### Criterios de Éxito del MVP

| Métrica | Objetivo |
|---------|----------|
| Tiempo para tomar asistencia | < 2 minutos por grupo |
| Tasa de adopción | 80% de alumnos escanean en primera semana |
| Errores de escaneo | < 5% |
| Satisfacción del profe | "Más fácil que pasar lista tradicional" |

---

## 9. Roadmap

| Fase | Versión | Contenido | Tiempo Estimado |
|------|---------|-----------|-----------------|
| **MVP** | v1.0 | Core + Asistencia | 2-3 meses |
| **Fase 2** | v1.1 | + Calificaciones | +1-2 meses |
| **Fase 3** | v1.2 | + Comunicación/Avisos | +1 mes |
| **Fase 4** | v2.0 | + Tareas | +2 meses |
| **Fase 5** | v2.5 | + Calendario | +1 mes |
| **Fase 6** | v3.0 | + Reportes + Exportación | +2 meses |
| **Fase 7** | v4.0 | Rol Admin + API institucional | +3 meses |

---

## 10. Fuera de Alcance (Por Ahora)

Esta app **NO es**:

| Excluido | Razón |
|----------|-------|
| LMS completo (como Moodle) | Demasiado complejo, diferente mercado |
| Videoconferencias | Ya existen Zoom, Meet, etc. |
| Chat bidireccional | Protege al profe de mensajes 24/7 |
| Sistema de pagos/cobranza | Fuera del scope del profesor |
| Gestión administrativa de la universidad | Otro producto |
| Red social educativa | No es el objetivo |

---

## 11. Modelo de Monetización (Futuro)

| Plan | Módulos | Precio Sugerido |
|------|---------|-----------------|
| **Gratis** | Core + Asistencia | $0 |
| **Básico** | + Calificaciones + Comunicación | $X/mes |
| **Pro** | Todo | $XX/mes |
| **Institucional** | Todo + Admin + API + Soporte | Cotización |

---

## 12. Preguntas Abiertas

- [ ] ¿Nombre de la app?
- [ ] ¿Tecnología de desarrollo? (React Native, Flutter, Nativo)
- [ ] ¿Backend propio o BaaS (Firebase, Supabase)?
- [ ] ¿Piloto con qué universidad/profesores?
- [ ] ¿Integración con sistemas universitarios existentes?

---

## Historial de Cambios

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2025-01-16 | Documento inicial |

---

*Documento generado como resultado de investigación y análisis de necesidades de profesores universitarios en México.*
