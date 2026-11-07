from complementos.complementos import limpiar_pantalla, pausar_y_limpiar
from validaciones import (FormularioCancelado, avisar_cancelacion, aviso_cancelacion,
                                leer_id_existente, leer_texto, leer_confirmacion,
                                explicar_error)
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from servicios.autorizacion import exigir_admin


def menu_dominio_gestionDepartamento(gestion_departamentos, usuario_actual=None):
    try:
        exigir_admin(usuario_actual)
    except PermissionError as error:
        print(error)
        return
    while True:
        limpiar_pantalla()
        print("\n===== GESTIÓN DE DEPARTAMENTOS ===== ")
        print("1. Crear departamento")
        print("2. Buscar departamento")
        print("3. Editar departamento")
        print("4. Eliminar departamento")
        print("5. Listar departamentos")
        print("0. Volver a Módulos EcoTech")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "0":
            return
        limpiar_pantalla()
        try:
            exigir_admin(usuario_actual)
            if opcion == "1":
                aviso_cancelacion()
                nombre = leer_texto("Nombre del departamento: ", campo="Nombre", maximo=50, tipo="departamento")
                id_gerente = leer_id_existente(
                    "ID gerente (Enter = sin gerente): ", EmpleadoDAO.buscar_por_id,
                    etiqueta="El empleado", obligatorio=False, listar=EmpleadoDAO.listar)
                departamento = gestion_departamentos.crear_departamento(
                    nombre, usuario_actual, id_gerente)
                print(f"Departamento creado en BD con ID: {departamento._id_departamento}")
            elif opcion in ("2", "3", "4"):
                aviso_cancelacion()
                id_departamento = leer_id_existente(
                    "ID del departamento: ", DepartamentoDAO.buscar_por_id,
                    etiqueta="El departamento", listar=DepartamentoDAO.listar)
                departamento = gestion_departamentos.buscar_departamento(id_departamento, usuario_actual)
                if opcion == "2":
                    print(f"ID: {departamento._id_departamento} | Nombre: {departamento._nombre} "
                        f"| Gerente: {departamento._id_gerente or 'Sin gerente'}")
                    print(f"Empleados asignados: {len(departamento._empleados)} | "
                        f"Proyectos vinculados: {len(departamento._proyectos)}")
                elif opcion == "3":
                    nombre = leer_texto(f"Nombre [{departamento._nombre}] (Enter = mantener): ",
                                        obligatorio=False, campo="Nombre", maximo=50, tipo="departamento")
                    id_gerente = leer_id_existente(
                        f"ID gerente [{departamento._id_gerente}] (Enter = mantener): ",
                        EmpleadoDAO.buscar_por_id, etiqueta="El empleado",
                        obligatorio=False, listar=EmpleadoDAO.listar)
                    nombre = nombre or departamento._nombre
                    id_gerente = departamento._id_gerente if id_gerente is None else id_gerente
                    if nombre == departamento._nombre and id_gerente == departamento._id_gerente:
                        print("No ingresaste cambios.")
                    elif gestion_departamentos.editar_departamento(
                            id_departamento, nombre, usuario_actual, id_gerente):
                        print("Departamento actualizado en la base de datos.")
                    else:
                        print("No se pudo actualizar el departamento.")
                else:
                    if leer_confirmacion(f"¿Eliminar {departamento._nombre}? (s/n): ") == "s":
                        if gestion_departamentos.eliminar_departamento(id_departamento, usuario_actual):
                            print("Departamento eliminado de la base de datos.")
                    else:
                        print("Eliminación cancelada.")
            elif opcion == "5":
                departamentos = gestion_departamentos.listar_departamentos(usuario_actual)
                if not departamentos:
                    print("No hay departamentos registrados.")
                for departamento in departamentos:
                    print(f"ID: {departamento._id_departamento} | Nombre: {departamento._nombre} "
                        f"| Gerente: {departamento._id_gerente or 'Sin gerente'}")
            else:
                print("Opción no válida.")
        except FormularioCancelado:
            avisar_cancelacion()
        except PermissionError as error:
            print(error)
            return
        except Exception as error:
            explicar_error(error, "gestionar departamentos")
        pausar_y_limpiar()
