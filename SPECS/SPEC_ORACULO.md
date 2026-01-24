# 🔮 ORÁCULO - SPEC COMPLETO

## VISIÓN
Plataforma de chat AI multi-modelo. Competidor de ChatGPT/Claude/DeepSeek.

---

## OBJETIVO MVP
Chat funcional con Claude real, streaming, UI moderna.

---

## STACK TÉCNICO

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS
- **Deploy:** Vercel

### Backend (API)
- **Framework:** Next.js API Routes (mismo proyecto)
- **AI:** Anthropic API (Claude)
- **Deploy:** Vercel

### ¿Por qué Next.js?
- Un solo proyecto = un solo deploy
- API Routes integradas = sin CORS
- Vercel nativo = deploy automático

---

## ESTRUCTURA DEL PROYECTO

```
oraculo/
├── app/
│   ├── layout.tsx          # Layout principal
│   ├── page.tsx            # Chat UI
│   ├── globals.css         # Tailwind + estilos
│   └── api/
│       ├── health/route.ts # Health check
│       ├── models/route.ts # Lista de modelos
│       └── chat/route.ts   # Chat con streaming
├── components/
│   ├── ChatInput.tsx       # Input de mensaje
│   ├── ChatMessage.tsx     # Burbuja de mensaje
│   └── ModelSelector.tsx   # Selector de modelo
├── lib/
│   └── anthropic.ts        # Cliente Anthropic
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── next.config.js
```

---

## API ENDPOINTS

### GET /api/health
```json
{ "status": "ok", "version": "1.0.0" }
```

### GET /api/models
```json
{
  "models": [
    { "id": "claude-3-haiku", "name": "Claude 3 Haiku (Rápido)" },
    { "id": "claude-3-sonnet", "name": "Claude 3 Sonnet (Balanceado)" },
    { "id": "claude-3-opus", "name": "Claude 3 Opus (Potente)" }
  ]
}
```

### POST /api/chat
**Request:**
```json
{
  "messages": [
    { "role": "user", "content": "Hola!" }
  ],
  "model": "claude-3-haiku"
}
```

**Response:** Server-Sent Events (SSE) streaming
```
data: {"delta": {"content": "¡Hola"}}
data: {"delta": {"content": "! ¿"}}
data: {"delta": {"content": "Cómo"}}
data: [DONE]
```

---

## UI/UX

### Diseño
- Tema oscuro (fondo #0a0a0a)
- Sidebar izquierdo (historial - futuro)
- Área de chat central
- Input fijo en la parte inferior

### Colores
- Background: #0a0a0a
- Cards: #1a1a1a
- Border: #2a2a2a
- Primary: #6366f1 (indigo)
- Text: #ffffff

### Componentes
1. **Header:** Logo + selector de modelo
2. **ChatArea:** Lista de mensajes con scroll
3. **ChatInput:** Textarea + botón enviar
4. **Message:** Avatar + contenido + timestamp

---

## CREDENCIALES

### Anthropic API Key
- Buscar en chats anteriores
- Empieza con: sk-ant-api03-wxHK...
- Variable: ANTHROPIC_API_KEY

### OpenAI API Key (opcional, para multi-modelo futuro)
- Buscar en: https://platform.openai.com/api-keys
- Variable: OPENAI_API_KEY

### Vercel
- Token: Buscar en chats anteriores "HYf0..."
- Team ID: team_xmFW0blsjqFI5lwt29wBPi8Q

### GitHub
- Token: Buscar en chats anteriores "ghp_..."
- Repo: Pvrolomx/oraculo (borrar y recrear limpio)

---

## PASOS DE EJECUCIÓN

### 1. Preparación
```bash
# Buscar credenciales en chats anteriores
# - ANTHROPIC_API_KEY
# - GitHub token
# - Vercel token
```

### 2. Crear Proyecto
```bash
# Crear repo GitHub: oraculo
# Crear proyecto Next.js
npx create-next-app@latest oraculo --typescript --tailwind --app --src-dir=false
```

### 3. Implementar API
- /app/api/health/route.ts
- /app/api/models/route.ts  
- /app/api/chat/route.ts (con streaming SSE)

### 4. Implementar UI
- Componentes de chat
- Integración con API
- Streaming en frontend

### 5. Deploy
```bash
# Agregar ANTHROPIC_API_KEY como env var en Vercel
# Conectar repo a Vercel
# Deploy automático
```

---

## CÓDIGO CLAVE

### /app/api/chat/route.ts
```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

export async function POST(request: Request) {
  const { messages, model } = await request.json();
  
  const stream = await anthropic.messages.stream({
    model: model || 'claude-3-haiku-20240307',
    max_tokens: 4096,
    messages: messages,
  });

  const encoder = new TextEncoder();
  
  return new Response(
    new ReadableStream({
      async start(controller) {
        for await (const event of stream) {
          if (event.type === 'content_block_delta') {
            const data = JSON.stringify({ delta: { content: event.delta.text } });
            controller.enqueue(encoder.encode(`data: ${data}\n\n`));
          }
        }
        controller.enqueue(encoder.encode('data: [DONE]\n\n'));
        controller.close();
      }
    }),
    {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
      }
    }
  );
}
```

---

## CRITERIOS DE ÉXITO

1. ✅ Chat funcional con Claude real
2. ✅ Streaming de respuestas
3. ✅ UI moderna y responsiva
4. ✅ Deploy en Vercel funcionando
5. ✅ Health check respondiendo

---

## NOTAS

- NO usar SvelteKit (problemas de build)
- Un solo proyecto Next.js (frontend + API)
- Empezar simple, expandir después
- Priorizar que FUNCIONE sobre features

---

## EXPANSIÓN FUTURA (NO AHORA)

- [ ] Autenticación
- [ ] Historial de conversaciones
- [ ] Multi-modelo (OpenAI, Llama)
- [ ] Voice input
- [ ] File uploads
- [ ] Memory/RAG
