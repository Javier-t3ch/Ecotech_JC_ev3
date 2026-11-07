# EcoTech Solutions — Sistema de Gestión Empresarial

**Asignatura:** TI3021 — Programación Orientada a Objeto Seguro  
**Unidades:** Unidad 2 (POO y persistencia) y Unidad 3 (APIs externas y seguridad)  
**Tipo de proyecto:** aplicación de consola en Python, desarrollada con fines académicos.

## 1. Descripción

EcoTech Solutions es un sistema de gestión empresarial que permite administrar empleados, departamentos, proyectos, cuentas de usuario y registros de horas trabajadas. Combina programación orientada a objetos (POO), un modelo relacional, operaciones CRUD, autenticación, permisos por rol y consumo de servicios externos.

La versión actual incorpora dos APIs: una para consultar el dólar observado y otra para obtener condiciones meteorológicas. También permite **estimar montos de CLP a USD** y consultar un **pronóstico de tres días** como apoyo a la planificación de actividades.

> **Alcance:** el sistema es una implementación académica. La estimación en USD no ejecuta pagos ni modifica salarios, y las orientaciones climáticas no sustituyen las alertas oficiales.

## 2. Funcionalidades

### Gestión de información interna

- **Empleados:** registrar, buscar, actualizar, listar y administrar su información y cargo, según permisos.
- **Departamentos:** crear, consultar, modificar y eliminar departamentos; asignar empleados, gerentes y relacionar proyectos.
- **Proyectos:** administrar proyectos, sus fechas y descripciones, asignaciones de empleados y relaciones con departamentos.
- **Registros de tiempo:** registrar y consultar las horas trabajadas y su descripción, asociadas a empleados y proyectos.
- **Usuarios:** autenticar cuentas, registrar usuarios para empleados existentes sin cuenta y cambiar contraseñas.
- **Gestión de Permisos:** un administrador puede consultar las cuentas y otorgar el rol `admin` a otra cuenta. El cambio queda persistido en la base de datos.
- **Gestión de Departamentos:** utiliza datos reales de la base mediante `DepartamentoDAO`, en lugar de una demostración en memoria.

Los módulos administrativos están agrupados bajo **Módulos EcoTech**, accesible desde el menú privado del administrador.

### Menú privado de cada cuenta

Tras iniciar sesión se puede:

1. Consultar la propia ficha laboral.
2. Cambiar únicamente el nombre y el correo propios.
3. Consultar los propios registros de tiempo.
4. Consultar los proyectos asignados.
5. Consultar los departamentos asociados.
6. Registrar horas propias **solo en proyectos asignados**.
7. Acceder al submenú **Servicios externos (APIs)**.

Según los permisos, aparecen opciones adicionales para registrar cuentas, administrar módulos, contratar empleados o asignarlos a departamentos.

### Recursos Humanos

El **cargo** y el **rol de acceso** son conceptos distintos:

| Concepto | Valores | Función |
|---|---|---|
| Rol de la cuenta (`usuario.rol`) | `admin`, `empleado` | Define el acceso administrativo. |
| Cargo del empleado (`empleado.id_cargo`) | `1` Empleado, `2` Recursos Humanos | Define funciones laborales específicas. |

Una cuenta vinculada a un empleado con **cargo Recursos Humanos (ID 2)** puede, aunque tenga rol `empleado`:

- Contratar un empleado nuevo y asignarlo a un departamento.
- Asignar un empleado existente a un departamento.

La contratación y la asignación inicial se realizan en una transacción para evitar registros incompletos si falla una de las operaciones. Tener el cargo de Recursos Humanos **no otorga automáticamente** el rol `admin`.

### Servicios externos (APIs)

El menú **Servicios externos** está disponible para usuarios autenticados e incorpora:

| Opción | Funcionalidad | Fuente / almacenamiento |
|---|---|---|
| 1 | Consultar dólar observado | `mindicador.cl`; se guarda en `indicador_api`. |
| 2 | Historial del dólar | Lectura de la base local. |
| 3 | Consultar clima actual | Open-Meteo; se guarda en `clima_api`. |
| 4 | Historial del clima | Lectura de la base local por ciudad. |
| 5 | Estimar monto internacional de CLP a USD | Usa el dólar observado consultado o un dato local identificado como respaldo. |
| 6 | Planificación climática | Pronóstico de tres días desde Open-Meteo. |
| 0 | Volver al menú privado | Regresa sin una pausa adicional. |

**Ciudades disponibles para clima:** La Serena, Santiago, Valparaíso, Concepción y Temuco. Se seleccionan desde el menú.

