from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from dominio.registroTiempo import RegistroTiempo
from persistencia.conexion import abrir_conexion
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao
from persistencia.registroTiempo_dao import RegistroTiempoDAO


EMPLEADOS_DEMO = [
    ('Ana González', 'Av. Providencia 123', 912345678, 'ana.gonzalez@empresa.cl', '2022-03-15', 1200000, 'Analista de Recursos Humanos'),
    ('Carlos Muñoz', 'Av. Las Condes 456', 923456789, 'carlos.munoz@empresa.cl', '2021-07-10', 1500000, 'Contador'),
    ('María López', 'Calle Huérfanos 789', 934567890, 'maria.lopez@empresa.cl', '2023-01-20', 1300000, 'Especialista en Marketing'),
    ('Pedro Ramírez', 'Av. Apoquindo 321', 945678901, 'pedro.ramirez@empresa.cl', '2020-11-05', 2000000, 'Desarrollador de Software'),
    ('Sofía Torres', 'Calle Manuel Montt 654', 956789012, 'sofia.torres@empresa.cl', '2024-06-01', 1100000, 'Ejecutiva de Ventas'),
    ('Diego Fernández', 'Av. Grecia 789', 967890123, 'diego.fernandez@empresa.cl', '2022-08-12', 1400000, 'Diseñador Gráfico'),
    ('Camila Rojas', 'Calle San Diego 234', 978901234, 'camila.rojas@empresa.cl', '2021-04-18', 1600000, 'Jefa de Finanzas'),
    ('Javier Silva', 'Av. Macul 567', 989012345, 'javier.silva@empresa.cl', '2023-09-25', 1250000, 'Asistente Administrativo'),
    ('Valentina Castro', 'Calle Irarrázaval 890', 991234567, 'valentina.castro@empresa.cl', '2020-02-14', 1800000, 'Ingeniera de Software'),
    ('Matías Herrera', 'Av. Vicuña Mackenna 111', 912345670, 'matias.herrera@empresa.cl', '2024-02-05', 1150000, 'Ejecutivo Comercial'),
    ('Daniela Morales', 'Calle Moneda 222', 923456780, 'daniela.morales@empresa.cl', '2022-12-01', 1350000, 'Analista Contable'),
    ('Felipe Ortiz', 'Av. Independencia 333', 934567801, 'felipe.ortiz@empresa.cl', '2021-06-20', 1700000, 'Administrador de Sistemas'),
    ('Isidora Vega', 'Calle Bellavista 444', 945678012, 'isidora.vega@empresa.cl', '2023-05-10', 1280000, 'Community Manager'),
    ('Tomás Reyes', 'Av. Santa Rosa 555', 956789123, 'tomas.reyes@empresa.cl', '2020-09-08', 1900000, 'Ingeniero Civil'),
    ('Fernanda Navarro', 'Calle Portugal 666', 967890234, 'fernanda.navarro@empresa.cl', '2024-01-15', 1180000, 'Reclutadora'),
    ('Sebastián Flores', 'Av. Departamental 777', 978901245, 'sebastian.flores@empresa.cl', '2022-07-22', 1450000, 'Analista de Datos'),
    ('Constanza Medina', 'Calle Carmen 888', 989012356, 'constanza.medina@empresa.cl', '2021-10-30', 1550000, 'Coordinadora de Proyectos'),
    ('Nicolás Aguilera', 'Av. Tobalaba 999', 991234568, 'nicolas.aguilera@empresa.cl', '2023-11-12', 1320000, 'Técnico Informático'),
    ('Javiera Soto', 'Calle Eleuterio Ramírez 101', 912345671, 'javiera.soto@empresa.cl', '2020-05-19', 1750000, 'Supervisora de Ventas'),
    ('Benjamín Contreras', 'Av. Matta 202', 923456781, 'benjamin.contreras@empresa.cl', '2024-08-03', 1220000, 'Asistente de Marketing'),
]

DEPARTAMENTOS_DEMO = [
    "Recursos Humanos", "Finanzas", "Marketing", "Tecnología", "Ventas",
]

PROYECTOS_DEMO = [
    ("Modernización RRHH", "2026-03-01", "Digitalización de los procesos de contratación"),
    ("Control Financiero", "2026-02-12", "Seguimiento de presupuestos y gastos"),
    ("Campaña EcoTech Verde", "2026-04-05", "Difusión digital de productos sostenibles"),
    ("Portal EcoTech", "2026-01-20", "Implementación del portal corporativo"),
    ("Gestión de Clientes", "2026-06-10", "Organización y seguimiento comercial"),
]

REGISTROS_DEMO = [
    ("ana.gonzalez@empresa.cl", "Modernización RRHH", "2026-03-06", 4, "Revisión de postulaciones"),
    ("fernanda.navarro@empresa.cl", "Modernización RRHH", "2026-03-07", 3, "Actualización de perfiles"),
    ("carlos.munoz@empresa.cl", "Control Financiero", "2026-02-18", 6, "Consolidación presupuestaria"),
    ("daniela.morales@empresa.cl", "Control Financiero", "2026-02-19", 5, "Revisión de gastos"),
    ("maria.lopez@empresa.cl", "Campaña EcoTech Verde", "2026-04-10", 4, "Planificación de campaña"),
    ("diego.fernandez@empresa.cl", "Campaña EcoTech Verde", "2026-04-11", 5, "Diseño de material gráfico"),
    ("pedro.ramirez@empresa.cl", "Portal EcoTech", "2026-01-27", 8, "Desarrollo del módulo principal"),
    ("valentina.castro@empresa.cl", "Portal EcoTech", "2026-01-28", 6, "Pruebas del sistema"),
    ("sofia.torres@empresa.cl", "Gestión de Clientes", "2026-06-15", 5, "Clasificación de clientes"),
    ("javiera.soto@empresa.cl", "Gestión de Clientes", "2026-06-16", 3, "Informe comercial"),
]


