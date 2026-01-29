# 🌍 COUNTERPART — SPEC COMPLETO

## VISIÓN
**"Same age. Same question. Different life—daily."**

App de conexión social efímera que te empareja cada día con un extraño de tu misma edad, en cualquier parte del mundo. Ambos responden la misma pregunta íntima. Ves el contraste. La conexión desaparece al día siguiente.

---

## OBJETIVO MVP
Flujo diario completo: registro por año → notificación 8am → pregunta → respuesta → reveal de counterpart → card compartible.

---

## STACK TÉCNICO

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS
- **Deploy:** Vercel

### Backend (API)
- **Framework:** Next.js API Routes (mismo proyecto)
- **Database:** Supabase (PostgreSQL + Auth + Realtime)
- **Notificaciones:** Cron job Vercel + Web Push API
- **Deploy:** Vercel

### ¿Por qué este stack?
- Supabase = Auth + DB + Realtime gratis tier generoso
- Next.js = frontend + API en uno
- Vercel = deploy automático + cron jobs

---

## ESTRUCTURA DEL PROYECTO

```
counterpart/
├── app/
│   ├── layout.tsx              # Layout + metadata PWA
│   ├── page.tsx                # Landing / Login
│   ├── onboarding/page.tsx     # Selección año nacimiento
│   ├── daily/page.tsx          # Pregunta del día + respuesta
│   ├── reveal/page.tsx         # Reveal del counterpart
│   ├── history/page.tsx        # Historial de contrasts
│   ├── globals.css
│   └── api/
│       ├── health/route.ts
│       ├── auth/[...supabase]/route.ts
│       ├── question/route.ts   # GET pregunta del día
│       ├── answer/route.ts     # POST mi respuesta
│       ├── match/route.ts      # GET mi counterpart
│       └── cron/daily/route.ts # Cron: nueva pregunta + matching
├── components/
│   ├── QuestionCard.tsx
│   ├── AnswerInput.tsx
│   ├── ContrastCard.tsx        # La card compartible
│   ├── ShareButton.tsx
│   ├── CountdownTimer.tsx
│   └── BirthYearSelector.tsx
├── lib/
│   ├── supabase.ts
│   ├── questions.ts            # Pool de preguntas
│   └── matching.ts             # Lógica de emparejamiento
├── public/
│   ├── manifest.json
│   ├── sw.js
│   ├── icon-192.png
│   └── icon-512.png
├── package.json
├── tailwind.config.js
└── next.config.js
```

---

## DATABASE SCHEMA (Supabase)

### users
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE,
  birth_year INTEGER NOT NULL,
  city TEXT,
  country TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  last_active TIMESTAMP
);
```

### questions
```sql
CREATE TABLE questions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  text_es TEXT NOT NULL,
  text_en TEXT NOT NULL,
  category TEXT, -- 'life', 'career', 'relationships', 'fears', 'dreams'
  active_date DATE UNIQUE -- NULL = en pool, DATE = pregunta de ese día
);
```

### answers
```sql
CREATE TABLE answers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  question_id UUID REFERENCES questions(id),
  answer_text TEXT NOT NULL,
  answered_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, question_id)
);
```

### matches
```sql
CREATE TABLE matches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  question_id UUID REFERENCES questions(id),
  user_a UUID REFERENCES users(id),
  user_b UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  revealed_a BOOLEAN DEFAULT FALSE,
  revealed_b BOOLEAN DEFAULT FALSE
);
```

---

## API ENDPOINTS

### GET /api/health
```json
{ "status": "ok", "version": "1.0.0", "question_of_day": true }
```

### GET /api/question
**Response:**
```json
{
  "id": "uuid",
  "text": "¿Qué es lo que más miedo te da del futuro?",
  "category": "fears",
  "expires_in": 43200, // segundos hasta nueva pregunta
  "my_answer": null // o string si ya respondí
}
```

### POST /api/answer
**Request:**
```json
{
  "question_id": "uuid",
  "answer": "Quedarme solo..."
}
```
**Response:**
```json
{
  "success": true,
  "can_reveal": true // true si ya hay match disponible
}
```

### GET /api/match
**Response (si hay match y ambos respondieron):**
```json
{
  "my_answer": "Quedarme solo...",
  "counterpart": {
    "answer": "No poder pagar la renta del próximo mes",
    "city": "São Paulo",
    "country": "Brasil",
    "birth_year": 1995 // mismo que el mío
  },
  "question": "¿Qué es lo que más miedo te da del futuro?",
  "share_card_url": "/api/card/uuid.png"
}
```

### GET /api/cron/daily (Vercel Cron - 00:00 UTC)
1. Selecciona pregunta random del pool → marca como `active_date = TODAY`
2. Crea matches entre usuarios del mismo `birth_year`
3. Algoritmo: greedy random pairing por birth_year

---

## UI/UX

### Diseño
- **Tema:** Claro, minimalista, humano
- **Sensación:** Intimidad, no dating app
- **Tipografía:** Serif para preguntas (sensación de carta), sans para UI

### Colores
- Background: #FAFAF9 (stone-50)
- Cards: #FFFFFF
- Primary: #F97316 (orange-500) — calidez humana
- Text: #1C1917 (stone-900)
- Muted: #78716C (stone-500)

### Flujo de Screens

#### 1. Landing
```
[Logo Counterpart]

