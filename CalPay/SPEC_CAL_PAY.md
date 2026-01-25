# SPEC: CalPay - Sistema de Citas con Pagos

## Resumen
Sistema de agendamiento de citas con verificación automática de pagos mediante Mercado Pago. Diseñado para profesionales independientes (psicólogos, médicos, coaches, etc).

## Problema
Los profesionales necesitan:
1. Mostrar disponibilidad a clientes
2. Permitir agendar citas online
3. Cobrar por adelantado
4. Confirmar automáticamente al recibir pago
5. Notificar a ambas partes

Soluciones existentes (Calendly, Cal.com) cobran $12-20 USD/mes por integrar pagos.

## Solución
App standalone que integra calendario + Mercado Pago con webhooks para confirmación automática. Costo: $0 (tiers gratuitos).

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js)                    │
├─────────────────────────────────────────────────────────┤
│  /                  Landing + Servicios                  │
│  /agendar           Calendario + Formulario              │
│  /pago/[id]         Checkout Mercado Pago                │
│  /confirmado        Página de confirmación               │
│  /admin             Panel administrador (protegido)      │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   API ROUTES (Next.js)                   │
├─────────────────────────────────────────────────────────┤
│  /api/servicios     GET lista de servicios               │
│  /api/disponibilidad GET horarios libres por fecha       │
│  /api/citas         POST crear cita pendiente            │
│  /api/pago          POST crear preferencia MP            │
│  /api/webhook/mp    POST recibir notificación MP         │
│  /api/admin/*       CRUD admin (auth required)           │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   DATABASE (Supabase)                    │
├─────────────────────────────────────────────────────────┤
│  servicios    │ id, nombre, duracion_min, precio, activo │
│  horarios     │ id, dia_semana, hora_inicio, hora_fin    │
│  citas        │ id, servicio_id, fecha, hora, cliente_*, │
│               │ estado (pendiente/pagado/cancelado),     │
│               │ mp_preference_id, mp_payment_id          │
│  config       │ key, value (emails, tokens, etc)         │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   SERVICIOS EXTERNOS                     │
├─────────────────────────────────────────────────────────┤
│  Mercado Pago  │ Checkout Pro + Webhooks                 │
│  Resend        │ Emails transaccionales                  │
│  Google Cal    │ Sync bidireccional (opcional)           │
└─────────────────────────────────────────────────────────┘
```

---

## Flujo de Usuario

### Cliente agenda cita:
```
1. Entra a /agendar
2. Selecciona servicio (ej: Psicoterapia Adultos)
3. Ve calendario con días disponibles
4. Click en día → ve horarios disponibles
5. Selecciona horario
6. Llena formulario (nombre, email, teléfono)
7. Click "Reservar y Pagar"
8. Redirect a checkout Mercado Pago
9. Paga (tarjeta/OXXO/transferencia)
10. Webhook confirma → cita PAGADA
11. Email de confirmación a cliente + admin
12. Redirect a /confirmado
```

### Admin gestiona:
```
1. Login en /admin
2. Ve dashboard con citas del día/semana
3. Puede ver/cancelar/reprogramar citas
4. Configura horarios de disponibilidad
5. Ve historial de pagos
```

---

## Base de Datos

### Tabla: servicios
```sql
CREATE TABLE servicios (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre TEXT NOT NULL,
  descripcion TEXT,
  duracion_min INT NOT NULL DEFAULT 50,
  precio DECIMAL(10,2) NOT NULL,
  activo BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Tabla: horarios
```sql
CREATE TABLE horarios (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  dia_semana INT NOT NULL, -- 0=domingo, 1=lunes, etc
  hora_inicio TIME NOT NULL,
  hora_fin TIME NOT NULL,
  activo BOOLEAN DEFAULT true
);
```

### Tabla: citas
```sql
CREATE TABLE citas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  servicio_id UUID REFERENCES servicios(id),
  fecha DATE NOT NULL,
  hora TIME NOT NULL,
  cliente_nombre TEXT NOT NULL,
  cliente_email TEXT NOT NULL,
  cliente_telefono TEXT,
  estado TEXT DEFAULT 'pendiente', -- pendiente, pagado, cancelado
  mp_preference_id TEXT,
  mp_payment_id TEXT,
  monto DECIMAL(10,2),
  notas TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  paid_at TIMESTAMPTZ
);
```

### Tabla: config
```sql
CREATE TABLE config (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
-- Valores: admin_email, mp_access_token, resend_api_key, etc
```

---

## API Endpoints

### GET /api/servicios
Retorna lista de servicios activos.

### GET /api/disponibilidad?fecha=2026-01-30
Retorna horarios disponibles para una fecha.
1. Obtiene horarios configurados para ese día de semana
2. Filtra los que ya tienen cita (estado != cancelado)
3. Retorna slots disponibles

### POST /api/citas
Crea cita con estado "pendiente".
```json
{
  "servicio_id": "uuid",
  "fecha": "2026-01-30",
  "hora": "10:00",
  "cliente_nombre": "Juan Pérez",
  "cliente_email": "juan@email.com",
  "cliente_telefono": "3221234567"
}
```
Retorna: { cita_id, redirect_url }

### POST /api/pago
Crea preferencia de Mercado Pago.
```json
{
  "cita_id": "uuid"
}
```
Retorna: { init_point } (URL checkout MP)

### POST /api/webhook/mp
Recibe notificaciones de Mercado Pago.
1. Valida firma
2. Si payment.status == "approved":
   - Actualiza cita.estado = "pagado"
   - Guarda mp_payment_id
   - Envía emails de confirmación

---

## Integraciones

### Mercado Pago
```javascript
// Crear preferencia
const preference = {
  items: [{
    title: "Psicoterapia Adultos",
    unit_price: 800,
    quantity: 1
  }],
  back_urls: {
    success: "https://app.com/confirmado",
    failure: "https://app.com/error",
    pending: "https://app.com/pendiente"
  },
  notification_url: "https://app.com/api/webhook/mp",
  external_reference: cita_id
};
```

### Resend (Emails)
```javascript
// Email confirmación
await resend.emails.send({
  from: 'citas@dominio.com',
  to: cliente_email,
  subject: 'Cita Confirmada - Psic. Mariela',
  html: templateConfirmacion(cita)
});
```

---

## UI/UX

### Página /agendar
- Header con nombre del profesional
- Selector de servicio (cards)
- Calendario (mes actual + siguiente)
- Días con disponibilidad en verde
- Click en día → modal con horarios
- Formulario inline
- Botón "Reservar y Pagar"

### Estilos
- Colores: sage green (#627362), cream (#f5f5dc)
- Font: Inter o system
- Rounded corners
- Sombras sutiles
- Mobile-first

---

## Configuración Requerida

### Mercado Pago
1. Crear app en developers.mercadopago.com
2. Obtener Access Token (producción)
3. Configurar webhook URL

### Supabase
1. Crear proyecto
2. Ejecutar SQL de tablas
3. Obtener URL + anon key

### Resend
1. Crear cuenta
2. Verificar dominio (o usar @resend.dev)
3. Obtener API key

### Vercel
1. Conectar repo
2. Agregar env vars:
   - SUPABASE_URL
   - SUPABASE_ANON_KEY
   - MP_ACCESS_TOKEN
   - RESEND_API_KEY
   - ADMIN_PASSWORD

---

## MVP (Fase 1)

### Incluye:
- [ ] Landing con servicios
- [ ] Calendario funcional
- [ ] Disponibilidad real (sin Google Cal)
- [ ] Formulario de reserva
- [ ] Checkout Mercado Pago
- [ ] Webhook confirmación
- [ ] Email básico de confirmación
- [ ] Página /confirmado

### No incluye (Fase 2):
- Panel admin visual
- Google Calendar sync
- Recordatorios automáticos
- Cancelación/reprogramación online
- Múltiples profesionales

---

## Tiempo Estimado

| Fase | Tarea | Tiempo |
|------|-------|--------|
| 1 | Setup proyecto + DB | 2h |
| 1 | UI calendario | 3h |
| 1 | API disponibilidad | 2h |
| 1 | Integración MP | 3h |
| 1 | Webhook + emails | 2h |
| 1 | Testing + deploy | 2h |
| **Total MVP** | | **~14h** |

---

## Nombres de dominio sugeridos
- citas.psicmarielapm.com (subdominio)
- agenda.psicmarielapm.com
- o como app separada: calpay.duendes.app

---

## Siguiente Paso
1. Crear repo: github.com/Pvrolomx/cal-pay
2. Setup Next.js + Supabase
3. Crear tablas
4. Implementar MVP
