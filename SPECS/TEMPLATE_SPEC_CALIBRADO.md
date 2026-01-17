# TEMPLATE SPEC - CALIBRADO PARA HAIKU/SONNET v1.0
# Fecha: 2026-01-17
# Autor: C1 (Sleepy) - Consigliere
# Uso: Copiar y adaptar para cada proyecto

---

## INSTRUCCIONES PARA EL CLAUDE EJECUTOR

IMPORTANTE: Este SPEC está diseñado para ejecución directa.
NO preguntes. NO pidas clarificación. EJECUTA.

Si algo no está claro:
1. Toma la decisión más lógica
2. Documenta la decisión en un comentario
3. Continúa

---

## PREREQUISITOS (HACER PRIMERO)

### Paso 1: Verificar Tokens
```bash
# Buscar tokens en conversaciones anteriores
conversation_search("github token vercel token")

# Si no encuentras, pide al usuario:
"Necesito tokens de GitHub y Vercel para continuar"
```

### Paso 2: Crear Repo
```bash
# Crear repo ANTES de escribir código
curl -X POST -H "Authorization: token TU_TOKEN" \
  https://api.github.com/user/repos \
  -d '{"name":"NOMBRE_PROYECTO","private":false}'
```

### Paso 3: Primer Commit
```bash
# Push inicial aunque sea vacío
echo "# NOMBRE_PROYECTO" > README.md
git add . && git commit -m "init" && git push
```

---

## 1. QUE CONSTRUIR

NOMBRE: [Nombre del proyecto]
URL FINAL: https://[nombre].vercel.app

DESCRIPCION EN UNA LINEA:
[Qué hace la app en máximo 15 palabras]

---

## 2. STACK (NO CAMBIAR)

```
Framework: Astro 5
UI: React + Tailwind CSS
Icons: Lucide React
Deploy: Vercel
```

COMANDOS DE INSTALACION:
```bash
npm create astro@latest NOMBRE -- --template minimal
cd NOMBRE
npx astro add react tailwind
npm install lucide-react
```

---

## 3. ARCHIVOS A CREAR

Lista EXACTA de archivos. Créalos EN ESTE ORDEN:


### Archivo 1: astro.config.mjs
```javascript
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [react(), tailwind()],
  output: 'static'
});
```

### Archivo 2: tailwind.config.mjs
```javascript
export default {
  content: ['./src/**/*.{astro,html,js,jsx,ts,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### Archivo 3: src/layouts/Layout.astro
```astro
---
const { title } = Astro.props;
---
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width" />
  <link rel="manifest" href="/manifest.json" />
  <title>{title}</title>
</head>
<body class="bg-slate-50 min-h-screen">
  <slot />
</body>
</html>
```

### Archivo 4: public/manifest.json
```json
{
  "name": "NOMBRE_APP",
  "short_name": "APP",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#f8fafc",
  "theme_color": "#2563eb",
  "icons": [
    {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}
  ]
}
```

### Archivo 5: src/pages/index.astro
```astro
---
import Layout from '../layouts/Layout.astro';
import MiComponente from '../components/MiComponente';
---
<Layout title="NOMBRE_APP">
  <main class="container mx-auto p-4">
    <MiComponente client:load />
  </main>
  <footer class="text-center p-4 text-sm text-slate-500">
    Hecho con ❤️ por Colmena 2026
  </footer>
</Layout>
```

---

## 4. COMPONENTES REACT

Para CADA componente, sigue este patrón:

```tsx
// src/components/NombreComponente.tsx
import { useState } from 'react';
import { IconName } from 'lucide-react';

interface Props {
  // definir props
}

export default function NombreComponente({ prop1, prop2 }: Props) {
  const [state, setState] = useState(initialValue);

  const handleAction = () => {
    // lógica
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      {/* contenido */}
    </div>
  );
}
```

---

## 5. API ROUTES (si aplica)

```typescript
// src/pages/api/endpoint.ts
import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();
  
  // lógica
  
  return new Response(JSON.stringify({ 
    success: true, 
    data: resultado 
  }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
};
```


---

## 6. COLORES Y ESTILOS

USA ESTOS COLORES (Tailwind):
- Fondo: bg-slate-50
- Cards: bg-white
- Primary: bg-blue-600, text-blue-600
- Secondary: bg-emerald-600
- Texto: text-slate-800
- Texto secundario: text-slate-500
- Bordes: border-slate-200
- Hover: hover:bg-blue-700

CLASES COMUNES:
- Card: "bg-white rounded-lg shadow p-4"
- Button primary: "bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
- Button secondary: "border border-slate-300 px-4 py-2 rounded-lg hover:bg-slate-100"
- Input: "border border-slate-300 rounded-lg px-3 py-2 w-full"

---

## 7. COMMITS (OBLIGATORIO)

HAZ COMMIT DESPUES DE CADA PASO:

```bash
# Después de crear estructura
git add . && git commit -m "feat: estructura inicial" && git push

# Después de cada componente
git add . && git commit -m "feat: add NombreComponente" && git push

# Después de cada página
git add . && git commit -m "feat: add pagina X" && git push

# Antes de deploy
git add . && git commit -m "feat: ready for deploy" && git push
```

---

## 8. DEPLOY A VERCEL

OPCION A - Con MCP Vercel:
```
Usa: Vercel:deploy_to_vercel
```

OPCION B - Manual:
```bash
npm install -g vercel
vercel --prod
```

OPCION C - Via GitHub:
1. Push a GitHub
2. Usuario importa en vercel.com/new
3. Selecciona repo
4. Deploy

---

## 9. CHECKLIST FINAL

Antes de reportar como COMPLETO, verificar:

- [ ] App carga sin errores
- [ ] Todas las rutas funcionan
- [ ] Mobile responsive (probar en viewport 375px)
- [ ] Footer dice "Hecho con ❤️ por Colmena 2026"
- [ ] manifest.json presente
- [ ] Commits pusheados a GitHub
- [ ] URL de Vercel funciona

---

## 10. SI ALGO FALLA

### Error: npm install falla
```bash
rm -rf node_modules package-lock.json
npm install
```

### Error: Build falla
```bash
# Ver error específico
npm run build 2>&1 | head -50
# Usualmente es import faltante o typo
```

### Error: Vercel 404
- Verificar que Framework Preset = "Astro"
- Verificar que output = 'static' en astro.config

### Error: Componente no renderiza
- Verificar client:load en el .astro
- Verificar export default en el componente

---

## 11. REPORTAR RESULTADO

Al terminar, responde con:

```
✅ COMPLETADO

📦 Repo: github.com/usuario/nombre
🌐 URL: https://nombre.vercel.app
⏱️ Tiempo: X minutos

📝 Notas: [cualquier decisión tomada]
```

---

FIN DEL TEMPLATE
Versión: 1.0 Calibrado para Haiku/Sonnet
Autor: C1 (Sleepy)
Fecha: 2026-01-17
