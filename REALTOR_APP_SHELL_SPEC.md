# REALTOR APP - SPEC CAPARAZÓN v1.0
# Fecha: 2026-01-17
# Autor: C1 (Sleepy) - Consigliere
# Para: Claude ejecutor

## 1. VISION DEL PRODUCTO

NOMBRE: RealtorPV (o RealtorBahia)

PITCH: "CRM inteligente para agentes inmobiliarios de Bahía de Banderas"

TARGET USER: Agentes inmobiliarios de Puerto Vallarta y Bahía de Banderas

MODULOS:
1. Dashboard - Vista general
2. Comps - Generador de comparables (YA EXISTE)
3. Inventario - Gestión de propiedades
4. Clientes - CRM básico
5. Matcher - IA que conecta clientes con propiedades

## 2. ARQUITECTURA MODULAR

```
/                    -> Dashboard
/comps               -> Módulo Comps (existente)
/inventario          -> Módulo Inventario
/clientes            -> Módulo Clientes
/matcher             -> Módulo Matcher
/settings            -> Configuración
```

PRINCIPIO: Cada módulo es independiente.
Pueden construirse/actualizarse por separado.

## 3. STACK TECNOLOGICO

FRONTEND:
- Framework: Astro 5 + React
- Styling: Tailwind CSS
- Icons: Lucide
- Estado: React Context (simple)

BACKEND:
- API: Astro API routes
- AI: Claude API (para Comps y Matcher)

DATA:
- Storage: JSON files (MVP)
- Futuro: Supabase

DEPLOY:
- Hosting: Vercel
- Repo: github.com/Pvrolomx/realtor-app


## 4. ESTRUCTURA DE ARCHIVOS

```
realtor-app/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx        # Nav lateral
│   │   │   ├── Header.tsx         # Header con user
│   │   │   └── MobileNav.tsx      # Nav móvil
│   │   ├── dashboard/
│   │   │   ├── StatCard.tsx       # Card de estadística
│   │   │   └── QuickActions.tsx   # Acciones rápidas
│   │   ├── comps/                 # (MIGRAR DE REPO EXISTENTE)
│   │   │   ├── PropertyForm.tsx
│   │   │   ├── CompResults.tsx
│   │   │   └── CompCard.tsx
│   │   ├── inventario/
│   │   │   ├── PropertyList.tsx
│   │   │   ├── PropertyCard.tsx
│   │   │   └── PropertyForm.tsx
│   │   ├── clientes/
│   │   │   ├── ClientList.tsx
│   │   │   ├── ClientCard.tsx
│   │   │   └── ClientForm.tsx
│   │   └── matcher/
│   │       ├── MatchForm.tsx
│   │       └── MatchResults.tsx
│   ├── layouts/
│   │   └── AppLayout.astro        # Layout con sidebar
│   ├── pages/
│   │   ├── index.astro            # Dashboard
│   │   ├── comps.astro            # Módulo Comps
│   │   ├── inventario.astro       # Módulo Inventario
│   │   ├── clientes.astro         # Módulo Clientes
│   │   ├── matcher.astro          # Módulo Matcher
│   │   ├── settings.astro         # Settings
│   │   └── api/
│   │       ├── generate-comps.ts
│   │       ├── properties.ts
│   │       ├── clients.ts
│   │       └── match.ts
│   ├── lib/
│   │   ├── compEngine.ts
│   │   ├── matchEngine.ts
│   │   └── store.ts               # Estado global simple
│   └── data/
│       ├── properties.json
│       └── clients.json
├── public/
│   ├── manifest.json
│   └── icons/
└── astro.config.mjs
```

## 5. NAVEGACION (Sidebar)

```
┌─────────────────────┐
│  🏠 RealtorPV       │
├─────────────────────┤
│  📊 Dashboard       │  <- /
│  📈 Comps           │  <- /comps
│  🏢 Inventario      │  <- /inventario
│  👥 Clientes        │  <- /clientes
│  🎯 Matcher         │  <- /matcher
├─────────────────────┤
│  ⚙️ Settings        │  <- /settings
└─────────────────────┘
```

