from dominio.departamento import Departamento
from validaciones import validar_texto
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from servicios.autorizacion import exigir_admin


class GestionDepartamento:
    def listar_departamentos(self, sesion):
        exigir_admin(sesion)
        return DepartamentoDAO.listar()

    def buscar_departamento(self, id_departamento, sesion):
        exigir_admin(sesion)
        return DepartamentoDAO.buscar_por_id(id_departamento)

    def _validar_nombre(self, nombre, excluir_id=None):
        nombre = validar_texto(nombre, tipo="departamento", campo="Nombre de departamento", maximo=50)
        for existente in DepartamentoDAO.listar():
            if (existente._nombre.casefold() == nombre.casefold()
                    and existente._id_departamento != excluir_id):
                raise ValueError("Ya existe un departamento con ese nombre.")
        return nombre

    def _validar_gerente(self, id_gerente):
        if id_gerente is not None and EmpleadoDAO.buscar_por_id(id_gerente) is None:
            raise ValueError("El gerente indicado no existe.")

    def crear_departamento(self, nombre, sesion, id_gerente=None):
        exigir_admin(sesion)
        nombre = self._validar_nombre(nombre)
        self._validar_gerente(id_gerente)
        return DepartamentoDAO.insertar(Departamento(nombre, id_gerente=id_gerente))

    def editar_departamento(self, id_departamento, nuevo_nombre, sesion, id_gerente=None):
        exigir_admin(sesion)
        departamento = DepartamentoDAO.buscar_por_id(id_departamento)
        if departamento is None:
            raise ValueError("Departamento no encontrado.")
        nombre = self._validar_nombre(nuevo_nombre, id_departamento)
        self._validar_gerente(id_gerente)
        departamento._nombre = nombre
        departamento._id_gerente = id_gerente
        return DepartamentoDAO.actualizar(departamento)

    def eliminar_departamento(self, id_departamento, sesion):
        exigir_admin(sesion)
        departamento = DepartamentoDAO.buscar_por_id(id_departamento)
        if departamento is None:
            raise ValueError("Departamento no encontrado.")
        if departamento._empleados or departamento._proyectos:
            raise ValueError("No se puede eliminar un departamento con empleados o proyectos.")
        return DepartamentoDAO.eliminar(id_departamento)
