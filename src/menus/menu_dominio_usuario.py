
from getpass import getpass

from complementos.complementos import limpiar_pantalla
from dominio.usuario import Usuario
from menus.menu_usuario import pedir_dato, solicitar_registro
from menus.validaciones import ErrorFormulario, explicar_error, preguntar_reintento
from persistencia.usuario_dao import UsuarioDAO
from servicios.autenticacion import autenticar, cambiar_contrasena


def menu_dominio_usuario():
    reintento = None
    while True:
        opcion = reintento
        reintento = None
        if opcion is None:
            limpiar_pantalla()
            print("\n===== CUENTAS DE USUARIO (BASE DE DATOS) =====")
            print("1. Registrar cuenta para un empleado")
            print("2. Comprobar credenciales de un usuario")
            print("3. Cambiar contraseña")
            print("4. Listar cuentas registradas")
            print("0. Volver al menú principal")
            opcion = input("Seleccione una opción: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return
        try:
            if opcion == "1":
                if solicitar_registro() is None:
                    raise ErrorFormulario("No fue posible registrar la cuenta.")
            elif opcion == "2":
                nombre = input("Usuario: ")
                clave = getpass("Contraseña: ")
                if autenticar(nombre, clave) is None:
                    raise ErrorFormulario("Usuario o contraseña incorrectos.")
                print("Credenciales correctas. La sesión actual no cambia.")
            elif opcion == "3":
                nombre = pedir_dato("Usuario: ", Usuario.normalizar_usuario, leer=lambda mensaje: input(mensaje))
                actual = getpass("Contraseña actual: ")
                nueva = pedir_dato("Nueva contraseña (mínimo 6 caracteres): ", Usuario.validar_clave, getpass)
                while getpass("Repita la nueva contraseña: ") != nueva:
                    print("Las contraseñas no coinciden. Repita la confirmación.")
                if not cambiar_contrasena(nombre, actual, nueva):
                    raise ErrorFormulario("Usuario o contraseña actual incorrectos, o clave sin cambios.")
                print("Contraseña actualizada y guardada correctamente.")
            elif opcion == "4":
                cuentas = UsuarioDAO.listar()
                if not cuentas:
                    print("Todavía no hay cuentas registradas.")
                else:
                    for cuenta in cuentas:
                        print(f"ID: {cuenta['id']} | Usuario: {cuenta['nombre_usuario']} | "
                            f"Empleado: {cuenta['empleado_id']}")
                print("No se muestran contraseñas ni hashes.")
            else:
                print("Opción no válida.")
                continue
        except Exception as error:
            explicar_error(error, "procesar la cuenta de usuario")
            if preguntar_reintento():
                reintento = opcion
            continue
        input("\nPresione Enter para continuar...")
