from validaciones import (
    FormularioCancelado, avisar_cancelacion, aviso_cancelacion, leer_id_existente, leer_entrada, leer_secreto,
    ErrorFormulario, explicar_error, preguntar_reintento,
    leer_texto, leer_telefono, leer_correo,
    leer_fecha, leer_entero, leer_real, leer_confirmacion
)
from dominio.empleado import Empleado
from dominio.cargo import CARGOS, validar_id_cargo, nombre_cargo
from servicios.autorizacion import puede_contratar, exigir_recursos_humanos
from servicios.empleados import (registrar_empleado, actualizar_empleado,
                            listar_todos, buscar_empleado, eliminar_empleado,
                            asignar_empleado_a_departamento)
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from complementos.complementos import limpiar_pantalla


def correo_ya_registrado(correo, excluir_id=None):
    return any(
        e._correo.casefold() == correo.casefold() and e._id != excluir_id
        for e in EmpleadoDAO.listar()
    )


def mostrar_menu_empleado():
    print("\n===== EMPLEADOS - ECOTECH =====")
    print("1. Registrar Empleado")
    print("2. Listar Empleados")
    print("3. Buscar Empleado")
    print("4. Actualizar Empleado")
    print("5. Eliminar Empleado")
    print("0. Volver al menu principal")


def mostrar_cargos():
    print("\nCargos disponibles:")
    for id_cargo, nombre in CARGOS.items():
        print(f"  {id_cargo}. {nombre}")


def leer_id_cargo(*, actual=None):
    while True:
        valor = leer_entero(
            f"ID del cargo [{actual}] (Enter = mantener): " if actual is not None
            else "ID del cargo: ", obligatorio=actual is None
        )
        if valor is None:
            return actual
        try:
            return validar_id_cargo(valor)
        except ValueError:
            print("Seleccione uno de los cargos mostrados (1 o 2).")


def contratar_y_asignar_empleado(usuario_actual):
    try:
        exigir_recursos_humanos(usuario_actual)
        print("\n===== CONTRATAR EMPLEADO Y ASIGNAR A DEPARTAMENTO =====")
        aviso_cancelacion()
        nombre = leer_texto("Nombre: ", campo="Nombre", maximo=50, persona=True)
        direccion = leer_texto("Dirección: ", campo="La dirección", maximo=150, tipo="direccion")
        numero = leer_telefono("Número de teléfono: ")
        correo = leer_correo("Correo: ", ocupado=correo_ya_registrado)
        fecha_contrato = leer_fecha("Fecha de contrato (AAAA-MM-DD): ")
        salario = leer_real("Salario: ")
        mostrar_cargos()
        id_cargo = leer_id_cargo()
        id_departamento = leer_id_existente(
            "ID del departamento (LISTAR para ver los disponibles): ",
            DepartamentoDAO.buscar_por_id,
            etiqueta="El departamento", listar=DepartamentoDAO.listar,
        )
        empleado = Empleado(nombre, direccion, numero, correo,
                            fecha_contrato, salario, id_cargo)
        registrado = registrar_empleado(empleado, usuario_actual, id_departamento)
        print(f"Empleado registrado con ID: {registrado._id} y asignado al departamento {id_departamento}.")
        return registrado
    except FormularioCancelado:
        avisar_cancelacion()
    except PermissionError as error:
        print(error)
    except ValueError as error:
        explicar_error(error, "registrar y asignar empleado")
    except Exception:
        print("No se pudo registrar y asignar el empleado. Revisa los datos y la conexión.")
    return None


def asignar_empleado_existente(usuario_actual):
    try:
        exigir_recursos_humanos(usuario_actual)
        print("\n===== ASIGNAR EMPLEADO EXISTENTE A DEPARTAMENTO =====")
        aviso_cancelacion()
        id_departamento = leer_id_existente(
            "ID del departamento (LISTAR para ver los disponibles): ",
            DepartamentoDAO.buscar_por_id,
            etiqueta="El departamento", listar=DepartamentoDAO.listar,
        )
        departamento = DepartamentoDAO.buscar_por_id(id_departamento)
        id_empleado = leer_id_existente(
            "ID del empleado (LISTAR para ver los disponibles): ",
            EmpleadoDAO.buscar_por_id, etiqueta="El empleado",
            listar=EmpleadoDAO.listar,
            condicion=lambda e: all(a._id != e._id for a in departamento._empleados),
            mensaje_condicion="El empleado ya pertenece a ese departamento.",
        )
        if asignar_empleado_a_departamento(id_empleado, id_departamento, usuario_actual):
            print("Empleado asignado correctamente al departamento.")
            return True
        print("No se pudo guardar la asignación.")
    except FormularioCancelado:
        avisar_cancelacion()
    except PermissionError as error:
        print(error)
    except ValueError as error:
        explicar_error(error, "asignar empleado al departamento")
    except Exception:
        print("No se pudo asignar el empleado. Revisa los datos y la conexión.")
    return False


