# SPEC: ANFITRION-MX-PAYMENTS-001
# Implementación de Pagos con Stripe Payment Links

## Contexto
El backend actual (/crear-sesion-reporte) no está desplegado en Vercel.
Cuando usuarios agotan 10 créditos gratis y dan click en "Comprar más",
reciben error 404.

## Solución: Stripe Payment Links
Usar Payment Links de Stripe en lugar de backend personalizado.
Es más simple, no requiere servidor, y Stripe maneja todo.

## Configuración en Stripe Dashboard

### 1. Crear Payment Link

En Stripe Dashboard → Payment Links → Create:

- **Producto:** "10 Cálculos - Anfitrión MX"
- **Precio:** $10 MXN (pago único)
- **Cantidad:** Fija (1)
- **After payment:** Redirect to URL

### 2. URL de Éxito

```
https://airbnb-calculadora.vercel.app/?payment=success&credits=10
```

(O el nuevo dominio cuando esté configurado)

### 3. Obtener Link

Stripe generará algo como:
```
https://buy.stripe.com/test_XXXXXX
```

## Implementación en Frontend

### 1. Modificar Botón de Compra

```javascript
// ANTES (no funciona)
async function comprarCreditos() {
  const response = await fetch('/crear-sesion-reporte', {
    method: 'POST'
  });
  // redirect a Stripe Checkout
}

// DESPUÉS (funciona)
function comprarCreditos() {
  // Abrir Payment Link directamente
  window.open('https://buy.stripe.com/XXXXXX', '_blank');
}
```

### 2. Detectar Pago Exitoso

```javascript
// Al cargar la página
document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  
  if (params.get('payment') === 'success') {
    const creditsToAdd = parseInt(params.get('credits')) || 10;
    
    // Agregar créditos
    let currentCredits = parseInt(localStorage.getItem('calculosRestantes')) || 0;
    localStorage.setItem('calculosRestantes', currentCredits + creditsToAdd);
    
    // Mostrar mensaje de éxito
    mostrarNotificacion('¡Pago exitoso! Se agregaron ' + creditsToAdd + ' cálculos.');
    
    // Limpiar URL
    window.history.replaceState({}, document.title, window.location.pathname);
    
    // Actualizar UI de créditos
    actualizarContadorCreditos();
  }
});
```

### 3. UI del Botón

```html
<div id="comprar-creditos" class="hidden">
  <p>Te quedaste sin cálculos gratuitos</p>
  <button onclick="comprarCreditos()" class="btn-primary">
    Comprar 10 cálculos por $10 MXN
  </button>
</div>
```

### 4. CSS para Notificación

```css
.notificacion-exito {
  position: fixed;
  top: 20px;
  right: 20px;
  background: #10b981;
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  animation: slideIn 0.3s ease;
  z-index: 1000;
}

@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
```

## Flujo Completo

```
1. Usuario agota 10 créditos gratis
2. Aparece botón "Comprar 10 cálculos por $10 MXN"
3. Click → Abre Stripe Payment Link (nueva pestaña)
4. Usuario paga con tarjeta
5. Stripe redirige a: ?payment=success&credits=10
6. Frontend detecta params y agrega créditos
7. Muestra notificación de éxito
8. Usuario puede seguir calculando
```

## Archivos a Modificar

1. **public/index.html** (o JS principal)
   - Cambiar función comprarCreditos()
   - Agregar detección de payment=success
   - Agregar función mostrarNotificacion()

2. **public/credits.js** (si existe separado)
   - Mismos cambios

3. **public/styles.css**
   - Agregar estilos de notificación

## Configuración de Stripe

### Modo Test (actual)
- Key: sk_test_51SceBgPGdoJRaXCX...
- Usar Payment Links de test

### Modo Live (cuando esté listo)
- Cambiar a sk_live_...
- Crear Payment Link en modo live
- Actualizar URL en frontend

## Eliminar Código Obsoleto

Estos archivos/endpoints ya no son necesarios:
- /crear-sesion-reporte (backend)
- Cualquier código de Stripe Checkout server-side

## Checklist

- [ ] Crear producto en Stripe Dashboard
- [ ] Crear Payment Link con redirect URL
- [ ] Actualizar botón de compra en frontend
- [ ] Agregar detección de ?payment=success
- [ ] Agregar notificación de éxito
- [ ] Probar flujo completo en modo test
- [ ] Cambiar a modo live cuando esté listo

## Ventajas de Payment Links

✅ No requiere backend
✅ Stripe maneja toda la seguridad
✅ Funciona con Vercel static hosting
✅ Fácil de actualizar precios
✅ Soporte para múltiples métodos de pago
✅ Cumple con PCI DSS automáticamente

---
Spec creado: 2026-01-18
Autor: C1 (Sleepy)
Prioridad: Alta
Dependencia: Crear Payment Link en Stripe Dashboard primero
