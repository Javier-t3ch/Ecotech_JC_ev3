from menus.validaciones import ErrorFormulario, explicar_error, preguntar_reintento, leer_texto, leer_entero
from complementos.complementos import limpiar_pantalla
from getpass import getpass

from menus.menu_dominio_usuario import buscar_usuario


def menu_dominio_gestionPermisos(usuarios, gestion_permisos):
    reintento = None
    while True:
        hubo_error = False
        if reintento is None:
            limpiar_pantalla()
            print("\n===== DOMINIO GESTION PERMISOS (DEMOSTRACION) =====")
            print("1. Ver usuarios y permisos")
            print("2. Otorgar permiso")
            print("0. Volver al menu principal")

            opcion = input("Seleccione una opcion: ").strip()
            limpiar_pantalla()

        else:
            opcion = reintento
            reintento = None
            limpiar_pantalla()
        if opcion == "0":
            return

        elif opcion == "1":
            if not usuarios:
                print("No hay usuarios. Cree uno desde el menu Usuario.")
            else:
                for usuario in usuarios:
                    print(
                        "ID:", usuario._id_usuario,
                        "| Usuario:", usuario._nombre,
                        "| Permisos:", ", ".join(usuario._permisos) or "Sin permisos"
                    )

        elif opcion == "2":
            try:
                if not usuarios:
                    raise ErrorFormulario("Primero debes crear un usuario desde el menu Usuario.")
                id_encargado = leer_entero("ID del usuario encargado: ")
                encargado = buscar_usuario(usuarios, id_encargado)
                if encargado is None:
                    raise ErrorFormulario("Encargado no encontrado.")

                contrasenia = getpass("Contrasena del encargado: ")
                if not encargado.autenticar(contrasenia):
                    raise ErrorFormulario("Autenticacion incorrecta.")

                id_usuario = leer_entero("ID del usuario que recibira el permiso: ")
                usuario = buscar_usuario(usuarios, id_usuario)
                if usuario is None:
                    raise ErrorFormulario("Usuario destinatario no encontrado.")

                permiso = leer_texto("Nombre del permiso: ", campo="El permiso")
                if gestion_permisos.otorgar_permiso(encargado, usuario, permiso):
                    print("Permiso otorgado correctamente.")
                else:
                    raise ErrorFormulario("No se pudo otorgar: encargado sin autorizacion, permiso vacio o repetido.")

            except Exception as error:
                explicar_error(error, 'otorgar el permiso')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        else:
            print("Opcion no valida.")
        if reintento is not None or hubo_error:
            continue
        input("\nPresione Enter para continuar...")