**Dólar y clima actual:** las respuestas JSON se validan y deserializan a objetos de dominio antes de almacenarlas mediante DAO. Si falla una consulta, el sistema intenta recuperar la última observación local disponible e indica que se trata de un respaldo que podría estar desactualizado.

**Estimación internacional:** divide el monto CLP ingresado por la cotización CLP/USD y muestra el resultado aproximado en USD. No realiza transferencias, no registra pagos, no aplica comisiones ni impuestos y no cambia el salario de ningún empleado.

**Planificación climática:** muestra temperaturas mínimas y máximas, probabilidad y cantidad de lluvia, viento máximo y estado del tiempo de los próximos tres días. Las orientaciones para actividades al aire libre son didácticas. El pronóstico se consulta en línea; el historial de clima actual **no** se utiliza como pronóstico de respaldo.

## 3. Autenticación y seguridad

- Las contraseñas se almacenan como **hashes con `bcrypt`**, no como texto plano.
- En una terminal compatible, se muestra un `*` por cada carácter de contraseña; en otras consolas se oculta la entrada sin mostrar asteriscos.
- Las contraseñas se validan por longitud y admiten hasta **72 bytes UTF-8**, de acuerdo con la implementación actual.
- Las cuentas se vinculan a un empleado mediante `usuario.empleado_id`, que es único: **cada empleado puede tener como máximo una cuenta**.
- Las funciones protegidas verifican la sesión y los permisos en los servicios o métodos correspondientes; no dependen únicamente de ocultar opciones del menú.
- Una promoción a `admin` se guarda en la base de datos. La persona debe iniciar sesión nuevamente para utilizar el rol actualizado.
- Las consultas HTTP emplean `requests`, tiempo de espera y validación de la respuesta.
- Los errores se controlan para evitar que fallos comunes de entrada o conexión terminen abruptamente la aplicación.

> No publiques el archivo `.env`, bases de datos con información laboral, credenciales ni copias de contraseñas. `.gitignore` excluye estos archivos del control de versiones, pero debes revisarlos antes de comprimir una entrega.

## 4. Validaciones de datos y uso de formularios

Todas las reglas de validación y lectura están centralizadas en **`src/validaciones.py`**. Ya no se utilizan `src/menus/validaciones.py` ni `src/dominio/validaciones_datos.py`.

| Campo | Regla principal |
|---|---|
| Nombre de persona | Máximo 50 caracteres; letras, tildes, ñ, espacios, guiones, puntos y apóstrofes. Sin números ni símbolos extraños. |
| Nombre de departamento o proyecto | Máximo 50 caracteres; letras, números y espacios; debe incluir al menos una letra. |
| Descripción de proyecto o tarea | Máximo 100 caracteres; admite puntuación habitual. |
| Dirección | Máximo 150 caracteres; admite símbolos habituales de direcciones. |
| Correo electrónico | Máximo 100 caracteres, con validación de formato. |
| Teléfono | Entre 8 y 15 dígitos; máximo 20 caracteres incluidos separadores admitidos. |
| Nombre de usuario | Entre 3 y 40 caracteres; letras sin tildes, números y `_`. |
| Contraseña | Mínimo del modelo: 6 caracteres; máximo 72 bytes UTF-8. Algunos lectores de formulario pueden exigir 8. |
| Identificadores (IDs) | Enteros positivos, solo dígitos, hasta 2.147.483.647. |
| Horas trabajadas | Entre 1 y 24 horas por registro. |
| Salario | Hasta 9.999.999.999,99, con máximo dos decimales. |
| Fecha | Formato `AAAA-MM-DD` y fecha real válida. |

Los campos no válidos vuelven a solicitarse **sin reiniciar el formulario completo** cuando el error puede corregirse en ese campo.

Comandos disponibles en los formularios:

- **`LISTAR`**: muestra los IDs disponibles cuando el campo lo permite; luego solicita de nuevo el mismo ID. Puede filtrar opciones según la operación.
- **`CANCELAR`**: abandona el formulario sin guardar la operación incompleta (también se admiten `SALIR` y `:q` en las lecturas compatibles).
- **Enter**: en campos opcionales de edición, conserva el dato anterior cuando el formulario lo indica.

Los menús limpian la pantalla en sus transiciones. Después de mostrar resultados normalmente se pide **Enter para continuar**, mientras que regresar con `0` desde Módulos EcoTech o Servicios externos no agrega esa pausa.

## 5. Tecnologías y dependencias

- Python 3.
- `sqlite3` (incluido en Python) para SQLite.
- `PyMySQL` para MySQL.
- `python-dotenv` para cargar el archivo `.env`.
- `bcrypt` para el hash y verificación de contraseñas.
- `requests` para peticiones HTTP a las APIs.
- Git/GitHub y diagramas UML para el desarrollo y documentación.