## 6. PAGINAS DETALLADAS

### 6.1 Dashboard (index.astro)
```
┌─────────────────────────────────────┐
│ Buenos días, Agente               🔔│
├─────────────────────────────────────┤
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │
│ │ 24  │ │ 12  │ │  5  │ │  3  │   │
│ │Props│ │Clien│ │Match│ │Comps│   │
│ └─────┘ └─────┘ └─────┘ └─────┘   │
├─────────────────────────────────────┤
│ ACCIONES RAPIDAS                    │
│ [Generar Comps] [Nuevo Cliente]     │
│ [Agregar Propiedad] [Ver Matches]   │
├─────────────────────────────────────┤
│ ACTIVIDAD RECIENTE                  │
│ • Comp generado: Casa Bucerias      │
│ • Nuevo cliente: Juan Pérez         │
│ • Match encontrado: Maria + Condo   │
└─────────────────────────────────────┘
```


### 6.2 Comps (comps.astro)
YA EXISTE en repo realtor-comps.
MIGRAR componentes:
- PropertyForm.tsx
- CompResults.tsx
- CompCard.tsx
- PriceAnalysis.tsx
- API: generate-comps.ts

### 6.3 Inventario (inventario.astro)
```
┌─────────────────────────────────────┐
│ Inventario              [+ Agregar] │
├─────────────────────────────────────┤
│ Filtros: [Tipo ▼] [Zona ▼] [Precio] │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │ 🏠 Casa Mar Azul                │ │
│ │ Bucerias | 3BD/2BA | $450,000   │ │
│ │ [Ver] [Editar] [Comps]          │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 🏢 Condo Torre Naomi            │ │
│ │ Bucerias | 2BD/2BA | $425,000   │ │
│ │ [Ver] [Editar] [Comps]          │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### 6.4 Clientes (clientes.astro)
```
┌─────────────────────────────────────┐
│ Clientes                [+ Agregar] │
├─────────────────────────────────────┤
│ Buscar: [________________] 🔍       │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │ 👤 Juan Pérez                   │ │
│ │ Busca: Condo 2BD | $400-500k    │ │
│ │ Zona: Bucerias, Flamingos       │ │
│ │ [Ver] [Editar] [Matcher]        │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### 6.5 Matcher (matcher.astro)
```
┌─────────────────────────────────────┐
│ Matcher IA                          │
├─────────────────────────────────────┤
│ Selecciona cliente:                 │
│ [Juan Pérez                    ▼]   │
├─────────────────────────────────────┤
│ Preferencias:                       │
│ • Tipo: Condo                       │
│ • Budget: $400k - $500k            │
│ • Zona: Bucerias, Flamingos        │
│ • Must have: Pool, Vista mar       │
├─────────────────────────────────────┤
│         [🎯 Encontrar Matches]      │
├─────────────────────────────────────┤
│ RESULTADOS:                         │
│ ┌─────────────────────────────────┐ │
│ │ 95% Match - Condo Torre Naomi   │ │
│ │ $425k | 2BD | Pool, Vista ✓     │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 87% Match - Casa Mar Azul       │ │
│ │ $450k | 3BD | Pool ✓ Vista ✓    │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```


## 7. MODELOS DE DATOS

### properties.json
```json
{
  "properties": [
    {
      "id": "prop_001",
      "mls_id": "POC001",
      "name": "Condo Torre Naomi 301",
      "type": "Condominio",
      "region": "Bucerias",
      "price_usd": 425000,
      "bedrooms": 2,
      "bathrooms": 2,
      "m2_construction": 98,
      "features": ["pool", "ac", "ocean_view"],
      "status": "Disponible",
      "created_at": "2026-01-17"
    }
  ]
}
```