"Same age. Same question. 
Different life."

[Continuar con Google]
[Continuar con Email]

Ya tengo cuenta → Login
```

#### 2. Onboarding (solo primera vez)
```
¿En qué año naciste?

[Selector: 1960 ————•———— 2010]
            1995

Esto determina con quién te 
conectamos. No lo verá nadie.

[Continuar]
```

#### 3. Daily Question (estado: sin responder)
```
Enero 29, 2026

"¿Qué es lo que más 
miedo te da del futuro?"

[Textarea con placeholder: "Escribe honestamente..."]

[Enviar respuesta]

Tu counterpart está en algún lugar 
del mundo, respondiendo lo mismo.
```

#### 4. Daily Question (estado: esperando counterpart)
```
✓ Tu respuesta fue enviada

Esperando a tu counterpart...

[Animación sutil de reloj mundial]

Te notificaremos cuando puedas 
ver su respuesta.
```

#### 5. Reveal
```
Enero 29, 2026

"¿Qué es lo que más miedo te da del futuro?"

┌─────────────────────────────────┐
│  TÚ                    México   │
│  "Quedarme solo y no tener     │
│   a nadie que me cuide"        │
├─────────────────────────────────┤
│  TU COUNTERPART        Brasil   │
│  "No poder pagar la renta      │
│   del próximo mes"             │
└─────────────────────────────────┘

          Nacidos en 1995

[Compartir] [Nueva pregunta en 14:32:05]
```

#### 6. Share Card (generado para screenshot/stories)
```
┌─────────────────────────────────┐
│     COUNTERPART                 │
│     29 Enero 2026               │
│                                 │
│  "¿Qué es lo que más miedo     │
│   te da del futuro?"           │
│                                 │
│  ─────────────────────────────  │
│  🇲🇽 "Quedarme solo..."        │
│  ─────────────────────────────  │
│  🇧🇷 "No poder pagar..."       │
│  ─────────────────────────────  │
│                                 │
│        Nacidos en 1995          │
│     counterpart.app             │
└─────────────────────────────────┘
```

---

## PREGUNTAS INICIALES (Pool MVP)

```typescript
const QUESTIONS = [
  // VIDA
  "¿Qué es lo que más miedo te da del futuro?",
  "¿Cuál fue el momento más feliz de tu vida?",
  "¿Qué sacrificarías por tu familia?",
  "¿Qué te quita el sueño últimamente?",
  
  // CARRERA
  "¿Cómo te ves en 10 años?",
  "¿Qué trabajo harías gratis?",
  "¿Cuál es tu mayor logro profesional?",
  
  // RELACIONES
  "¿Qué es lo más difícil de mantener una relación?",
  "¿Qué aprendiste de tu peor ruptura?",
  "¿Qué no perdonarías en una pareja?",
  
  // EXISTENCIAL
  "Si murieras mañana, ¿qué te arrepentirías de no haber hecho?",
  "¿Qué le dirías a tu yo de 15 años?",
  "¿En qué momento supiste que eras adulto?",
  
  // IDENTIDAD
  "¿Qué parte de ti escondes del mundo?",
  "¿Qué te hace sentir más vivo?",
  "¿Cuándo fue la última vez que lloraste?"
];
```

---

## ALGORITMO DE MATCHING

```typescript
async function createDailyMatches(questionId: string) {
  // 1. Agrupar usuarios activos por birth_year
  const usersByYear = await groupUsersByBirthYear();
  
  // 2. Para cada grupo, hacer matching aleatorio
  for (const [year, users] of Object.entries(usersByYear)) {
    shuffle(users);
    
    // Emparejar de dos en dos
    for (let i = 0; i < users.length - 1; i += 2) {
      await createMatch(questionId, users[i], users[i + 1]);
    }
    
    // Si es impar, el último se empareja con alguien de ±1 año
    if (users.length % 2 === 1) {
      const lonely = users[users.length - 1];
      const neighbor = await findNeighborYearUser(year, lonely);
      if (neighbor) {
        await createMatch(questionId, lonely, neighbor);
      }
    }
  }
}
```

---

## CREDENCIALES REQUERIDAS

### Supabase
- URL: `NEXT_PUBLIC_SUPABASE_URL`
- Anon Key: `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Service Key: `SUPABASE_SERVICE_KEY` (para cron)

