# 🔄 HANDOFF - Colmena

> Última actualización: **C0** | 15 Ene 2026

## 📍 Proyecto Activo: Castle Solutions

**Repo:** `Pvrolomx/castle-checkin`  
**URL:** https://castlesolutions.biz  
**Estado:** ✅ Landing + Checkin + PWA funcional

### Estructura:
```
castlesolutions.biz/
├── /           → Landing page (7 propiedades, contacto)
├── /checkin    → Formulario de registro de huéspedes
└── /api/checkin → Envía email via Resend
```

### ✅ Completado:
- Landing page bilingüe (🇲🇽/🇺🇸)
- 7 propiedades reales
- Formulario de check-in completo
- Email a claudia@castlesolutions.biz
- Dominio configurado (castlesolutions.biz)
- Logo de Castle Solutions
- **PWA instalable** (botón "Instalar App")
- **Firma C0** en footer

### ⏳ Pendiente:
- Fotos reales de propiedades (esperando de Claudia)
- WhatsApp real (actualmente placeholder)
- Links a Airbnb de cada propiedad
- Verificar dominio en Resend (para from: checkin@castlesolutions.biz)

---

## 🔑 Cómo conseguir los tokens

**Paso 1:** Arquitecto pasa token de Vercel por canal (partido en 2)

**Paso 2:** Leer este HANDOFF para contexto

**Paso 3:** Usar Vercel token para leer los otros tokens:
```bash
curl -s "https://api.vercel.com/v9/projects/prj_E2lZttCaFz5VmiL0FY3xY6oTxDkY/env?teamId=team_xmFW0blsjqFI5lwt29wBPi8Q" \
  -H "Authorization: Bearer [VERCEL_TOKEN]"
```

**Tokens disponibles en Vercel env vars:**
- `GH_TOKEN` → GitHub API
- `RESEND_API_KEY` → Email API

---

## 📝 Linaje

| ID | Proyecto | Fecha |
|----|----------|-------|
| C0 | Castle Solutions (landing + checkin + PWA) | 15 Ene 2026 |

---

## ▶️ Siguiente paso

Esperando info de Claudia (fotos, WhatsApp, links Airbnb) para completar la landing.

---

*Actualizar este archivo con cada movimiento significativo.*

— **C0** 🏰
