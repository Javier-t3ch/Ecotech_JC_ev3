from getpass import getpass

from dominio.usuario import Usuario
from servicios.autenticacion import autenticar, registrar_usuario
from menus.validaciones import preguntar_reintento


def pedir_dato(mensaje, validador, leer=input):
    """Repite únicamente el campo que no supera la validación."""
    while True:
        try:
            return validador(leer(mensaje))
        except (TypeError, ValueError) as error:
            print(f"{error} Intente nuevamente.")


def _validar_id(texto):
    try:
        empleado_id = int(texto)
    except (TypeError, ValueError) as error:
        raise ValueError("Ingrese un ID de empleado numérico.") from error
    if empleado_id <= 0:
        raise ValueError("El ID del empleado debe ser positivo.")
    return empleado_id


def solicitar_registro():
    print("\n===== REGISTRAR CUENTA =====")
    empleado_id = pedir_dato("ID del empleado: ", _validar_id)
    nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
    clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)
    while getpass("Repita la contraseña: ") != clave:
        print("Las contraseñas no coinciden. Repita la confirmación.")
    try:
        cuenta_id = registrar_usuario(empleado_id, nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo registrar la cuenta: compruebe que el empleado exista y no tenga otra cuenta.")
        return None
    except Exception:
        print("No se pudo guardar la cuenta. Revise los datos y la conexión.")
        return None
    print(f"Cuenta creada correctamente. ID: {cuenta_id}")
    return cuenta_id


def solicitar_login():
    print("\n===== INICIAR SESIÓN =====")
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    try:
        cuenta = autenticar(nombre, clave)
    except (TypeError, ValueError):
        cuenta = None
    if cuenta is None:
        print("Usuario o contraseña incorrectos.")
        return None
    print("Sesión iniciada correctamente.")
    return cuenta


def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión para ver el perfil.")
        return
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"ID de empleado: {usuario_actual['empleado_id']}")


def menu_privado(usuario_actual, menu_modulos=None):
    """No abre ninguna opción si no hay sesión; 9 cierra sesión y 0 sale."""
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"
    while True:
        print("\n===== MENÚ PRIVADO =====")
        print("1. Registrar usuario para otro empleado")
        print("2. Ver mi perfil")
        print("3. Abrir módulos EcoTech")
        print("9. Cerrar sesión")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
        if opcion == "1":
            while solicitar_registro() is None:
                if not preguntar_reintento():
                    break
        elif opcion == "2":
            mostrar_perfil(usuario_actual)
        elif opcion == "3":
            if menu_modulos is not None:
                menu_modulos()
            else:
                print("Los módulos no están disponibles.")
        else:
            print("Opción no válida.")