### Vercel
- Token: Buscar en chats anteriores
- Team ID: team_xmFW0blsjqFI5lwt29wBPi8Q

### GitHub
- Token: Buscar en chats anteriores
- Repo: Pvrolomx/counterpart

---

## TESTS (Playwright)

```typescript
// tests/counterpart.spec.ts

test('página carga correctamente', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('text=Counterpart')).toBeVisible();
});

test('flujo de onboarding', async ({ page }) => {
  await page.goto('/onboarding');
  await page.fill('[data-testid=birth-year]', '1995');
  await page.click('text=Continuar');
  await expect(page).toHaveURL('/daily');
});

test('enviar respuesta', async ({ page }) => {
  await page.goto('/daily');
  await page.fill('textarea', 'Mi respuesta de prueba');
  await page.click('text=Enviar');
  await expect(page.locator('text=respuesta fue enviada')).toBeVisible();
});

test('reveal muestra contraste', async ({ page }) => {
  await page.goto('/reveal');
  await expect(page.locator('[data-testid=my-answer]')).toBeVisible();
  await expect(page.locator('[data-testid=counterpart-answer]')).toBeVisible();
});

test('share card se genera', async ({ page }) => {
  await page.goto('/reveal');
  await page.click('text=Compartir');
  // Verificar que se abre el share dialog o se copia
});

test('PWA instalable', async ({ page }) => {
  await page.goto('/');
  const manifest = await page.evaluate(() => 
    fetch('/manifest.json').then(r => r.json())
  );
  expect(manifest.name).toBe('Counterpart');
});
```

---

## CRITERIOS DE ACEPTACIÓN

### MVP Funcional
- [ ] Auth con Google/Email (Supabase)
- [ ] Onboarding captura birth_year
- [ ] Pregunta diaria visible
- [ ] Usuario puede responder
- [ ] Match se crea automáticamente
- [ ] Reveal muestra ambas respuestas
- [ ] Share card funciona (Web Share API)
- [ ] Cron job corre a las 00:00 UTC

### UI/UX
- [ ] Mobile-first responsive
- [ ] Tema claro y cálido
- [ ] Animaciones sutiles
- [ ] Loading states

### PWA
- [ ] manifest.json correcto
- [ ] Service worker registrado
- [ ] App instalable
- [ ] Firma "Hecho con 🧡 por Colmena 2026"

### Deploy
- [ ] URL: counterpart.vercel.app (o dominio custom)
- [ ] Env vars configuradas en Vercel
- [ ] Health check respondiendo

---

## MECANISMOS VIRALES

### 1. FOMO Diario
- Nueva pregunta cada 24h
- Match desaparece al día siguiente
- Notificación push a las 8am local

### 2. Share Card Nativo
- Diseño optimizado para Instagram Stories
- Botón de compartir usa Web Share API
- Fallback: copiar imagen al clipboard

### 3. Network Effects
- Más usuarios = mejor matching
- Más países representados = contrastes más interesantes

---

## MONETIZACIÓN (FUTURO, NO MVP)

### Freemium
- **Free:** 1 counterpart/día
- **Premium ($4.99/mo):**
  - 3 counterparts/día
  - Elegir categoría de pregunta
  - Chat anónimo 24h con match
  - Sin ads

---

## NOTAS DE IMPLEMENTACIÓN

- Empezar SIN notificaciones push (agregar después)
- Empezar SIN historial (agregar después)
- Priorizar: auth → pregunta → respuesta → reveal → share
- El cron job puede ser manual al inicio (trigger desde Vercel dashboard)

---

## EXPANSIÓN FUTURA (NO AHORA)

- [ ] Notificaciones push
- [ ] Historial de contrasts
- [ ] Filtro por categoría
- [ ] Chat efímero con match
- [ ] Audio answers
- [ ] Modo grupal (3+ personas mismo año)

---

*"La app es la construcción de la app, no el producto."*

🐝 **Colmena 2026 — Counterpart SPEC v1**

---

## HISTORIAL

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 29 Ene 2026 | Claude (SPEC Session) | Versión inicial |