Las dependencias externas están indicadas en `requirements.txt`.

## 6. Instalación

Desde la carpeta principal del proyecto, donde se encuentran `requirements.txt` y `src/`, abre la terminal integrada de VS Code o PowerShell.

**Crear y activar el entorno virtual (Windows/PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Instalar dependencias:**

```powershell
python -m pip install -r requirements.txt
```

Usar `python -m pip` evita depender de que `pip` esté disponible como comando independiente.

### Configurar `.env`

Crea `.env` en la raíz a partir de `.env.example` y **deja un solo bloque de configuración** para el motor que usarás. El ejemplo del repositorio contiene opciones para ambos motores; no mantengas dos valores `DB_ENGINE` activos a la vez.

**SQLite (recomendado para comenzar):**

```ini
DB_ENGINE=sqlite
DB_NAME=ecotech.db
```

**MySQL:**

```ini
DB_ENGINE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecotech
DB_USER=tu_usuario
DB_PASSWORD=tu_contrasena
```

Para MySQL, crea previamente la base `ecotech` y configura credenciales válidas. El puerto puede ser distinto si tu instalación local utiliza otra configuración. **No copies contraseñas reales a archivos que publicarás.**

## 7. Ejecutar EcoTech

```powershell
python src/main.py
```

Al iniciar, el programa:

1. Crea las tablas necesarias (y realiza las migraciones contempladas por el proyecto).
2. Ejecuta la semilla académica de empleados, departamentos, proyectos y relaciones.
3. Prepara la cuenta inicial `admin` si no existe; en el primer inicio solicita crear y confirmar su contraseña.
4. Muestra el formulario de inicio de sesión.

La semilla incluye **20 empleados, 5 departamentos, 5 proyectos y 10 registros de tiempo**, además de relaciones. Está diseñada para evitar duplicar sus registros de ejemplo en ejecuciones sucesivas. El proceso de creación de tablas no debe utilizarse como sustituto de una copia de seguridad.

**Importante:** el proyecto no necesita ejecutar `conexion.py` ni `crear_bd.py` por separado para iniciar normalmente. `main.py` es su punto de entrada.

### Ejercicio de prueba de API por separado

```powershell
python src/main_prueba.py
```

Este archivo permite probar el dólar observado con una petición real o respuestas simuladas. Es un ejercicio independiente y **no reemplaza** el menú de APIs integrado en `main.py`.

## 8. Base de datos

El esquema actual contiene **11 tablas**:

| Tabla | Uso |
|---|---|
| `cargo` | Catálogo de cargos laborales. |
| `empleado` | Datos laborales, contacto, cargo, contratación y salario. |
| `usuario` | Nombre de cuenta, hash de contraseña, rol y vínculo único con empleado. |
| `departamento` | Departamentos y gerente designado. |
| `proyecto` | Proyectos, fechas de inicio y descripciones. |
| `registro_tiempo` | Horas, fechas, tareas y relaciones con empleado y proyecto. |
| `departamento_empleado` | Relación entre departamentos y empleados. |
| `departamento_proyecto` | Relación entre departamentos y proyectos. |
| `proyecto_empleado` | Relación entre proyectos y empleados. |
| `indicador_api` | Observaciones del dólar con fuente, código, fecha y valor. |
| `clima_api` | Observaciones climáticas con ciudad, fecha/hora y variables meteorológicas. |

Las tablas de indicadores utilizan claves únicas para evitar duplicar la misma observación de una fuente y fecha (o fecha/hora para clima).

**Persistencia y límites:** las validaciones están en el código de entrada, el dominio y los DAO correspondientes. Algunas columnas SQLite son `TEXT`; por ello, no todas las restricciones de longitud están expresadas como `CHECK` de la base. Si se edita manualmente la base, se puede eludir parte de la validación de Python.

## 9. Organización del proyecto

```text
Ecotech_JC_ev3/
├── README.md
├── requirements.txt
├── .env.example
├── integracion_IA.md
├── Docs/
│   └── Modificable.drawio
├── tests/
│   └── test_validaciones_unificadas.py
└── src/
    ├── main.py
    ├── main_prueba.py
    ├── validaciones.py
    ├── dominio/
    │   ├── empleado.py, departamento.py, proyecto.py, registroTiempo.py
    │   ├── usuario.py, cargo.py, gestionPermisos.py, Gestion_departamento.py
    │   └── indicador.py, clima.py, pronostico.py
    ├── persistencia/
    │   ├── conexion.py, crear_bd.py, semilla_db.py, semilla_admin.py
    │   ├── empleado_dao.py, departamento_dao.py, proyecto_dao.py
    │   ├── registroTiempo_dao.py, usuario_dao.py
    │   └── indicador_dao.py, clima_dao.py
    ├── servicios/
    │   ├── autenticacion.py, autorizacion.py, empleados.py, mi_cuenta.py
    │   ├── indicadores_api.py, indicadores.py, deserializador_indicador.py
    │   ├── clima_api.py, clima.py, deserializador_clima.py
    │   ├── pronostico_clima.py, deserializador_pronostico.py
    │   └── pagos_internacionales.py
    ├── menus/
    │   ├── menu_usuario.py, menu_empleado.py, menu_departamento.py
    │   ├── menu_proyecto.py, menu_registroTiempo.py, menu_apis.py
    │   └── menu_dominio_*.py
    └── complementos/
        ├── complementos.py
        └── entrada_segura.py
```

**Responsabilidad de cada carpeta:**

- `dominio/`: objetos y reglas de negocio.
- `persistencia/`: conexión, creación de tablas, semillas y DAO.
- `servicios/`: operaciones de negocio, autorización, APIs, deserialización y cálculos.
- `menus/`: presentación de información y formularios de consola.
- `complementos/`: limpieza de pantalla y entrada de contraseñas con asteriscos.
- `validaciones.py`: único módulo compartido de validaciones.
- `Docs/`: UML y material gráfico, incluido el archivo editable `Modificable.drawio`.

## 10. Pruebas

Desde la raíz del proyecto:

```powershell
python -m unittest discover -s tests -v
```

El archivo `tests/test_validaciones_unificadas.py` cubre límites de longitud, símbolos, corrección por campo, `LISTAR`, `CANCELAR`, uso de DAO, SQLite temporal, semilla y algunas rutas de navegación. Las pruebas incluidas no equivalen a una verificación de todas las operaciones del sistema.

**Pendiente para una verificación completa en el equipo de entrega:** inicio de sesión con el paquete `bcrypt` real, uso del terminal de Windows, conexión MySQL si se utiliza ese motor y consultas en vivo a ambas APIs. Algunas pruebas automatizadas simulan importaciones de dependencias no disponibles, sin probar sus conexiones reales.

## 11. Problemas frecuentes

| Síntoma | Comprobación recomendada |
|---|---|
| `pip` no se reconoce | Usar `python -m pip install -r requirements.txt` y verificar la instalación de Python. |
| `ModuleNotFoundError` | Activar el entorno virtual e instalar las dependencias desde la raíz. |
| No se encuentra la base de datos | Revisar `DB_ENGINE`, `DB_NAME` y la carpeta desde donde se ejecuta `main.py`. |
| Falla la conexión MySQL | Verificar servidor, puerto, base creada y credenciales del `.env`. |
| No se muestran asteriscos | Usar una terminal interactiva de VS Code/PowerShell. Si no es compatible, se oculta la entrada. |
| Una API no responde | Revisar conexión; la observación almacenada puede utilizarse como respaldo cuando corresponda. |
| Un usuario no ve los módulos | Revisar su rol. El cargo Recursos Humanos no es igual al rol `admin`. |
| Fallan imports de validaciones | Comprobar que exista `src/validaciones.py` y que se hayan eliminado los dos módulos de validación antiguos. |

## 12. Uso de inteligencia artificial y documentación

Las herramientas de IA se emplearon como apoyo para analizar importaciones, revisar validaciones, razonar sobre controles de acceso, depurar errores y diseñar pruebas. Las propuestas deben contrastarse con el código real, verificarse y justificarse, especialmente cuando afectan seguridad y persistencia.

El archivo `integracion_IA.md` recoge una explicación general de su utilización. Para la evaluación de la Unidad 3 conviene complementarlo con ejemplos concretos de **problema detectado → cambio realizado → prueba aplicada → justificación técnica**.

## 13. Limitaciones conocidas

- La conversión CLP→USD es una **estimación de referencia**, no una transferencia ni un sistema de remuneraciones internacionales.
- El pronóstico se elige mediante un catálogo fijo de ciudades; los proyectos no tienen una ubicación geográfica propia vinculada automáticamente al pronóstico.
- El pronóstico de tres días se consulta en línea y no se persiste como historial de pronósticos. `clima_api` almacena observaciones del clima actual.
- Para completar la evaluación conviene ejecutar pruebas con las dependencias reales y documentar sus evidencias.
- El sistema utiliza datos de demostración y no está preparado, sin controles adicionales, para almacenar información laboral real en producción.

---

**Finalidad:** demostrar POO, persistencia relacional, autenticación con bcrypt, permisos por roles y cargos, validaciones reutilizables, manejo de errores, deserialización de JSON e integración de APIs externas en una aplicación de consola Python.
