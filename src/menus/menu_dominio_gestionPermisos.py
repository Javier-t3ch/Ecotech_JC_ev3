from complementos.complementos import limpiar_pantalla, pausar_y_limpiar
from validaciones import (FormularioCancelado, avisar_cancelacion, aviso_cancelacion,
                                leer_id_existente, leer_confirmacion, explicar_error)
from persistencia.usuario_dao import UsuarioDAO
from servicios.autorizacion import exigir_admin


def menu_dominio_gestionPermisos(gestion_permisos, usuario_actual=None):
    try:
        exigir_admin(usuario_actual)
    except PermissionError as error:
        print(error)
        return

    while True:
        limpiar_pantalla()
        print("\n===== GESTIÓN DE PERMISOS =====")
        print("1. Listar cuentas y roles")
        print("2. Otorgar rol admin a una cuenta")
        print("0. Volver a Módulos EcoTech")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "0":
            return
        limpiar_pantalla()
        try:
            exigir_admin(usuario_actual)
            if opcion == "1":
                cuentas = gestion_permisos.listar_cuentas(usuario_actual)
                if not cuentas:
                    print("No hay cuentas registradas.")
                for cuenta in cuentas:
                    print(f"ID: {cuenta['id']} | Usuario: {cuenta['nombre_usuario']} | "
                        f"Empleado: {cuenta['empleado_id']} | Rol: {cuenta['rol']}")
            elif opcion == "2":
                print("Solo una cuenta administradora puede otorgar este rol.")
                aviso_cancelacion()
                id_usuario = leer_id_existente(
                    "ID de la cuenta (LISTAR para ver cuentas): ",
                    UsuarioDAO.buscar_por_id, etiqueta="La cuenta",
                    listar=lambda: gestion_permisos.listar_cuentas(usuario_actual),
                )
                cuenta = UsuarioDAO.buscar_por_id(id_usuario)
                if cuenta.rol == "admin":
                    print("Esta cuenta ya tiene rol admin.")
                else:
                    respuesta = leer_confirmacion(
                        f"¿Convertir {cuenta.nombre_usuario} en administrador? (s/n): "
                    )
                    if respuesta == "s":
                        if gestion_permisos.otorgar_admin(usuario_actual, id_usuario):
                            print("Rol admin guardado correctamente en la base de datos.")
                        else:
                            print("El rol ya estaba asignado.")
                    else:
                        print("No se realizaron cambios.")
            else:
                print("Opción no válida.")
        except FormularioCancelado:
            avisar_cancelacion()
        except PermissionError as error:
            print(error)
            return
        except Exception as error:
            explicar_error(error, "gestionar permisos")
        pausar_y_limpiar()
