# LEGAL-SOLUTIONS SPEC v1.0

## 🎯 Visión General

Sistema de gestión para despachos jurídicos pequeños y medianos. Una sola aplicación web (Next.js) con experiencia optimizada para PC (captura/organización) y móvil (consulta rápida). Desplegable como PWA.

---

## 📱 Filosofía: Una App, Dos Experiencias

```
PC (Oficina)              NUBE              Móvil (Campo)
┌─────────────┐      ┌──────────┐      ┌─────────────┐
│ • Capturar  │      │          │      │ • Consultar │
│ • Organizar │ ───► │ Postgres │ ◄─── │ • Copiar    │
│ • Subir docs│      │          │      │ • Ver docs  │
│ • Config    │      └──────────┘      │ • Alertas   │
└─────────────┘                        └─────────────┘
```

| Acción | PC | Móvil |
|--------|:--:|:-----:|
| Capturar clientes | ✓✓ | ✓ |
| Subir documentos | ✓✓ | Cámara |
| Buscar/consultar | ✓ | ✓✓ |
| Copiar datos | ✓ | ✓✓ |
| Ver documentos | ✓✓ | ✓ |
| Capturar términos | ✓✓ | ✓ |
| Configuración | ✓✓ | Mínima |

---

## 🗂️ Módulos

### 1. CLIENTES
Gestión completa de clientes del despacho.

**Campos:**
- Nombre completo / Razón social
- RFC
- CURP
- Teléfono(s)
- Email
- Dirección completa
- Notas
- Fecha de alta
- Estado (Activo/Inactivo)

**Funcionalidades:**
- CRUD completo
- Búsqueda rápida por nombre/RFC
- Botón "Copiar" en cada campo (móvil)
- Historial de expedientes relacionados

---

### 2. EXPEDIENTES
Casos/asuntos legales vinculados a clientes.

**Campos:**
- Número de expediente
- Cliente (relación)
- Tipo (Civil, Penal, Familiar, Mercantil, Laboral, Amparo, Administrativo)
- Juzgado/Autoridad
- Contraparte
- Descripción/Objeto
- Estado (Activo, En trámite, Suspendido, Concluido, Archivado)
- Fecha de inicio
- Fecha de conclusión
- Notas

**Funcionalidades:**
- CRUD completo
- Filtros por tipo, estado, cliente
- Timeline de actuaciones
- Documentos adjuntos

---

### 3. DOCUMENTOS
Archivos relacionados a expedientes.

**Campos:**
- Nombre del documento
- Expediente (relación)
- Tipo (Demanda, Contestación, Auto, Sentencia, Promoción, Acuerdo, Otro)
- Archivo (PDF, imagen, Word)
- Fecha del documento
- Fecha de carga
- Notas

**Funcionalidades:**
- Upload drag & drop (PC)
- Captura con cámara (móvil)
- Visor de PDF inline
- Descarga
- Organización por carpetas/etiquetas

---

### 4. TÉRMINOS
Control de plazos y vencimientos.

**Campos:**
- Título
- Expediente (relación)
- Fecha de vencimiento
- Tipo (Fatal, Procesal, Convencional)
- Días de anticipación para alerta
- Estado (Pendiente, Cumplido, Vencido)
- Descripción
- Recordatorio activado (sí/no)

**Funcionalidades:**
- Calendario visual
- Lista de próximos vencimientos
- Alertas push (PWA)
- Notificación por email (opcional)
- Dashboard de términos críticos

---

### 5. AGENDA
Citas y eventos del despacho.

**Campos:**
- Título
- Fecha y hora
- Duración
- Lugar
- Cliente (opcional)
- Expediente (opcional)
- Tipo (Audiencia, Cita cliente, Diligencia, Reunión, Otro)
- Notas
- Recordatorio

**Funcionalidades:**
- Vista calendario (mes/semana/día)
- Lista de eventos del día
- Sincronización con Google Calendar (futuro)

---

### 6. CONFIGURACIÓN
Ajustes del sistema.

**Opciones:**
- Datos del despacho (nombre, dirección, logo)
- Usuarios y permisos
- Tipos personalizados (expedientes, documentos)
- Preferencias de notificación
- Backup/Export de datos