### clients.json
```json
{
  "clients": [
    {
      "id": "cli_001",
      "name": "Juan Pérez",
      "email": "juan@email.com",
      "phone": "+52 322 123 4567",
      "preferences": {
        "type": ["Condominio", "Casa"],
        "regions": ["Bucerias", "Flamingos"],
        "budget_min": 400000,
        "budget_max": 500000,
        "bedrooms_min": 2,
        "must_have": ["pool", "ocean_view"]
      },
      "status": "Activo",
      "created_at": "2026-01-17"
    }
  ]
}
```

## 8. API ENDPOINTS

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| /api/generate-comps | POST | Generar comps (existente) |
| /api/properties | GET | Listar propiedades |
| /api/properties | POST | Agregar propiedad |
| /api/properties/[id] | PUT | Editar propiedad |
| /api/properties/[id] | DELETE | Eliminar propiedad |
| /api/clients | GET | Listar clientes |
| /api/clients | POST | Agregar cliente |
| /api/clients/[id] | PUT | Editar cliente |
| /api/clients/[id] | DELETE | Eliminar cliente |
| /api/match | POST | Ejecutar matcher IA |

## 9. UI/UX GUIDELINES

COLORES:
- Primary: #2563eb (blue-600)
- Secondary: #059669 (emerald-600)
- Sidebar: #1e293b (slate-800)
- Background: #f8fafc (slate-50)

RESPONSIVE:
- Desktop: Sidebar fijo + contenido
- Mobile: Hamburger menu + contenido full

COMPONENTES REUTILIZABLES:
- Card (para propiedades y clientes)
- Form (campos consistentes)
- Button (primary, secondary, danger)
- Badge (status, match score)
- Modal (confirmaciones, forms)


## 10. ORDEN DE CONSTRUCCION

FASE 1 - CAPARAZON (2 horas):
1. Crear proyecto Astro + React + Tailwind
2. AppLayout con Sidebar
3. Dashboard básico con stats hardcodeados
4. Navegación funcionando
5. Deploy inicial

FASE 2 - MIGRAR COMPS (30 min):
1. Copiar componentes de realtor-comps
2. Integrar en /comps
3. Verificar que funciona

FASE 3 - INVENTARIO (1 hora):
1. PropertyList + PropertyCard
2. PropertyForm (agregar/editar)
3. API CRUD
4. Filtros básicos

FASE 4 - CLIENTES (1 hora):
1. ClientList + ClientCard
2. ClientForm
3. API CRUD
4. Búsqueda

FASE 5 - MATCHER (1 hora):
1. MatchForm (seleccionar cliente)
2. MatchResults
3. API con Claude
4. Integrar con datos existentes

## 11. CRITERIOS DE ACEPTACION

MVP COMPLETO CUANDO:
- [ ] Dashboard muestra stats
- [ ] Sidebar navega correctamente
- [ ] Comps funciona (migrado)
- [ ] CRUD de propiedades
- [ ] CRUD de clientes
- [ ] Matcher básico funciona
- [ ] Mobile responsive
- [ ] PWA instalable
- [ ] Footer: "Hecho con ❤️ por Colmena 2026"
- [ ] Deploy en Vercel

## 12. REFERENCIA

REPO COMPS EXISTENTE:
- GitHub: github.com/Pvrolomx/realtor-comps
- Live: https://realtor-comps.vercel.app
- Local: /home/pvrolo/colmena/apps/realtor-comps

PROPERTIES DATA:
- Usar: C:/Users/pvrol/colmena/scrapers/poc_properties.json

## 13. NOTAS PARA EJECUTOR

1. NO empezar de cero - MIGRAR de realtor-comps
2. Sidebar es crítico - la app vive o muere por la nav
3. Mobile first - muchos agentes usan celular
4. Matcher usa Claude API - mismo pattern que Comps
5. Commits frecuentes - ver RDE Cloud

---
FIN DEL SPEC CAPARAZON
Generado: 2026-01-17 16:30
Por: C1 (Sleepy) - Consigliere
