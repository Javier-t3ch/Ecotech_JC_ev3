from menus.validaciones import (
    leer_texto, leer_confirmacion, ErrorFormulario,
    explicar_error, preguntar_reintento
)
from complementos.complementos import limpiar_pantalla


def menu_dominio_gestionDepartamento(gestion_departamentos):
    reintento = None
    while True:
        hubo_error = False
        if reintento is None:
            limpiar_pantalla()
            print("\n===== DOMINIO GESTION DEPARTAMENTO (DEMOSTRACION) =====")
            print("1. Crear departamento")
            print("2. Buscar departamento")
            print("3. Editar departamento")
            print("4. Eliminar departamento")
            print("5. Listar departamentos de la demostracion")
            print("0. Volver al menu principal")
            opcion = input("Seleccione una opcion: ").strip()
            limpiar_pantalla()
        else:
            opcion = reintento
            reintento = None
            limpiar_pantalla()

        if opcion == "0":
            return
        elif opcion in ("1", "2", "3", "4"):
            try:
                if opcion == "1":
                    nombre = leer_texto("Nombre del departamento: ", campo="Nombre", maximo=100)
                    departamento = gestion_departamentos.crear_departamento(nombre)
                    if departamento is False:
                        raise ErrorFormulario("Ya existe un departamento con ese nombre.")
                    print("Departamento creado:", departamento._nombre)
                    print("Nota: este ejemplo no guarda datos en la base de datos.")

                elif opcion == "2":
                    nombre = leer_texto("Nombre a buscar: ", campo="Nombre", maximo=100)
                    departamento = gestion_departamentos.buscar_departamento(nombre)
                    if departamento is False:
                        raise ErrorFormulario("Departamento no encontrado.")
                    print("Departamento encontrado:", departamento._nombre)

                elif opcion == "3":
                    nombre = leer_texto("Nombre actual del departamento: ", campo="Nombre", maximo=100)
                    departamento = gestion_departamentos.buscar_departamento(nombre)
                    if departamento is False:
                        raise ErrorFormulario("Departamento no encontrado.")
                    nuevo_nombre = leer_texto("Nuevo nombre: ", campo="Nombre", maximo=100)
                    if not gestion_departamentos.editar_departamento(departamento, nuevo_nombre):
                        raise ErrorFormulario("El nuevo nombre no es valido o ya existe.")
                    print("Departamento actualizado:", departamento._nombre)

                elif opcion == "4":
                    nombre = leer_texto("Nombre del departamento a eliminar: ", campo="Nombre", maximo=100)
                    departamento = gestion_departamentos.buscar_departamento(nombre)
                    if departamento is False:
                        raise ErrorFormulario("Departamento no encontrado.")
                    if leer_confirmacion("Confirmar eliminacion (s/n): ") == "s":
                        if not gestion_departamentos.eliminar_departamento(departamento):
                            raise ErrorFormulario("No se puede eliminar un departamento con empleados o proyectos.")
                        print("Departamento eliminado.")
                    else:
                        print("Eliminacion cancelada.")

            except Exception as error:
                explicar_error(error, "procesar el departamento de demostracion")
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "5":
            if not gestion_departamentos._departamentos:
                print("No hay departamentos creados en la demostracion.")
            else:
                for departamento in gestion_departamentos._departamentos:
                    print("-", departamento._nombre)
        else:
            print("Opcion no valida.")

        if reintento is not None or hubo_error:
            continue
        input("\nPresione Enter para continuar...")
