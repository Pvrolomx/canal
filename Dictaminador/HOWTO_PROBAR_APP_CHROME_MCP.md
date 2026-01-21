# HOW TO: Probar una App con Chrome MCP

Guia paso a paso para abrir y probar funcionalidades de una app web usando Claude + Chrome MCP.

## REQUISITOS PREVIOS
- Chrome con extension MCP instalada
- - Claude con acceso a Chrome MCP tools
  - - URL de la app a probar (Vercel, localhost, etc.)
   
    - ## PASO 1: Obtener contexto de tabs
    - tabs_context_mcp con createIfEmpty: true
    - Esto te da los tabs disponibles o crea uno nuevo.
   
    - ## PASO 2: Crear tab nueva (opcional)
    - tabs_create_mcp
    - Devuelve el tabId que usaras en los siguientes pasos.
   
    - ## PASO 3: Navegar a la app
    - navigate con tabId y url de tu app
   
    - ## PASO 4: Esperar carga
    - computer action:wait duration:3
   
    - ## PASO 5: Screenshot inicial
    - computer action:screenshot
    - Esto te muestra la UI actual.
   
    - ## PASO 6: Encontrar elementos
    - find query:"boton de login" o "campo email"
    - Devuelve ref_ids que usas para interactuar.
   
    - ## PASO 7: Llenar formularios
    - form_input ref:ref_22 value:"tu valor"
   
    - ## PASO 8: Hacer clicks
    - computer action:left_click ref:ref_71
   
    - ## PASO 9: Scroll
    - computer action:scroll coordinate:[420,400] scroll_amount:5 scroll_direction:down
   
    - ## PASO 10: Leer contenido de pagina
    - read_page para ver el DOM/accessibility tree.
   
    - ## EJEMPLO COMPLETO: Probar Calculadora
    - 1. tabs_context_mcp - obtener/crear tab
      2. 2. navigate - https://anfitrion-mx.vercel.app
         3. 3. wait 3 segundos
            4. 4. screenshot - ver UI
               5. 5. find Tarifa por noche - ref_22
                  6. 6. form_input ref_22 value:1500
                     7. 7. find Numero de noches - ref_24
                        8. 8. form_input ref_24 value:5
                           9. 9. scroll down
                              10. 10. find Ver cuanto me queda - ref_71
                                  11. 11. left_click ref_71
                                      12. 12. screenshot - ver resultado
                                         
                                          13. ## TIPS
                                          14. - Siempre haz screenshot despues de acciones importantes
                                              - - Usa find con lenguaje natural
                                                - - Si no encuentras algo, haz scroll primero
                                                  - - Los ref_ids cambian entre paginas/recargas
                                                   
                                                    - ---
                                                    Creado por C_OG2 - Dictaminador | Colmena 2026