---

## 🗄️ Modelo de Datos (Prisma)

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  password  String
  role      Role     @default(USER)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

enum Role {
  ADMIN
  USER
  VIEWER
}

model Cliente {
  id           String       @id @default(cuid())
  nombre       String
  rfc          String?
  curp         String?
  telefono     String?
  telefono2    String?
  email        String?
  direccion    String?
  notas        String?
  activo       Boolean      @default(true)
  createdAt    DateTime     @default(now())
  updatedAt    DateTime     @updatedAt
  expedientes  Expediente[]
  eventos      Evento[]
}

model Expediente {
  id           String       @id @default(cuid())
  numero       String       @unique
  clienteId    String
  cliente      Cliente      @relation(fields: [clienteId], references: [id])
  tipo         TipoExpediente
  juzgado      String?
  contraparte  String?
  descripcion  String?
  estado       EstadoExpediente @default(ACTIVO)
  fechaInicio  DateTime     @default(now())
  fechaFin     DateTime?
  notas        String?
  createdAt    DateTime     @default(now())
  updatedAt    DateTime     @updatedAt
  documentos   Documento[]
  terminos     Termino[]
  eventos      Evento[]
}

enum TipoExpediente {
  CIVIL
  PENAL
  FAMILIAR
  MERCANTIL
  LABORAL
  AMPARO
  ADMINISTRATIVO
  OTRO
}

enum EstadoExpediente {
  ACTIVO
  EN_TRAMITE
  SUSPENDIDO
  CONCLUIDO
  ARCHIVADO
}

model Documento {
  id           String       @id @default(cuid())
  nombre       String
  expedienteId String
  expediente   Expediente   @relation(fields: [expedienteId], references: [id])
  tipo         TipoDocumento
  archivoUrl   String
  archivoKey   String
  fechaDoc     DateTime?
  notas        String?
  createdAt    DateTime     @default(now())
  updatedAt    DateTime     @updatedAt
}

enum TipoDocumento {
  DEMANDA
  CONTESTACION
  AUTO
  SENTENCIA
  PROMOCION
  ACUERDO
  CONTRATO
  PODER
  IDENTIFICACION
  OTRO
}

model Termino {
  id             String       @id @default(cuid())
  titulo         String
  expedienteId   String
  expediente     Expediente   @relation(fields: [expedienteId], references: [id])
  fechaVencimiento DateTime
  tipo           TipoTermino
  diasAlerta     Int          @default(3)
  estado         EstadoTermino @default(PENDIENTE)
  descripcion    String?
  recordatorio   Boolean      @default(true)
  createdAt      DateTime     @default(now())
  updatedAt      DateTime     @updatedAt
}

enum TipoTermino {
  FATAL
  PROCESAL
  CONVENCIONAL
}

enum EstadoTermino {
  PENDIENTE
  CUMPLIDO
  VENCIDO
}

model Evento {
  id           String       @id @default(cuid())
  titulo       String
  fecha        DateTime
  duracion     Int?         // minutos
  lugar        String?
  clienteId    String?
  cliente      Cliente?     @relation(fields: [clienteId], references: [id])
  expedienteId String?
  expediente   Expediente?  @relation(fields: [expedienteId], references: [id])
  tipo         TipoEvento
  notas        String?
  recordatorio Boolean      @default(true)
  createdAt    DateTime     @default(now())
  updatedAt    DateTime     @updatedAt
}

enum TipoEvento {
  AUDIENCIA
  CITA_CLIENTE
  DILIGENCIA
  REUNION
  OTRO
}
```

---

## 📱 Pantallas

### PC (Desktop)

```
┌─────────────────────────────────────────────────────────┐
│  🏛️ Legal-Solutions              [Buscar...]    [User] │
├────────────┬────────────────────────────────────────────┤
│            │                                            │
│  Dashboard │   [Contenido principal]                    │
│  Clientes  │                                            │
│  Expedientes│   - Tablas con filtros                    │
│  Documentos│   - Formularios completos                  │
│  Términos  │   - Vista detalle                          │
│  Agenda    │                                            │
│  Config    │                                            │
│            │                                            │
└────────────┴────────────────────────────────────────────┘
```

### Móvil

```
┌─────────────────────┐
│  🏛️ Legal-Solutions │
│  [🔍 Buscar...]     │
├─────────────────────┤
│                     │
│  [Contenido]        │
│                     │
│  - Cards compactas  │
│  - Botones copiar   │
│  - Swipe actions    │
│                     │
│                     │
├─────────────────────┤
│ 🏠  📁  📄  ⏰  📅  │
└─────────────────────┘
   Bottom navigation
