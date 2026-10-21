from menus.validaciones import (
    ErrorFormulario, explicar_error, preguntar_reintento,
    leer_texto, leer_correo, leer_entero,
    leer_contrasena
)
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
    reintento = None
    while True:
        hubo_error = False
        if reintento is None:
            limpiar_pantalla()
            print("\n===== DOMINIO USUARIO (DEMOSTRACION) =====")
            print("1. Crear usuario para un empleado")
            print("2. Autenticar usuario")
            print("3. Cambiar contrasena")
            print("4. Listar usuarios de la demostracion")
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
            try:
                id_empleado = leer_entero("ID del empleado existente: ")
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    raise ErrorFormulario("Empleado no encontrado. Registrelo primero en el CRUD.")

                repetido = False
                for actual in usuarios:
                    if actual._empleado._id == id_empleado:
                        repetido = True
                if repetido:
                    raise ErrorFormulario("Este empleado ya tiene un usuario en la demostracion.")

                nombre = leer_texto("Nombre de usuario: ", campo="Nombre", maximo=100)
                mail = leer_correo(
                    "Correo del usuario: ",
                    ocupado=lambda c: any(u._mail.casefold() == c.casefold() for u in usuarios)
                )
                if nombre == "" or "@" not in mail or "." not in mail:
                    raise ErrorFormulario("Ingrese un nombre y un correo validos.")

                contrasenia = leer_contrasena("Contrasena (minimo 8 caracteres): ")
                if len(contrasenia) < 8:
                    raise ErrorFormulario("La contrasena debe tener al menos 8 caracteres.")

                existe_mail = False
                for actual in usuarios:
                    if actual._mail.lower() == mail.lower():
                        existe_mail = True
                if existe_mail:
                    raise ErrorFormulario("Ya existe un usuario con ese correo.")

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

            except Exception as error:
                explicar_error(error, 'procesar la operacion de usuario')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion in ("2", "3"):
            try:
                id_usuario = leer_entero("ID del usuario: ")
                usuario = buscar_usuario(usuarios, id_usuario)
                if usuario is None:
                    raise ErrorFormulario("Usuario no encontrado.")

                contrasenia = getpass("Contrasena actual: ")

                if opcion == "2":
                    if usuario.autenticar(contrasenia):
                        print("Autenticacion correcta.")
                    else:
                        raise ErrorFormulario("Contrasena incorrecta.")

                elif opcion == "3":
                    nueva = leer_contrasena("Nueva contrasena (minimo 8 caracteres): ")
                    if usuario.cambiar_contrasenia(contrasenia, nueva):
                        print("Contrasena cambiada correctamente.")
                    else:
                        raise ErrorFormulario("No se pudo cambiar la contrasena.")

            except Exception as error:
                explicar_error(error, 'procesar la operacion de usuario')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

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
        if reintento is not None or hubo_error:
            continue
        input("\nPresione Enter para continuar...")
