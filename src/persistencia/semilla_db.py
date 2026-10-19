from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from dominio.empleado import Empleado
from dominio.departamento import Departamento


def cargar_empleados():
    empleados_ej = [
    (1, "Ana González", "Av. Providencia 123", 912345678, "ana.gonzalez@empresa.cl", "2022-03-15", 1200000, "Analista de Recursos Humanos", []),
    (2, "Carlos Muñoz", "Av. Las Condes 456", 923456789, "carlos.munoz@empresa.cl", "2021-07-10", 1500000, "Contador", []),
    (3, "María López", "Calle Huérfanos 789", 934567890, "maria.lopez@empresa.cl", "2023-01-20", 1300000, "Especialista en Marketing", []),
    (4, "Pedro Ramírez", "Av. Apoquindo 321", 945678901, "pedro.ramirez@empresa.cl", "2020-11-05", 2000000, "Desarrollador de Software", []),
    (5, "Sofía Torres", "Calle Manuel Montt 654", 956789012, "sofia.torres@empresa.cl", "2024-06-01", 1100000, "Ejecutiva de Ventas", []),
    (6, "Diego Fernández", "Av. Grecia 789", 967890123, "diego.fernandez@empresa.cl", "2022-08-12", 1400000, "Diseñador Gráfico", []),
    (7, "Camila Rojas", "Calle San Diego 234", 978901234, "camila.rojas@empresa.cl", "2021-04-18", 1600000, "Jefa de Finanzas", []),
    (8, "Javier Silva", "Av. Macul 567", 989012345, "javier.silva@empresa.cl", "2023-09-25", 1250000, "Asistente Administrativo", []),
    (9, "Valentina Castro", "Calle Irarrázaval 890", 991234567, "valentina.castro@empresa.cl", "2020-02-14", 1800000, "Ingeniera de Software", []),
    (10, "Matías Herrera", "Av. Vicuña Mackenna 111", 912345670, "matias.herrera@empresa.cl", "2024-02-05", 1150000, "Ejecutivo Comercial", []),
    (11, "Daniela Morales", "Calle Moneda 222", 923456780, "daniela.morales@empresa.cl", "2022-12-01", 1350000, "Analista Contable", []),
    (12, "Felipe Ortiz", "Av. Independencia 333", 934567801, "felipe.ortiz@empresa.cl", "2021-06-20", 1700000, "Administrador de Sistemas", []),
    (13, "Isidora Vega", "Calle Bellavista 444", 945678012, "isidora.vega@empresa.cl", "2023-05-10", 1280000, "Community Manager", []),
    (14, "Tomás Reyes", "Av. Santa Rosa 555", 956789123, "tomas.reyes@empresa.cl", "2020-09-08", 1900000, "Ingeniero Civil", []),
    (15, "Fernanda Navarro", "Calle Portugal 666", 967890234, "fernanda.navarro@empresa.cl", "2024-01-15", 1180000, "Reclutadora", []),
    (16, "Sebastián Flores", "Av. Departamental 777", 978901245, "sebastian.flores@empresa.cl", "2022-07-22", 1450000, "Analista de Datos", []),
    (17, "Constanza Medina", "Calle Carmen 888", 989012356, "constanza.medina@empresa.cl", "2021-10-30", 1550000, "Coordinadora de Proyectos", []),
    (18, "Nicolás Aguilera", "Av. Tobalaba 999", 991234568, "nicolas.aguilera@empresa.cl", "2023-11-12", 1320000, "Técnico Informático", []),
    (19, "Javiera Soto", "Calle Eleuterio Ramírez 101", 912345671, "javiera.soto@empresa.cl", "2020-05-19", 1750000, "Supervisora de Ventas", []),
    (20, "Benjamín Contreras", "Av. Matta 202", 923456781, "benjamin.contreras@empresa.cl", "2024-08-03", 1220000, "Asistente de Marketing", [])
]

    for id_empleado, nombre in empleados_ej:
        existente = EmpleadoDAO.buscar_por_id(id_empleado)
        if existente is not None:
            print(f"Ya existe: {id_empleado} Corresponde a: {nombre}")
            continue
        empleado = Empleado()
        EmpleadoDAO.insertar(empleado)
        print(f"Creado: {correo}")



def cargar_departamento():
    departamentos_ej = [
    (1, "Recursos Humanos", 1),
    (2, "Finanzas", 2),
    (3, "Marketing", 3),
    (4, "Tecnología", 4),
    (5, "Ventas", 5)
]

    for id_departamento, nombre, id_gerente in departamentos_ej:
        existente = DepartamentoDAO.buscar_por_id(id_departamento)
        if existente is not None:
            print(f"Ya existe: {id_departamento}")
            continue
        departamento = Departamento(id_departamento, nombre, id_gerente)
        DepartamentoDAO.insertar(departamento)
        print(f"Creado: {id_departamento}")