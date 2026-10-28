from menus.validaciones import (
    ErrorFormulario, explicar_error, preguntar_reintento,
    leer_texto, leer_telefono, leer_correo,
    leer_fecha, leer_entero, leer_real, leer_confirmacion
)
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO
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


def main_empleado():
    reintento = None
    while True:
        hubo_error = False
        if reintento is None:
            limpiar_pantalla()
            mostrar_menu_empleado()
            opcion = input("Seleccione una opcion: ")
            limpiar_pantalla()

        else:
            opcion = reintento
            reintento = None
            limpiar_pantalla()
        if opcion == "1":
            try:
                nombre = leer_texto("Nombre: ", campo="Nombre", maximo=100, persona=True)
                direccion = leer_texto("Direccion: ", campo="La direccion", maximo=200)
                numero = leer_telefono("Numero de telefono: ")
                correo = leer_correo("Correo: ", ocupado=correo_ya_registrado)
                fecha_contrato = leer_fecha("Fecha de contrato (AAAA-MM-DD): ")
                salario = leer_real("Salario: ")
                cargo = leer_texto("Cargo: ", campo="El cargo", maximo=100)
                empleado = Empleado(nombre, direccion, numero, correo, fecha_contrato, salario, cargo)
                EmpleadoDAO.insertar(empleado)
                print("Empleado registrado con ID:", empleado._id)
            except ValueError as error:
                explicar_error(error, 'registrar empleado')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'registrar empleado')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "2":
            try:
                empleados = EmpleadoDAO.listar()
                if not empleados:
                    print("No hay empleados registrados.")
                else:
                    for empleado in empleados:
                        print(empleado.mostrar_datos())
            except Exception as error:
                explicar_error(error, 'consultar empleado')

        elif opcion == "3":
            try:
                id_empleado = leer_entero("ID del empleado: ")
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    raise ErrorFormulario("Empleado no encontrado.")
                else:
                    print(empleado.mostrar_datos())
                    print("Telefono:", empleado._numero)
                    print("Fecha de contrato:", empleado._fecha_contrato)
                    print("Salario:", empleado.ver_salario())
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
                id_empleado = leer_entero("ID del empleado a actualizar: ")
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    raise ErrorFormulario("Empleado no encontrado.")
                print("Deja el campo vacio si no quieres modificarlo.")
                nombre = leer_texto(f"Nombre [{empleado._nombre}]: ", obligatorio=False, campo="Nombre", maximo=100, persona=True)
                direccion = leer_texto(f"Direccion [{empleado._direccion}]: ", obligatorio=False, campo="La direccion", maximo=200)
                numero = leer_telefono(f"Telefono [{empleado._numero}]: ", obligatorio=False)
                correo = leer_correo(f"Correo [{empleado._correo}]: ", obligatorio=False,
                                     ocupado=lambda c: correo_ya_registrado(c, empleado._id))
                fecha_texto = leer_fecha(f"Fecha contrato [{empleado._fecha_contrato}] (AAAA-MM-DD): ", obligatorio=False)
                salario_texto = leer_real(f"Salario [{empleado._salario}]: ", obligatorio=False)
                cargo = leer_texto(f"Cargo [{empleado._cargo}]: ", obligatorio=False, campo="El cargo", maximo=100)
                if not (nombre or direccion or numero or correo or fecha_texto is not None
                        or salario_texto is not None or cargo):
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
                    cargo=cargo or empleado._cargo,
                    id=empleado._id
                )
                if EmpleadoDAO.actualizar(actualizado):
                    print("Empleado actualizado correctamente.")
                else:
                    raise ErrorFormulario("No se detectaron cambios guardados.")
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
                id_empleado = leer_entero("ID del empleado a eliminar: ")
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    raise ErrorFormulario("Empleado no encontrado.")
                print(empleado.mostrar_datos())
                confirmar = leer_confirmacion("Confirmar eliminacion (s/n): ")
                if confirmar == "s":
                    if EmpleadoDAO.eliminar(id_empleado):
                        print("Empleado eliminado.")
                    else:
                        raise ErrorFormulario("No se pudo eliminar el empleado.")
                else:
                    print("Eliminacion cancelada.")
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
        if reintento is not None or hubo_error:
            continue
        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main_empleado()
