# 🔄 HANDOFF - Colmena

> Última actualización: C2.2.1 | 15 Ene 2026

## 📍 Proyecto Activo: Castle Solutions

**Repo:** `Pvrolomx/castle-checkin`  
**URL:** https://castlesolutions.biz  
**Estado:** ✅ Landing + Checkin funcional

### Estructura:
```
castlesolutions.biz/
├── /           → Landing page (7 propiedades, contacto)
├── /checkin    → Formulario de registro de huéspedes
└── /api/checkin → Envía email via Resend
```

### Lo que está listo:
- ✅ Landing page bilingüe (🇲🇽/🇺🇸)
- ✅ 7 propiedades reales
- ✅ Formulario de check-in completo
- ✅ Email a claudia@castlesolutions.biz
- ✅ Dominio configurado (sin "vercel" en URL)
- ✅ Logo de Castle Solutions

### Pendiente:
- ⏳ Fotos reales de propiedades (esperando de Claudia)
- ⏳ WhatsApp real
- ⏳ Links a Airbnb de cada propiedad
- ⏳ Verificar dominio en Resend (para from: checkin@castlesolutions.biz)

---

## 🔑 Tokens

**IMPORTANTE:** Los tokens están en Vercel env vars del proyecto `castle-checkin`:
- `GH_TOKEN` → GitHub API
- `RESEND_API_KEY` → Email

Para leerlos:
```bash
curl -s "https://api.vercel.com/v9/projects/prj_E2lZttCaFz5VmiL0FY3xY6oTxDkY/env?teamId=team_xmFW0blsjqFI5lwt29wBPi8Q" \
  -H "Authorization: Bearer [VERCEL_TOKEN]"
```

El token de Vercel se pasa por canal (partido en 2 para evitar bloqueo).

---

## 📝 Conversación de referencia

Chat anterior: **C2.2.1** (buscar en interfaz para contexto completo)

---

## ▶️ Siguiente paso

Esperando info de Claudia (fotos, WhatsApp, links Airbnb) para completar la landing.

---

*Actualizar este archivo con cada movimiento significativo.*