TABLAS = (
    "departamento", "empleado", "proyecto", "registro_tiempo",
    "proyecto_empleado",  
)


def contar_registros():
    conexion = abrir_conexion()
    try:
        cursor = conexion.cursor()
        cantidades = {}
        for tabla in TABLAS:  
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            cantidades[tabla] = cursor.fetchone()[0]
        return cantidades
    finally:
        conexion.close()


def cargar_departamentos():
    encontrados = {d._nombre.strip().casefold(): d for d in DepartamentoDAO.listar()}
    for nombre in DEPARTAMENTOS_DEMO:
        clave = nombre.strip().casefold()
        if clave in encontrados:
            print(f"Ya existe departamento: {nombre}")
            continue
        nuevo = Departamento(nombre=nombre)
        DepartamentoDAO.insertar(nuevo)
        encontrados[clave] = nuevo
        print(f"Departamento creado: {nombre}")
    return {nombre: encontrados[nombre.casefold()] for nombre in DEPARTAMENTOS_DEMO}


def cargar_empleados():
    encontrados = {e._correo.strip().casefold(): e for e in EmpleadoDAO.listar()}
    for nombre, direccion, numero, correo, fecha, salario, cargo in EMPLEADOS_DEMO:
        clave = correo.strip().casefold()
        if clave in encontrados:
            print(f"Ya existe empleado: {correo}")
            continue
        nuevo = Empleado(nombre, direccion, str(numero), correo, fecha, salario, cargo)
        EmpleadoDAO.insertar(nuevo)
        encontrados[clave] = nuevo
        print(f"Empleado creado: {correo}")
    return encontrados


def cargar_proyectos():
    encontrados = {p._nombre.strip().casefold(): p for p in ProyectoDao.listar()}
    for nombre, fecha, descripcion in PROYECTOS_DEMO:
        clave = nombre.strip().casefold()
        if clave in encontrados:
            print(f"Ya existe proyecto: {nombre}")
            continue
        nuevo = Proyecto(nombre, fecha, descripcion)
        ProyectoDao.insertar(nuevo)
        encontrados[clave] = nuevo
        print(f"Proyecto creado: {nombre}")
    return {nombre: encontrados[nombre.casefold()] for nombre, _, _ in PROYECTOS_DEMO}


def asignar_empleados_para_registros(empleados, proyectos):
    for correo, nombre_proyecto, _, _, _ in REGISTROS_DEMO:
        empleado = empleados[correo]
        proyecto = proyectos[nombre_proyecto]
        if RegistroTiempoDAO.empleado_asignado(empleado._id, proyecto._id_proyecto):
            continue
        if not ProyectoDao.asignar_empleado(proyecto, empleado):
            raise ValueError(
                f"No se pudo asignar {correo} al proyecto {nombre_proyecto}"
            )
        print(f"Asignación creada: {correo} -> {nombre_proyecto}")


def cargar_registros_tiempo(empleados, proyectos):
    existentes = {
        (
            registro._empleado._id,
            registro._proyecto._id_proyecto,
            str(registro._fecha_trabajada),
            registro._descripcion_tarea.strip().casefold(),
        )
        for registro in RegistroTiempoDAO.listar()
    }

    for correo, nombre_proyecto, fecha, horas, descripcion in REGISTROS_DEMO:
        empleado = empleados[correo]
        proyecto = proyectos[nombre_proyecto]
        clave = (empleado._id, proyecto._id_proyecto, fecha, descripcion.casefold())
        if clave in existentes:
            print(f"Ya existe registro: {correo} - {nombre_proyecto} - {fecha}")
            continue
        if horas <= 0:
            raise ValueError(f"Horas inválidas en semilla: {correo} - {fecha}")
        if not RegistroTiempoDAO.empleado_asignado(empleado._id, proyecto._id_proyecto):
            raise ValueError(f"{correo} no está asignado al proyecto {nombre_proyecto}")
        registro = RegistroTiempo(horas, fecha, descripcion, empleado, proyecto)
        if not RegistroTiempoDAO.insertar(registro):
            raise ValueError(f"No se pudo guardar el registro de {correo} en {nombre_proyecto}")
        existentes.add(clave)
        print(f"Registro creado: {correo} - {nombre_proyecto} - {fecha}")


def ejecutar_semilla():
    anteriores = contar_registros()
    print("\n=== INICIO DE SEMILLA ECOTECH ===")
    cargar_departamentos()
    empleados = cargar_empleados()
    proyectos = cargar_proyectos()
    asignar_empleados_para_registros(empleados, proyectos)
    cargar_registros_tiempo(empleados, proyectos)

    actuales = contar_registros()
    print("\n=== RESULTADOS DE LA EJECUCIÓN ===")
    print(f"{'Tabla':<23} {'Antes':>7} {'Después':>8} {'Nuevos':>8}")
    for tabla in TABLAS:
        antes, despues = anteriores[tabla], actuales[tabla]
        print(f"{tabla:<23} {antes:>7} {despues:>8} {despues - antes:>8}")
    print("Semilla finalizada correctamente.\n")
    return actuales

