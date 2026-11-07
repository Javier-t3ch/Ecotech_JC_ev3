from validaciones import FormularioCancelado, avisar_cancelacion, aviso_cancelacion, leer_id_existente, leer_entrada, leer_secreto
from validaciones import ErrorFormulario, explicar_error, preguntar_reintento, leer_texto, leer_entero, leer_confirmacion
from dominio.departamento import Departamento
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from complementos.complementos import limpiar_pantalla

def mostrar_menu_departementos():
    print("\n===== DEPARTAMENTOS - ECOTECH =====")
    print("1. Registrar Departamento")
    print("2. Listar Departamentos")
    print("3. Buscar Departamento")
    print("4. Actualizar Departamento")
    print("5. Eliminar Departamento")
    print("0. Volver al menu principal")


def main_departamento(usuario_actual=None):
    from servicios.autorizacion import exigir_admin
    try:
        exigir_admin(usuario_actual)
    except PermissionError as error:
        print(error)
        return
    reintento = None
    while True:
        hubo_error = False
        if reintento is None:
            limpiar_pantalla()
            mostrar_menu_departementos()
            aviso_cancelacion()
            opcion = input("Seleccione una opción: ").strip()
            limpiar_pantalla()

        else:
            opcion = reintento
            reintento = None
            limpiar_pantalla()
        if opcion == "1":
            try:
                nombre = leer_texto("Nombre del departamento: ", campo="Nombre", maximo=50, tipo="departamento")
                if not nombre:
                    raise ErrorFormulario("El nombre no puede estar vacio.")
                gerente_texto = leer_id_existente("ID del gerente (Enter si no tiene): ", EmpleadoDAO.buscar_por_id, etiqueta="El gerente", obligatorio=False)
                id_gerente = gerente_texto if gerente_texto is not None else None
                if id_gerente is not None and EmpleadoDAO.buscar_por_id(id_gerente) is None:
                    raise ErrorFormulario("El empleado indicado como gerente no existe.")
                departamento = Departamento(nombre, id_gerente=id_gerente)
                DepartamentoDAO.insertar(departamento)
                print("Departamento registrado con ID:", departamento._id_departamento)
            except FormularioCancelado:
                avisar_cancelacion()
            except ValueError as error:
                explicar_error(error, 'registrar departamento')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'registrar departamento')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "2":
            try:
                departamentos = DepartamentoDAO.listar()
                if not departamentos:
                    print("No hay departamentos registrados.")
                else:
                    for d in departamentos:
                        print(f"ID: {d._id_departamento} | Nombre: {d._nombre} | Gerente: {d._id_gerente}")
            except Exception as error:
                explicar_error(error, 'consultar departamento')

        elif opcion == "3":
            try:
                id_departamento = leer_id_existente("ID del departamento: ", DepartamentoDAO.buscar_por_id, etiqueta="El departamento")
                d = DepartamentoDAO.buscar_por_id(id_departamento)
                if d is None:
                    raise ErrorFormulario("Departamento no encontrado.")
                else:
                    print(f"ID: {d._id_departamento} | Nombre: {d._nombre} | Gerente: {d._id_gerente}")
            except FormularioCancelado:
                avisar_cancelacion()
            except ValueError as error:
                explicar_error(error, 'buscar departamento')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'buscar departamento')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "4":
            try:
                id_departamento = leer_id_existente("ID del departamento a actualizar: ", DepartamentoDAO.buscar_por_id, etiqueta="El departamento")
                d = DepartamentoDAO.buscar_por_id(id_departamento)
                if d is None:
                    raise ErrorFormulario("Departamento no encontrado.")
                nombre = leer_texto(f"Nombre [{d._nombre}]: ", obligatorio=False, campo="Nombre", maximo=50, tipo="departamento")
                gerente_texto = leer_id_existente(f"ID gerente [{d._id_gerente}] (Enter para mantener): ", EmpleadoDAO.buscar_por_id, etiqueta="El gerente", obligatorio=False)
                if not nombre and not gerente_texto:
                    raise ErrorFormulario("No ingresaste cambios.")
                id_gerente = gerente_texto if gerente_texto is not None else d._id_gerente
                if id_gerente is not None and EmpleadoDAO.buscar_por_id(id_gerente) is None:
                    raise ErrorFormulario("El gerente indicado no existe.")
                actualizado = Departamento(
                    nombre=nombre or d._nombre,
                    id_departamento=d._id_departamento,
                    id_gerente=id_gerente
                )
                if DepartamentoDAO.actualizar(actualizado):
                    print("Departamento actualizado.")
                else:
                    raise ErrorFormulario("No se detectaron cambios guardados.")
            except FormularioCancelado:
                avisar_cancelacion()
            except ValueError as error:
                explicar_error(error, 'actualizar departamento')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'actualizar departamento')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "5":
            try:
                id_departamento = leer_id_existente("ID del departamento a eliminar: ", DepartamentoDAO.buscar_por_id, etiqueta="El departamento")
                d = DepartamentoDAO.buscar_por_id(id_departamento)
                if d is None:
                    raise ErrorFormulario("Departamento no encontrado.")
                confirmar = leer_confirmacion(f"Eliminar {d._nombre}? (s/n): ")
                if confirmar == "s":
                    if DepartamentoDAO.eliminar(id_departamento):
                        print("Departamento eliminado.")
                    else:
                        raise ErrorFormulario("No se pudo eliminar el departamento.")
                else:
                    print("Eliminacion cancelada.")
            except FormularioCancelado:
                avisar_cancelacion()
            except ValueError as error:
                explicar_error(error, 'eliminar departamento')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'eliminar departamento')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "0":
            return
        else:
            print("Opcion no valida.")
        if reintento is not None:
            continue
        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main_departamento()
