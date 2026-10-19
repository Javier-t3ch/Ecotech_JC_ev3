from complementos.complementos import limpiar_pantalla
from getpass import getpass

from menus.menu_dominio_usuario import buscar_usuario


def menu_dominio_gestionPermisos(usuarios, gestion_permisos):
    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO GESTION PERMISOS (DEMOSTRACION) =====")
        print("1. Ver usuarios y permisos")
        print("2. Otorgar permiso")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()
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
            if not usuarios:
                print("Primero debe crear usuarios desde el menu Usuario.")
                input("\nPresione Enter para continuar...")
                continue

            try:
                id_encargado = int(input("ID del usuario encargado: "))
                encargado = buscar_usuario(usuarios, id_encargado)
                if encargado is None:
                    print("Encargado no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue

                contrasenia = getpass("Contrasena del encargado: ")
                if not encargado.autenticar(contrasenia):
                    print("Autenticacion incorrecta.")
                    input("\nPresione Enter para continuar...")
                    continue

                id_usuario = int(input("ID del usuario que recibira el permiso: "))
                usuario = buscar_usuario(usuarios, id_usuario)
                if usuario is None:
                    print("Usuario destinatario no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue

                permiso = input("Nombre del permiso: ").strip()
                if gestion_permisos.otorgar_permiso(encargado, usuario, permiso):
                    print("Permiso otorgado correctamente.")
                else:
                    print("No se pudo otorgar: encargado sin autorizacion, permiso vacio o repetido.")

            except ValueError:
                print("Los ID deben ser numericos.")

        else:
            print("Opcion no valida.")
        input("\nPresione Enter para continuar...")
