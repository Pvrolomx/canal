# SPEC: [Nombre del Proyecto]

> Template: Dashboard/Admin Panel
> Tiempo estimado: 45-90 min

## Cliente
- **Nombre:** [Nombre]
- **Negocio:** [Negocio]

## Tipo
Dashboard administrativo con autenticación

## Autenticación
- **Tipo:** PIN / Email+Password / Solo password
- **Usuarios:** [Lista de usuarios o solo admin]

## Módulos
| Módulo | CRUD | Campos principales |
|--------|------|-------------------|
| [Ej: Clientes] | ✅ | nombre, tel, email |
| [Ej: Pedidos] | ✅ | fecha, cliente, total |
| [Ej: Productos] | ✅ | nombre, precio, stock |

## Vistas
- [ ] Dashboard home (resumen/stats)
- [ ] Lista de [módulo]
- [ ] Crear/Editar [módulo]
- [ ] Detalle de [módulo]

## Almacenamiento
- **Opción A:** localStorage (datos en dispositivo)
- **Opción B:** Supabase (nube, sync entre dispositivos)

## Funcionalidades extra
- [ ] Exportar a Excel/CSV
- [ ] Búsqueda y filtros
- [ ] Notificaciones
- [ ] Gráficas/estadísticas

## Estilo
- **Tema:** Claro / Oscuro / Auto
- **Colores:** [Colores]

## Dominio
[nombre].vercel.app

---
*Status: PENDIENTE | EN PROGRESO | DONE*
