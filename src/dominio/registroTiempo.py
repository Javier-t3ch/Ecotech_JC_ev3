class RegistroTiempo:
    def __init__(self, horas_trabajadas, fecha_trabajada, descripcion_tarea,
                empleado, proyecto, id_registro=None):
        self._id_registro = id_registro
        self._horas_trabajadas = horas_trabajadas
        self._fecha_trabajada = fecha_trabajada
        self._descripcion_tarea = descripcion_tarea
        self._empleado = empleado
        self._proyecto = proyecto

    def calculo_horas(self, registros):
        total_horas = 0
        for registro in registros:
            mismo_empleado = registro._empleado == self._empleado
            if self._empleado._id is not None:
                if registro._empleado._id == self._empleado._id:
                    mismo_empleado = True
            if mismo_empleado:
                total_horas += registro._horas_trabajadas
        return total_horas

    def calculo_horas_proyecto(self, registros, proyecto):
        total_horas = 0
        for registro in registros:
            mismo_empleado = registro._empleado == self._empleado
            mismo_proyecto = registro._proyecto == proyecto
            if self._empleado._id is not None:
                if registro._empleado._id == self._empleado._id:
                    mismo_empleado = True
            if proyecto._id_proyecto is not None:
                if registro._proyecto._id_proyecto == proyecto._id_proyecto:
                    mismo_proyecto = True
            if mismo_empleado and mismo_proyecto:
                total_horas += registro._horas_trabajadas
        return total_horas
