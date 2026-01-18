# HANDOFF: Problema con OG Image

## Contexto
App: https://real-estate-solutions-kappa.vercel.app
Repo: github.com/Pvrolomx/real-estate-solutions

## Problema
La imagen de preview (Open Graph) se ve **oscura** cuando se comparte el link en celular/apps de mensajería. El usuario dice que la imagen aparece como un screenshot oscuro de la app, no la imagen OG configurada.

## Lo que se hizo
1. ✅ Se agregó `metadataBase` en layout.tsx para URLs absolutas
2. ✅ Se subió imagen OG de 1200x630 (dimensiones correctas)
3. ✅ Los meta tags están correctos:
   - `og:image` → `https://real-estate-solutions-kappa.vercel.app/og-image.jpg`
   - `twitter:image` → igual

## Verificación actual
```bash
curl -sL "https://real-estate-solutions-kappa.vercel.app" | grep "og:image"
# Resultado: content="https://real-estate-solutions-kappa.vercel.app/og-image.jpg"

curl -sI "https://real-estate-solutions-kappa.vercel.app/og-image.jpg"
# Resultado: 200 OK, image/jpeg, 1200x630
```

## El problema visual
El usuario compartió screenshot de Vercel Dashboard mostrando un preview oscuro (screenshot de la app con fondo de Puerto Vallarta), NO la imagen OG que subimos.

## Preguntas para dictamen
1. ¿Por qué las apps de mensajería no usan la imagen OG configurada?
2. ¿Es problema de caché? ¿Cómo forzar refresh?
3. ¿Falta algún meta tag adicional?
4. ¿El problema es que Vercel genera sus propios previews ignorando OG?

## Tokens
- Buscar en chats anteriores con: "token github vercel"

## Archivos relevantes
- /app/layout.tsx (tiene metadata con og:image)
- /public/og-image.jpg (1200x630, ~200KB)
