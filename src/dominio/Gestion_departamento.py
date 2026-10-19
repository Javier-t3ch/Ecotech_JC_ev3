from dominio.departamento import Departamento


class GestionDepartamento:

    def __init__(self):
        self._departamentos = []

    def crear_departamento(self, nombre):
        if not nombre or nombre.strip() == "":
            return False
        nombre = nombre.strip()
        if self.buscar_departamento(nombre) != False:
            return False
        departamento = Departamento(nombre)
        self._departamentos.append(departamento)
        return departamento

    def eliminar_departamento(self, departamento):
        if departamento not in self._departamentos:
            return False
        if departamento._empleados or departamento._proyectos:
            return False
        self._departamentos.remove(departamento)
        return True

    def editar_departamento(self, departamento, nuevo_nombre):
        if departamento not in self._departamentos:
            return False
        if not nuevo_nombre or nuevo_nombre.strip() == "":
            return False
        nuevo_nombre = nuevo_nombre.strip()
        otro_departamento = self.buscar_departamento(nuevo_nombre)
        if otro_departamento != False and otro_departamento != departamento:
            return False
        departamento._nombre = nuevo_nombre
        return True

    def buscar_departamento(self, nombre):
        if not nombre or nombre.strip() == "":
            return False
        for departamento in self._departamentos:
            if departamento._nombre.lower() == nombre.strip().lower():
                return departamento
        return False