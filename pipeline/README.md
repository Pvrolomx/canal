# 🔄 Pipeline Autónomo - Colmena

Sistema de construcción autónoma de apps con handoff entre Claudes.

## Estructura

```
pipeline/
├── SPEC_TEMPLATE.md      # Template para nuevos specs
├── progress.json         # Estado actual del pipeline
├── pipeline_monitor.js   # Script de monitoreo (va en RPi)
└── SPEC_*.md            # Specs activos (crear para iniciar)
```

## Cómo Usar

### 1. Crear un SPEC
```bash
# Copiar template
cp SPEC_TEMPLATE.md SPEC_mi_app.md

# Editar con los detalles de la app
```

### 2. Iniciar Monitor (en RPi)
```bash
# Copiar a RPi
scp pipeline_monitor.js pvrolo@192.168.1.84:~/colmena/

# En RPi
cd ~/colmena
GITHUB_TOKEN=ghp_xxx node pipeline_monitor.js
```

### 3. El Pipeline Automáticamente:
1. Detecta nuevo SPEC
2. Trigger Claude A
3. Claude A ejecuta (actualiza progress.json)
4. Si Claude A se estanca (>10 min sin update)
5. Trigger Claude B para continuar
6. Deploy y verificación

## Estados del Pipeline

| Status | Descripción |
|--------|-------------|
| IDLE | Esperando SPEC |
| IN_PROGRESS | Claude trabajando |
| DEPLOYED | App live |
| VERIFIED | Smoke test pasó |
| ERROR | Algo falló |

## Stages

1. SPEC_READ - SPEC leído y entendido
2. REPO_CREATED - Repo GitHub creado
3. CODE_PUSHED - Código subido
4. VERCEL_CONFIGURED - Proyecto Vercel listo
5. DEPLOYED - App deployada
6. VERIFIED - Smoke test completado

## Configurar Agentes

En `pipeline_monitor.js`, editar:
```javascript
CLAUDE_AGENTS: [
  { name: "Claude_A", ip: "192.168.1.X", port: 9997 },
  { name: "Claude_B", ip: "192.168.1.Y", port: 9998 }
]
```

## Ejemplo de progress.json Activo

```json
{
  "spec_id": "APP_001",
  "spec_name": "MiApp",
  "status": "IN_PROGRESS",
  "current_agent": "Claude_A",
  "last_update": "2026-01-27T18:30:00Z",
  "stages": {
    "SPEC_READ": { "completed": true, "timestamp": "...", "agent": "Claude_A" },
    "REPO_CREATED": { "completed": true, "timestamp": "...", "agent": "Claude_A" },
    "CODE_PUSHED": { "completed": false, "timestamp": null, "agent": null }
  }
}
```

---
*Colmena 2026 - Pipeline Autónomo MVP*

