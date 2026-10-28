from getpass import getpass

from complementos.complementos import limpiar_pantalla
from dominio.usuario import Usuario
from menus.menu_usuario import pedir_dato
from menus.validaciones import ErrorFormulario, explicar_error, leer_entero, leer_texto, preguntar_reintento
from persistencia.usuario_dao import UsuarioDAO
from servicios.autenticacion import autenticar


def menu_dominio_gestionPermisos(gestion_permisos):
    reintento = None
    while True:
        opcion = reintento
        reintento = None
        if opcion is None:
            limpiar_pantalla()
            print("\n===== GESTIÓN DE PERMISOS (DEMOSTRACIÓN) =====")
            print("1. Ver cuentas y permisos de prueba")
            print("2. Otorgar permiso de prueba")
            print("0. Volver al menú principal")
            opcion = input("Seleccione una opción: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return
        try:
            if opcion == "1":
                cuentas = UsuarioDAO.listar()
                if not cuentas:
                    print("No hay cuentas. Registre alguna en el menú Usuario.")
                for cuenta in cuentas:
                    permisos = gestion_permisos.listar_permisos(cuenta["id"])
                    print(f"ID: {cuenta['id']} | Usuario: {cuenta['nombre_usuario']} | "
                        f"Permisos: {', '.join(permisos) or 'Sin permisos'}")
            elif opcion == "2":
                nombre = pedir_dato("Usuario encargado: ", Usuario.normalizar_usuario, leer=lambda mensaje: input(mensaje))
                clave = getpass("Contraseña del encargado: ")
                encargado = autenticar(nombre, clave)
                if encargado is None:
                    raise ErrorFormulario("No se pudo comprobar la cuenta encargada.")
                if encargado["nombre_usuario"] != "admin":
                    raise ErrorFormulario("Solo la cuenta inicial admin puede otorgar permisos de prueba.")

                id_usuario = leer_entero("ID del usuario destinatario: ")
                usuario = UsuarioDAO.buscar_por_id(id_usuario)
                if usuario is None:
                    raise ErrorFormulario("Usuario destinatario no encontrado.")
                permiso = leer_texto("Permiso de prueba: ", campo="El permiso", maximo=80)
                if not gestion_permisos.otorgar_permiso(encargado, usuario, permiso):
                    raise ErrorFormulario("El permiso ya existe o los datos no son válidos.")
                print("Permiso de prueba asignado correctamente.")
            else:
                print("Opción no válida.")
                continue
        except Exception as error:
            explicar_error(error, "gestionar los permisos")
            if preguntar_reintento():
                reintento = opcion
            continue
        print("Nota: estos permisos solo viven en memoria y no protegen funciones de EcoTech.")
        input("\nPresione Enter para continuar...")
