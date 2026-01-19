# 🏥 HANDOFF: Healthcare Resources PV App

> **Proyecto:** Mi Salud PV  
> **Cliente:** Healthcare Resources Puerto Vallarta  
> **Contacto:** Amiga íntima del Arquitecto (dueña de HCRPV)  
> **Fecha:** 19 Enero 2026  
> **Autor:** C-OG

---

## 📋 CONTEXTO

### ¿Qué es Healthcare Resources PV?
- Red independiente de servicios médicos en Puerto Vallarta
- Conecta pacientes (mayormente expats/turistas) con médicos que hablan inglés
- Servicios: referrals, ayuda con seguros, check-ups, turismo médico
- Operando desde 2006
- Web actual: https://healthcareresourcespv.com/ (WordPress 2017)

### Perfil del usuario final
- **Edad:** 50-80 años (predominante)
- **Origen:** USA, Canadá, expats
- **Limitaciones:** 
  - Deterioro cognitivo (micro strokes, demencia temprana, Alzheimer)
  - No entienden tecnología compleja
  - Se pierden en menús
  - Olvidan contraseñas

### REGLA DE ORO
```
La app debe ser ≤ WhatsApp en complejidad
Si tu mamá no puede usarla, está mal
```

---

## 🎯 DOLORES IDENTIFICADOS

1. **Ella es el cuello de botella** - Todo pasa por WhatsApp/teléfono manual
2. **Clientes no entienden tecnología** - Necesitan UX ultra-simple
3. **Coordinación manual** - Citas, seguimiento, claims = todo a mano
4. **Sin directorio interactivo** - Pacientes no pueden buscar médicos solos
5. **FAQ repetitivo** - ¿Habla inglés? ¿Acepta mi seguro? (una y otra vez)

---

## 💡 SOLUCIÓN PROPUESTA: "Mi Salud PV"

### Pantalla del paciente (3 botones máximo)
```
┌─────────────────────────┐
│                         │
│   🆘 EMERGENCIA         │  ← Tap = llamada directa
│                         │
├─────────────────────────┤
│                         │
│   👨‍⚕️ BUSCAR DOCTOR      │  ← Directorio simple
│                         │
├─────────────────────────┤
│                         │
│   📅 MIS CITAS          │  ← Próximas citas
│                         │
├─────────────────────────┤
│                         │
│   💬 NECESITO AYUDA     │  ← WhatsApp directo a HCRPV
│                         │
└─────────────────────────┘

Sin login. Sin menús. Sin configuración.
3 taps máximo para cualquier acción.
```

### Admin para ella (dashboard oculto)
- Gestión de directorio médico
- Ver/editar citas
- Push notifications a pacientes
- Métricas básicas

---

## 🚀 ROADMAP DE ESCALADO

| Fase | Feature | Complejidad |
|------|---------|-------------|
| MVP | Directorio + botón WhatsApp | Baja (2-3 hrs) |
| V2 | Sistema de citas | Media (4-6 hrs) |
| V3 | Recordatorios de medicinas | Media (4 hrs) |
| V4 | Ayuda con claims de seguro | Alta (8+ hrs) |

**Empezar con MVP y validar antes de escalar.**

---

## 🔧 STACK TÉCNICO

```
- Framework: Next.js 14
- Hosting: Vercel (free tier)
- DB: localStorage (MVP) → Supabase (V2+)
- Auth: Ninguno en MVP (pacientes) / Simple pin (admin)
- PWA: Sí (instalable)
- Estilo: Inline o Tailwind mínimo
```

---

## 📞 ESTRATEGIA DE APPROACH

### Fase 1: Discovery (NO técnico)
```
Pregunta clave: "¿Cuál es el proceso más tedioso 
que haces a diario? El que te da hueva."
```
- Solo escuchar
- No mencionar que vas a construir algo
- Identificar dolor REPETITIVO

### Fase 2: Demo sorpresa
- Construir sin decirle
- Mandar: "Te hice algo, chécalo"
- Efecto WOW - costo $0 para ella

### Fase 3: El ask natural
```
"Si te sirve, solo te pido que cuando alguien 
de tu red necesite algo similar, me lo mandes."
```
- No pedir dinero
- No pedir compromiso
- Solo referidos naturales

---

## 🌐 RECURSOS

### URLs
- Web actual: https://healthcareresourcespv.com/
- Página de médicos: https://healthcareresourcespv.com/medical-tourism-puerto-vallarta-physicians/
- Contacto: https://healthcareresourcespv.com/contact-us-healthcare-resources-pv/
- PlusCard: https://healthcareresourcespv.com/pluscard/

### Credenciales
Ver archivo de credenciales Colmena (no incluidas aquí por seguridad)

---

## ✅ CHECKLIST PRE-BUILD

- [ ] Discovery con la dueña completado
- [ ] Dolor #1 confirmado
- [ ] Repo creado: `Pvrolomx/mi-salud-pv`
- [ ] Proyecto Vercel creado
- [ ] MVP construido
- [ ] Smoke test pasado
- [ ] Demo enviada a ella

---

## 📝 NOTAS

- La dueña puede canalizar a TODA su red de contactos
- Este proyecto es puerta de entrada a más apps de salud/turismo
- Priorizar UX sobre features
- Si el usuario tiene que pensar, está mal diseñado

---

*"Es como WhatsApp pero solo para sus citas y medicinas. Tres botones. Tu mamá lo podría usar."*

🐝 **C-OG - Colmena 2026**
