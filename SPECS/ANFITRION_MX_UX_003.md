# SPEC: ANFITRION-MX-UX-003
# Corrección de Idioma - Español Completo

## Objetivo
Corregir textos en inglés para mantener consistencia en español.

## Problema Detectado
- "Number of nights" aparece en inglés
- Inconsistencia en idioma reduce profesionalismo

## Solución
Buscar y reemplazar todos los textos en inglés.

## Implementación

### Textos a Corregir

| Actual (inglés) | Correcto (español) |
|-----------------|-------------------|
| Number of nights | Número de noches |
| Calculate | Calcular |
| Download PDF | Descargar PDF |
| Reset | Limpiar |
| Select | Seleccionar |
| Enter amount | Ingresa monto |
| Total | Total |

### Búsqueda y Reemplazo

```bash
# En el archivo HTML principal
sed -i 's/Number of nights/Número de noches/g' index.html
sed -i 's/Calculate/Calcular/g' index.html
sed -i 's/Download PDF/Descargar PDF/g' index.html
sed -i 's/Reset/Limpiar/g' index.html
```

### Placeholders

```html
<!-- ANTES -->
<input placeholder="Enter amount">

<!-- DESPUÉS -->
<input placeholder="Ingresa monto">
```

### Labels

```html
<!-- ANTES -->
<label>Number of nights</label>

<!-- DESPUÉS -->
<label>Número de noches</label>
```

## Checklist

- [ ] Buscar todos los textos en inglés
- [ ] Corregir "Number of nights"
- [ ] Verificar placeholders
- [ ] Verificar botones
- [ ] Verificar mensajes de error
- [ ] Probar todo el flujo en español

---
Spec creado: 2026-01-19
Autor: C1 (Sleepy)
Prioridad: Alta
Tiempo estimado: 5 minutos
Dependencias: Ninguna
