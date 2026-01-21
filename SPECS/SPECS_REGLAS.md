# REGLAS PARA SPECs

## Estructura Obligatoria

Todo SPEC debe incluir:

### 1. OBJETIVO
- Qué hace la app en 1-2 líneas

### 2. STACK
- Framework (React/Astro/HTML)
- Estilos (Tailwind)
- Deploy (Vercel)

### 3. FUNCIONALIDAD
- Lista de features requeridos
- Casos edge a manejar

### 4. UI/UX
- Colores/tema
- Responsive requerido
- Idiomas

### 5. TESTS (Playwright)
- [ ] Carga inicial < 3s
- [ ] Inputs válidos = resultado esperado
- [ ] Inputs inválidos = error controlado
- [ ] Flujo pago (si aplica)
- [ ] Mobile y desktop

### 6. CRITERIOS DE ACEPTACIÓN
- Qué define "terminado"
- URL de deploy esperada

---

## Notas
- El Claude ejecutor debe generar tests junto con el código
- Tests se corren con Playwright antes de marcar como completado
- Si falla un test, no se considera terminado

v1 - 2026-01-21
