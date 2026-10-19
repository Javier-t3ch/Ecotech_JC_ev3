from complementos.complementos import limpiar_pantalla
from getpass import getpass

from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO


def buscar_usuario(usuarios, id_usuario):
    for usuario in usuarios:
        if usuario._id_usuario == id_usuario:
            return usuario
    return None


def menu_dominio_usuario(usuarios):
    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO USUARIO (DEMOSTRACION) =====")
        print("1. Crear usuario para un empleado")
        print("2. Autenticar usuario")
        print("3. Cambiar contrasena")
        print("4. Listar usuarios de la demostracion")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return

        elif opcion == "1":
            try:
                id_empleado = int(input("ID del empleado existente: "))
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    print("Empleado no encontrado. Registrelo primero en el CRUD.")
                    input("\nPresione Enter para continuar...")
                    continue

                repetido = False
                for actual in usuarios:
                    if actual._empleado._id == id_empleado:
                        repetido = True
                if repetido:
                    print("Este empleado ya tiene un usuario en la demostracion.")
                    input("\nPresione Enter para continuar...")
                    continue

                nombre = input("Nombre de usuario: ").strip()
                mail = input("Correo del usuario: ").strip()
                if nombre == "" or "@" not in mail or "." not in mail:
                    print("Ingrese un nombre y un correo validos.")
                    input("\nPresione Enter para continuar...")
                    continue

                contrasenia = getpass("Contrasena (minimo 8 caracteres): ")
                if len(contrasenia) < 8:
                    print("La contrasena debe tener al menos 8 caracteres.")
                    input("\nPresione Enter para continuar...")
                    continue

                existe_mail = False
                for actual in usuarios:
                    if actual._mail.lower() == mail.lower():
                        existe_mail = True
                if existe_mail:
                    print("Ya existe un usuario con ese correo.")
                    input("\nPresione Enter para continuar...")
                    continue

                usuario = Usuario(
                    nombre=nombre,
                    mail=mail,
                    contrasenia=contrasenia,
                    empleado=empleado,
                    id_usuario=len(usuarios) + 1
                )

                if len(usuarios) == 0:
                    usuario._permisos.append("administrar_permisos")
                    print("Primer usuario: administrador de demostracion.")

                usuarios.append(usuario)
                print("Usuario creado. ID:", usuario._id_usuario)
                print("Nota: se conserva solo mientras el programa este abierto.")

            except ValueError:
                print("El ID del empleado debe ser un numero.")
            except Exception as error:
                print("Error al crear usuario:", error)

        elif opcion in ("2", "3"):
            try:
                id_usuario = int(input("ID del usuario: "))
                usuario = buscar_usuario(usuarios, id_usuario)
                if usuario is None:
                    print("Usuario no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue

                contrasenia = getpass("Contrasena actual: ")

                if opcion == "2":
                    if usuario.autenticar(contrasenia):
                        print("Autenticacion correcta.")
                    else:
                        print("Contrasena incorrecta.")

                elif opcion == "3":
                    nueva = getpass("Nueva contrasena: ")
                    if usuario.cambiar_contrasenia(contrasenia, nueva):
                        print("Contrasena cambiada correctamente.")
                    else:
                        print("No se pudo cambiar la contrasena.")

            except ValueError:
                print("El ID del usuario debe ser un numero.")

        elif opcion == "4":
            if not usuarios:
                print("Aun no hay usuarios en esta prueba.")
            else:
                for usuario in usuarios:
                    print(
                        "ID:", usuario._id_usuario,
                        "| Nombre:", usuario._nombre,
                        "| Empleado:", usuario._empleado._id,
                        "| Permisos:", ", ".join(usuario._permisos) or "Sin permisos"
                    )

        else:
            print("Opcion no valida.")
        input("\nPresione Enter para continuar...")