def main_empleado(usuario_actual=None):
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
            mostrar_menu_empleado()
            aviso_cancelacion()
            opcion = input("Seleccione una opción: ").strip()
            limpiar_pantalla()

        else:
            opcion = reintento
            reintento = None
            limpiar_pantalla()
        if opcion == "1":
            contratar_y_asignar_empleado(usuario_actual)

        elif opcion == "2":
            try:
                empleados = listar_todos(usuario_actual)
                if not empleados:
                    print("No hay empleados registrados.")
                else:
                    for empleado in empleados:
                        print(empleado.mostrar_datos())
            except Exception as error:
                explicar_error(error, 'consultar empleado')

        elif opcion == "3":
            try:
                id_empleado = leer_id_existente("ID del empleado: ", EmpleadoDAO.buscar_por_id, etiqueta="El empleado")
                empleado = buscar_empleado(id_empleado, usuario_actual)
                if empleado is None:
                    raise ErrorFormulario("Empleado no encontrado.")
                else:
                    print(empleado.mostrar_datos())
                    print("Telefono:", empleado._numero)
                    print("Fecha de contrato:", empleado._fecha_contrato)
                    print("Salario:", empleado.ver_salario())
            except FormularioCancelado:
                avisar_cancelacion()
            except ValueError as error:
                explicar_error(error, 'buscar empleado')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'buscar empleado')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "4":
            try:
                id_empleado = leer_id_existente("ID del empleado a actualizar: ", EmpleadoDAO.buscar_por_id, etiqueta="El empleado")
                empleado = buscar_empleado(id_empleado, usuario_actual)
                if empleado is None:
                    raise ErrorFormulario("Empleado no encontrado.")
                print("Deja el campo vacio si no quieres modificarlo.")
                nombre = leer_texto(f"Nombre [{empleado._nombre}]: ", obligatorio=False, campo="Nombre", maximo=50, persona=True)
                direccion = leer_texto(f"Direccion [{empleado._direccion}]: ", obligatorio=False, campo="La direccion", maximo=150, tipo="direccion")
                numero = leer_telefono(f"Telefono [{empleado._numero}]: ", obligatorio=False)
                correo = leer_correo(f"Correo [{empleado._correo}]: ", obligatorio=False,
                                    ocupado=lambda c: correo_ya_registrado(c, empleado._id))
                fecha_texto = leer_fecha(f"Fecha contrato [{empleado._fecha_contrato}] (AAAA-MM-DD): ", obligatorio=False)
                salario_texto = leer_real(f"Salario [{empleado._salario}]: ", obligatorio=False)
                if puede_contratar(usuario_actual):
                    mostrar_cargos()
                    id_cargo = leer_id_cargo(actual=empleado._id_cargo)
                else:
                    id_cargo = empleado._id_cargo
                    print("Cargo actual:", nombre_cargo(id_cargo), "(solo RRHH puede cambiarlo)")
                if not (nombre or direccion or numero or correo or fecha_texto is not None
                        or salario_texto is not None or id_cargo != empleado._id_cargo):
                    raise ErrorFormulario("No ingresaste cambios.")
                fecha = fecha_texto if fecha_texto is not None else empleado._fecha_contrato
                salario = salario_texto if salario_texto is not None else empleado._salario
                actualizado = Empleado(
                    nombre=nombre or empleado._nombre,
                    direccion=direccion or empleado._direccion,
                    numero=numero or empleado._numero,
                    correo=correo or empleado._correo,
                    fecha_contrato=fecha,
                    salario=salario,
                    id_cargo=id_cargo,
                    id=empleado._id
                )
                if actualizar_empleado(actualizado, usuario_actual):
                    print("Empleado actualizado correctamente.")
                else:
                    raise ErrorFormulario("No se detectaron cambios guardados.")
            except FormularioCancelado:
                avisar_cancelacion()
            except ValueError as error:
                explicar_error(error, 'actualizar empleado')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'actualizar empleado')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "5":
            try:
                id_empleado = leer_id_existente("ID del empleado a eliminar: ", EmpleadoDAO.buscar_por_id, etiqueta="El empleado")
                empleado = buscar_empleado(id_empleado, usuario_actual)
                if empleado is None:
                    raise ErrorFormulario("Empleado no encontrado.")
                print(empleado.mostrar_datos())
                confirmar = leer_confirmacion("Confirmar eliminacion (s/n): ")
                if confirmar == "s":
                    if eliminar_empleado(id_empleado, usuario_actual):
                        print("Empleado eliminado.")
                    else:
                        raise ErrorFormulario("No se pudo eliminar el empleado.")
                else:
                    print("Eliminacion cancelada.")
            except FormularioCancelado:
                avisar_cancelacion()
            except ValueError as error:
                explicar_error(error, 'eliminar empleado')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'eliminar empleado')
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
    main_empleado()