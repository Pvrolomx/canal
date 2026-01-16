# HANDOFF: App de Gestión para Profesores Universitarios

> Documento para continuar desarrollo en nueva conversación con Claude

---

## 🎯 Resumen Ejecutivo

Estamos construyendo una **app móvil para profesores universitarios en México** que resuelve sus principales dolores: tiempo perdido en papeleo, información dispersa, comunicación invadida (WhatsApp), herramientas complicadas y doble captura de datos.

**Enfoque:** Una sola app, dos roles (profe/alumno), arquitectura modular, offline-first.

---

## 📋 Decisiones Ya Tomadas

| Decisión | Elección |
|----------|----------|
| ¿Una o dos apps? | **Una app, dos roles** (login define la interfaz) |
| ¿Nube o local? | **Offline-first** (funciona sin internet, sincroniza después) |
| ¿Monolítico o modular? | **Modular** (agregar/quitar módulos no rompe nada) |
| ¿Cómo tomar asistencia? | **QR dinámico** en cel del profe, alumno escanea |
| ¿App o web para alumnos? | **App instalada** (más control, login persistente) |
| ¿MVP? | **Core + Asistencia** primero |

---

## 🧱 Arquitectura Definida

```
APP BASE (siempre existe)
├── Login / Registro
├── Perfil de usuario
├── Gestión de grupos / materias
└── Vinculación profe ↔ alumno

MÓDULOS (opcionales, escalables)
├── 📋 ASISTENCIA ← MVP
├── 📊 CALIFICACIONES ← Fase 2
├── 💬 COMUNICACIÓN ← Fase 3
├── 📁 TAREAS ← Fase 4
├── 📅 CALENDARIO ← Fase 5
└── 📄 REPORTES ← Fase 6
```

---

## 📱 MVP: Core + Asistencia

### Core
- Login/Registro con correo institucional
- Perfil de usuario (nombre, foto, rol)
- Crear grupo (profe)
- Unirse a grupo con código (alumno)
- Lista de alumnos por grupo

### Módulo Asistencia
- Profe genera QR dinámico (cambia cada 2-3 min)
- Alumno escanea con la app
- Registro con timestamp (presente, retardo, error)
- Vista en tiempo real para profe
- Historial de asistencia para alumno
- Log de errores (anti-reclamos)

---

## 🔄 Flujo de Asistencia (Detalle)

```
1. Profe abre grupo → "Tomar asistencia"
2. App genera QR dinámico en pantalla
3. Profe pone celular en escritorio
4. Alumnos se paran y escanean (5-10 min)
5. App registra: ✅ éxito | ⏰ retardo | ❌ error
6. Profe ve lista en tiempo real
7. Al cerrar, asistencia queda guardada
8. Sincroniza cuando hay internet
```

---

## 🎭 Permisos por Rol

| Función | Profe | Alumno |
|---------|:-----:|:------:|
| Crear grupo | ✅ | ❌ |
| Unirse a grupo | ❌ | ✅ |
| Generar QR asistencia | ✅ | ❌ |
| Escanear QR | ❌ | ✅ |
| Ver lista de asistencia del grupo | ✅ | ❌ |
| Ver MI historial de asistencia | ❌ | ✅ |

---

## 🔧 Requerimientos Técnicos

| Aspecto | Requerimiento |
|---------|---------------|
| Plataformas | iOS 13+ y Android 8+ |
| Offline | Base de datos local + sincronización |
| QR | Dinámico, cambia cada 2-3 minutos |
| Login | Correo institucional (Google/Microsoft) |
| Sincronización | Automática cuando detecta conexión |

---

## ❓ Decisiones Pendientes

| Pregunta | Opciones |
|----------|----------|
| ¿Nombre de la app? | Por definir |
| ¿Framework? | React Native / Flutter / Nativo |
| ¿Backend? | Propio (Node/Python) / Firebase / Supabase |
| ¿Base de datos local? | SQLite / Realm / WatermelonDB |
| ¿Diseño UI? | Por definir |

---

## 📄 Documentos Generados

1. **SPEC.md** - Especificaciones completas del producto
2. **HANDOFF.md** - Este documento

---

## 🚀 Próximos Pasos

1. **Definir stack técnico** (framework, backend, BD)
2. **Diseñar base de datos** (esquema para Core + Asistencia)
3. **Diseñar UI/UX** (wireframes o mockups)
4. **Construir MVP**
   - Autenticación
   - Gestión de grupos
   - Generación de QR
   - Escaneo de QR
   - Registro de asistencia
   - Sincronización offline

---

## 💬 Cómo Continuar

En la próxima conversación, comparte este archivo y di:

> "Estamos construyendo una app para profesores universitarios. Aquí está el handoff y el SPEC. Continuemos con [siguiente paso]."

Sugerencia de siguiente paso:
- "Definamos el stack técnico"
- "Diseñemos la base de datos"
- "Creemos los wireframes"
- "Empecemos a codear el MVP"

---

## 📊 Contexto de Negocio

| Aspecto | Detalle |
|---------|---------|
| Mercado | Profesores universitarios en México |
| Problema principal | Falta de internet confiable + herramientas dispersas |
| Diferenciador | Offline-first, simple, modular |
| Modelo de monetización | Freemium (Asistencia gratis, módulos premium) |

---

## 🔗 Archivos Relacionados

- `SPEC.md` - Especificaciones completas
- (Futuro) `DATABASE.md` - Esquema de base de datos
- (Futuro) `UI/` - Wireframes y mockups
- (Futuro) `/src` - Código fuente

---

*Última actualización: 2025-01-16*
