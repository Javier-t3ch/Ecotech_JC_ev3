# Integración y uso ético de inteligencia artificial en EcoTech

## 1. ¿Cómo se utilizó la IA?

Durante el desarrollo de EcoTech se utilizó ChatGPT para resolver dudas, comprender conceptos y recibir **recomendaciones sobre la organización y seguridad del sistema**. También se empleó como apoyo en revisiones del código y pruebas, pero sus respuestas no se consideraron automáticamente correctas.

Las recomendaciones se compararon con los requisitos del proyecto y la materia de clases. Antes de aceptar una modificación, se revisó su funcionamiento y su efecto sobre las demás partes del programa.

## 2. Ejemplos de consultas y recomendaciones

Los siguientes prompts están **redactados a modo de ejemplo a partir de las consultas realizadas**. No se presentan como transcripciones literales.

### Ejemplo 1. Organización del menú de usuario

**Prompt de ejemplo:**

> ¿Cómo me recomiendas organizar el menú de usuario de EcoTech para que las opciones dependan del rol de administrador y del cargo de Recursos Humanos?

**Recomendación recibida:** mantener un menú con funciones comunes y mostrar las opciones adicionales según los permisos. También se recomendó numerar dinámicamente las opciones visibles para evitar saltos y dejar «Cerrar sesión» al final.

**Análisis y decisión:** se consideró una organización más clara para cada usuario. Además, se mantuvieron verificaciones de permisos en los servicios, ya que ocultar una opción del menú no impide por sí solo el acceso no autorizado.

### Ejemplo 2. Validación de datos

**Prompt de ejemplo:**

> ¿Qué validaciones me recomiendas para los nombres, correos, proyectos y números ingresados en EcoTech, sin bloquear caracteres que sí sean necesarios?

**Recomendación recibida:** definir límites según el campo, permitir tildes en nombres, restringir símbolos innecesarios en proyectos y departamentos y conservar los caracteres válidos en correos y contraseñas.

**Análisis y decisión:** se eligieron reglas distintas para cada dato y se centralizaron las validaciones para evitar criterios contradictorios entre menús y clases.

### Ejemplo 3. Seguridad al consultar las APIs

**Prompt de ejemplo:**

> ¿Qué me recomiendas tener en cuenta para consultar las APIs de dólar y clima de forma segura y evitar que EcoTech se cierre si falla internet?

**Recomendación recibida:** comprobar las respuestas HTTP y los datos JSON, utilizar tiempos de espera y manejar excepciones. Para las consultas con historial, se recomendó distinguir un dato almacenado de una respuesta actual de la API.

**Análisis y decisión:** se incorporaron controles de errores y se identificaron los datos de respaldo para no confundir información antigua con información actual.

## 3. Uso ético y responsable

- **Transparencia:** se reconoce el apoyo de ChatGPT y se distingue entre recomendaciones, decisiones del proyecto y pruebas realizadas.
- **Revisión humana:** no se acepta una respuesta únicamente porque provenga de la IA; se analiza y se comprueba antes de utilizarla.
- **Privacidad:** no se deben compartir contraseñas, claves de API ni información privada del proyecto en los prompts o archivos de revisión.
- **Aprendizaje:** la IA se utiliza para entender alternativas y justificar decisiones, no para reemplazar el conocimiento necesario para explicar el programa.

## 4. Conclusión

ChatGPT fue una herramienta de orientación y apoyo durante el desarrollo de EcoTech. Sus recomendaciones ayudaron a tomar decisiones sobre el menú de usuario, las validaciones y el manejo de errores de las APIs. **La responsabilidad de revisar, comprender y justificar las decisiones técnicas sigue siendo de quien desarrolla el proyecto.**
