class Proyecto:
    def __init__(self, nombre, fecha_inicio, descripcion, id_proyecto=None):
        self._id_proyecto = id_proyecto
        self._nombre = nombre
        self._fecha_inicio = fecha_inicio
        self._descripcion = descripcion
        self._empleados = []
        self._registros_tiempo = []

    def asignar_empleado(self, empleado):
        if empleado is None or empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        return True

    def desvincular_empleado(self, empleado):
        if empleado not in self._empleados:
            return False
        self._empleados.remove(empleado)
        return True

    def agregar_registro_tiempo(self, registro):
        if registro is None:
            return False
        if registro._proyecto != self:
            return False
        if registro._empleado not in self._empleados:
            return False
        if registro._horas_trabajadas <= 0:
            return False
        if registro in self._registros_tiempo:
            return False
        self._registros_tiempo.append(registro)
        return True

    def generar_informe(self):
        total_horas = 0
        for registro in self._registros_tiempo:
            total_horas += registro._horas_trabajadas
        return (
            f"Proyecto: {self._nombre}\n"
            f"Fecha de inicio: {self._fecha_inicio}\n"
            f"Descripción: {self._descripcion}\n"
            f"Cantidad de empleados: {len(self._empleados)}\n"
            f"Horas registradas: {total_horas}"
        )