```

---

## 🔄 Flujos de Usuario

### Flujo 1: Alta de caso nuevo (PC)

```
1. Sidebar > Clientes > + Nuevo
2. Llenar formulario completo
3. Guardar → Redirige a vista cliente
4. Botón "Crear expediente"
5. Llenar datos del expediente
6. Guardar → Redirige a expediente
7. Drag & drop documentos
8. Agregar términos importantes
```

### Flujo 2: Consulta en juzgado (Móvil)

```
1. Abrir app
2. Buscar "García" en búsqueda global
3. Ver expediente en resultados
4. Tap para ver detalle
5. Copiar número de expediente
6. Ver último documento (auto)
7. Verificar próximo término
```

### Flujo 3: Alerta de término

```
1. Sistema detecta término a 3 días
2. Push notification (PWA)
3. Email al usuario (opcional)
4. Badge en menú "Términos"
5. Card destacada en Dashboard
6. Usuario marca como "Cumplido"
```

---

## 🛠️ Stack Técnico

| Capa | Tecnología |
|------|------------|
| Frontend | Next.js 14 (App Router) |
| Estilos | Tailwind CSS |
| Componentes | shadcn/ui |
| Base de datos | PostgreSQL (Neon/Supabase) |
| ORM | Prisma |
| Autenticación | NextAuth.js |
| Archivos | UploadThing / S3 |
| Deploy | Vercel |
| PWA | next-pwa |

---

## 📋 Prioridades de Desarrollo

### Fase 1: MVP (Core)
1. ✅ Setup proyecto Next.js + Prisma + Auth
2. ✅ CRUD Clientes
3. ✅ CRUD Expedientes
4. ✅ Upload Documentos básico
5. ✅ Responsive básico

### Fase 2: Funcionalidad Completa
6. ⬜ Términos con alertas
7. ⬜ Agenda/Calendario
8. ⬜ Búsqueda global
9. ⬜ Dashboard con métricas

### Fase 3: Optimización Móvil
10. ⬜ Bottom navigation móvil
11. ⬜ Botones "Copiar" optimizados
12. ⬜ Visor PDF móvil
13. ⬜ PWA (instalable)

### Fase 4: Extras
14. ⬜ Notificaciones push
15. ⬜ Email reminders
16. ⬜ Export/Backup
17. ⬜ Multi-usuario con roles

---

## 📝 Notas de Implementación

### PWA Setup
```javascript
// next.config.js
const withPWA = require('next-pwa')({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development'
})

module.exports = withPWA({
  // config
})
```

### Estructura de carpetas sugerida
```
/app
  /api
    /clientes
    /expedientes
    /documentos
    /terminos
    /eventos
  /(auth)
    /login
    /register
  /(dashboard)
    /page.tsx          # Dashboard
    /clientes
    /expedientes
    /documentos
    /terminos
    /agenda
    /config
/components
  /ui                  # shadcn
  /forms
  /tables
  /mobile
/lib
  /prisma.ts
  /auth.ts
  /utils.ts
/prisma
  /schema.prisma
```

---

## 🚀 Para Empezar

```bash
# 1. Clonar/crear proyecto
npx create-next-app@latest legal-solutions

# 2. Instalar dependencias
npm install prisma @prisma/client next-auth
npm install -D tailwindcss postcss autoprefixer

# 3. Configurar Prisma
npx prisma init
# Copiar schema de este SPEC

# 4. Configurar shadcn/ui
npx shadcn@latest init

# 5. Variables de entorno
DATABASE_URL="postgresql://..."
NEXTAUTH_SECRET="..."
NEXTAUTH_URL="http://localhost:3000"
```

---

*SPEC v1.0 - Enero 2026*
*Para asignar a nuevo proyecto Claude*
