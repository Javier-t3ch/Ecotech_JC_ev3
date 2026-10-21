from menus.validaciones import (
    ErrorFormulario, explicar_error, preguntar_reintento,
    leer_texto, leer_fecha, leer_entero,
    leer_confirmacion
)
from complementos.complementos import limpiar_pantalla
from dominio.proyecto import Proyecto
from persistencia.proyecto_dao import ProyectoDao


def mostrar_menu_proyecto():
    print("\n===== PROYECTOS - ECOTECH =====")
    print("1. Registrar Proyecto")
    print("2. Listar Proyectos")
    print("3. Buscar Proyecto")
    print("4. Actualizar Proyecto")
    print("5. Eliminar Proyecto")
    print("0. Volver al menu principal")


def main_proyecto():
    reintento = None
    while True:
        hubo_error = False
        if reintento is None:
            limpiar_pantalla()
            mostrar_menu_proyecto()
            opcion = input("Seleccione una opcion: ")
            limpiar_pantalla()

        else:
            opcion = reintento
            reintento = None
            limpiar_pantalla()
        if opcion == "1":
            try:
                nombre = leer_texto("Nombre: ", campo="Nombre", maximo=100)
                fecha_inicio = leer_fecha("Fecha de inicio (AAAA-MM-DD): ")
                descripcion = leer_texto("Descripcion: ", campo="La descripcion", maximo=500)
                if not nombre or not descripcion:
                    raise ErrorFormulario("Nombre y descripcion son obligatorios.")
                proyecto = Proyecto(nombre, fecha_inicio, descripcion)
                ProyectoDao.insertar(proyecto)
                print("Proyecto registrado con ID:", proyecto._id_proyecto)
            except ValueError as error:
                explicar_error(error, 'registrar proyecto')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'registrar proyecto')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "2":
            try:
                proyectos = ProyectoDao.listar()
                if not proyectos:
                    print("No hay proyectos registrados.")
                else:
                    for p in proyectos:
                        print(f"ID: {p._id_proyecto} | {p._nombre} | Inicio: {p._fecha_inicio} | {p._descripcion}")
            except Exception as error:
                explicar_error(error, 'consultar proyecto')

        elif opcion == "3":
            try:
                id_proyecto = leer_entero("ID del proyecto: ")
                p = ProyectoDao.buscar_por_id(id_proyecto)
                if p is None:
                    raise ErrorFormulario("Proyecto no encontrado.")
                else:
                    print(f"ID: {p._id_proyecto} | {p._nombre} | Inicio: {p._fecha_inicio} | {p._descripcion}")
            except ValueError as error:
                explicar_error(error, 'buscar proyecto')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'buscar proyecto')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "4":
            try:
                id_proyecto = leer_entero("ID del proyecto a actualizar: ")
                p = ProyectoDao.buscar_por_id(id_proyecto)
                if p is None:
                    raise ErrorFormulario("Proyecto no encontrado.")
                nombre = leer_texto(f"Nombre [{p._nombre}]: ", obligatorio=False, campo="Nombre", maximo=100)
                fecha_texto = leer_fecha(f"Fecha de inicio [{p._fecha_inicio}] (AAAA-MM-DD): ", obligatorio=False)
                descripcion = leer_texto(f"Descripcion [{p._descripcion}]: ", obligatorio=False, campo="La descripcion", maximo=500)
                if not (nombre or fecha_texto or descripcion):
                    raise ErrorFormulario("No ingresaste cambios.")
                fecha = fecha_texto if fecha_texto is not None else p._fecha_inicio
                actualizado = Proyecto(
                    nombre=nombre or p._nombre,
                    fecha_inicio=fecha,
                    descripcion=descripcion or p._descripcion,
                    id_proyecto=p._id_proyecto
                )
                if ProyectoDao.actualizar(actualizado):
                    print("Proyecto actualizado.")
                else:
                    raise ErrorFormulario("No se detectaron cambios guardados.")
            except ValueError as error:
                explicar_error(error, 'actualizar proyecto')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'actualizar proyecto')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "5":
            try:
                id_proyecto = leer_entero("ID del proyecto a eliminar: ")
                p = ProyectoDao.buscar_por_id(id_proyecto)
                if p is None:
                    raise ErrorFormulario("Proyecto no encontrado.")
                confirmar = leer_confirmacion(f"Eliminar {p._nombre}? (s/n): ")
                if confirmar == "s":
                    if ProyectoDao.eliminar(id_proyecto):
                        print("Proyecto eliminado.")
                    else:
                        raise ErrorFormulario("No se pudo eliminar el proyecto.")
                else:
                    print("Eliminacion cancelada.")
            except ValueError as error:
                explicar_error(error, 'eliminar proyecto')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'eliminar proyecto')
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
    main_proyecto()
