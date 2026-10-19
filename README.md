# EcoTech Solutions — Sistema de Gestión de Empleados

**Asignatura:** TI3021 — Programación Orientada a Objeto Seguro  
**Evaluación:** Unidad 2 — Implementación de Software Orientado a Objetos en Python

## Descripción

EcoTech Solutions es un proyecto académico desarrollado en Python que simula un sistema de gestión empresarial. Permite administrar empleados, departamentos, proyectos y registros de horas trabajadas.

El programa utiliza programación orientada a objetos (POO), operaciones CRUD, conexión a bases de datos y mecanismos de manejo de errores. Su estructura está basada en un diagrama de clases UML.

## Funcionalidades principales

El sistema dispone de siete módulos:

1. **Empleado:** gestión de información laboral, consulta de salarios y registro de horas.
2. **Departamento:** contratación de empleados y administración de las relaciones con departamentos y proyectos.
3. **Proyecto:** asignación de empleados, registro de horas y generación de informes.
4. **RegistroTiempo:** creación, consulta y cálculo de registros de horas trabajadas.
5. **Usuario:** creación de usuarios, autenticación y cambio de contraseñas.
6. **GestionPermisos:** consulta y asignación de permisos.
7. **GestionDepartamento:** creación, búsqueda, edición y eliminación de departamentos mediante métodos del dominio.

Los cuatro primeros módulos incorporan menús CRUD con conexión a la base de datos. Los tres últimos funcionan como demostraciones en memoria de las clases implementadas.

## Tecnologías utilizadas

- Python 3.
- SQLite mediante `sqlite3`.
- MySQL mediante `PyMySQL`.
- `python-dotenv` para administrar la configuración.
- Git y GitHub para el control de versiones.

## Instalación

Descargar o clonar el repositorio y abrir una terminal en la carpeta principal del proyecto.

Crear un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

## Configuración de la base de datos

Crear un archivo `.env` en la carpeta principal del proyecto, utilizando `.env.example` como referencia.

**Para SQLite:**

```ini
DB_ENGINE=sqlite
DB_NAME=ecotech.db
```

**Para MySQL mediante WampServer:**

```ini
DB_ENGINE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecotech
DB_USER=root
DB_PASSWORD=
```

El puerto, usuario y contraseña deben corresponder a la configuración local de MySQL. Algunos equipos utilizan el puerto `3307`.

Antes de iniciar con MySQL debe existir la base de datos `ecotech`. Puede crearse desde phpMyAdmin.

## Ejecución

Desde la carpeta principal del proyecto:

```powershell
python src/main.py
```

El programa lee la configuración del `.env`, establece una conexión con la base seleccionada y ejecuta `crear_tablas()` antes de mostrar el menú principal.

No es necesario ejecutar `conexion.py` por separado.

## Estructura de la base de datos

El sistema utiliza siete tablas:

| Tabla | Descripción |
|---|---|
| empleado | Información de empleados |
| departamento | Información de departamentos |
| proyecto | Información de proyectos |
| registro_tiempo | Registros de horas trabajadas |
| departamento_empleado | Relación entre empleados y departamentos |
| departamento_proyecto | Relación entre departamentos y proyectos |
| proyecto_empleado | Relación entre empleados y proyectos |

Las tablas se crean cuando no existen. La creación automática no elimina registros almacenados ni actualiza estructuras antiguas.

## Comprobación del funcionamiento

Para verificar el sistema:

1. Ejecutar el programa.
2. Registrar un empleado mediante el menú CRUD.
3. Crear un departamento y un proyecto.
4. Vincular el empleado al departamento y asignarlo al proyecto.
5. Registrar horas trabajadas.
6. Consultar la información y generar un informe del proyecto.
7. Abrir la base de datos y comprobar que se hayan almacenado los registros y relaciones.

En MySQL, los datos pueden verificarse desde phpMyAdmin. Para SQLite, puede utilizarse DB Browser for SQLite.

## Organización del código

- `src/dominio/`: clases y métodos basados en el UML.
- `src/persistencia/`: conexión con bases de datos y DAO.
- `src/menus/`: menús de dominio y CRUD.
- `src/complementos/`: funciones auxiliares.
- `src/main.py`: inicio y navegación principal.
- `Docs/`: diagramas UML.

## Manejo de errores

La aplicación utiliza `try-except`, validación de entradas y restricciones de la base de datos para manejar errores como identificadores inexistentes, datos incorrectos y problemas de conexión.

## Uso de inteligencia artificial

Durante el desarrollo se utilizaron herramientas de inteligencia artificial como apoyo para revisar y mejorar fragmentos de código.

Las sugerencias deben ser analizadas, probadas y justificadas técnicamente. La documentación correspondiente se prepara como parte de la evaluación y defensa individual.

## Finalidad

Proyecto desarrollado con fines académicos para demostrar la implementación de una aplicación de consola orientada a objetos, integrada con una base de datos relacional y basada en un modelo UML.