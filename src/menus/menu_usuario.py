from validaciones import FormularioCancelado, avisar_cancelacion, aviso_cancelacion, leer_id_existente, leer_entrada, leer_secreto
from complementos.complementos import limpiar_pantalla

from dominio.usuario import Usuario
from dominio.cargo import nombre_cargo
from persistencia.empleado_dao import EmpleadoDAO
from validaciones import preguntar_reintento, leer_texto, leer_correo, pedir_dato, leer_entero, leer_fecha
from menus.menu_apis import menu_apis
from menus.menu_empleado import contratar_y_asignar_empleado, asignar_empleado_existente
from servicios.autenticacion import autenticar, registrar_usuario
from servicios.autorizacion import exigir_admin, exigir_sesion, puede_contratar
from servicios.mi_cuenta import (
    mi_ficha, mis_registros, mis_proyectos, mis_departamentos, actualizar_mis_datos,
    registrar_mis_horas,
)


def _validar_id(texto):
    if not isinstance(texto, str) or not texto.isascii() or not texto.isdecimal() or len(texto) > 10:
        raise ValueError("Ingrese un ID de empleado compuesto solo por dígitos.")
    try:
        empleado_id = int(texto)
    except (TypeError, ValueError) as error:
        raise ValueError("Ingrese un ID de empleado numérico.") from error
    if not 1 <= empleado_id <= 2_147_483_647:
        raise ValueError("El ID del empleado debe estar entre 1 y 2147483647.")
    return empleado_id


def solicitar_registro(usuario_actual=None):
    try:
        exigir_admin(usuario_actual)
    except PermissionError as error:
        print(error)
        return None

    print("\n===== REGISTRAR CUENTA (ROL EMPLEADO) =====")
    aviso_cancelacion()
    try:
        disponibles = EmpleadoDAO.listar_sin_cuenta()
        if not disponibles:
            print("Todos los empleados registrados ya tienen una cuenta de usuario.")
            return None

        print("\n===== EMPLEADOS SIN CUENTA =====")
        print(f"{'ID':<6} {'Nombre':<30} Cargo")
        print("-" * 58)
        for empleado in disponibles:
            print(f"{empleado._id:<6} {empleado._nombre:<30} "
                f"{nombre_cargo(empleado._id_cargo)}")
        ids_disponibles = {empleado._id for empleado in disponibles}

        def validar_seleccion(texto):
            if texto.strip() == "0":
                return 0
            empleado_id = _validar_id(texto)
            if empleado_id not in ids_disponibles:
                raise ValueError("Seleccione un ID de la lista de empleados sin cuenta.")
            return empleado_id

        empleado_id = pedir_dato("\nID del empleado (0 para cancelar): ", validar_seleccion)
        if empleado_id == 0:
            avisar_cancelacion()
            return None

        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, leer_secreto)
        while True:
            confirmacion = leer_secreto("Repita la contraseña: ")
            if confirmacion == clave:
                break
            print("Las contraseñas no coinciden. Repita solamente la confirmación.")

        cuenta_id = registrar_usuario(empleado_id, nombre, clave, usuario_actual)
        print(f"Cuenta creada correctamente. ID: {cuenta_id}")
        return cuenta_id
    except FormularioCancelado:
        avisar_cancelacion()
        return None
    except (ValueError, TypeError, PermissionError) as error:
        print(f"No se pudo registrar la cuenta: {error}")
        return None
    except Exception:
        print("No se pudo guardar la cuenta. Revisa la conexión e inténtalo nuevamente.")
        return None


def solicitar_login():
    limpiar_pantalla()
    print("\n===== INICIAR SESIÓN =====")
    aviso_cancelacion()
    try:
        nombre = pedir_dato("Usuario: ", Usuario.normalizar_usuario)
        clave = leer_secreto("Contraseña: ")
        cuenta = autenticar(nombre, clave)
    except FormularioCancelado:
        avisar_cancelacion()
        return None
    except Exception:
        print("No fue posible validar el acceso. Revisa la conexión.")
        return None
    if cuenta is None:
        print("Usuario o contraseña incorrectos.")
        return None
    print("Sesión iniciada correctamente.")
    return cuenta


def mostrar_perfil(sesion):
    try:
        empleado = mi_ficha(sesion)
        if empleado is None:
            print("No se encontró la ficha del empleado.")
            return
        print("\n===== MI FICHA =====")
        print("Usuario:", sesion["nombre_usuario"], "| Rol:", sesion["rol"])
        print("ID:", empleado._id, "| Nombre:", empleado._nombre)
        print("Correo:", empleado._correo)
        print("Cargo:", nombre_cargo(empleado._id_cargo), f"(ID {empleado._id_cargo})")
        print("Dirección:", empleado._direccion)
        print("Teléfono:", empleado._numero)
        print("Fecha de contrato:", empleado._fecha_contrato)
        print("Salario:", empleado._salario)
    except PermissionError as error:
        print(error)
    except FormularioCancelado:
        avisar_cancelacion()
    except Exception:
        print("No se pudieron recuperar los datos. Revisa la conexión e inténtalo nuevamente.")


def mostrar_registros(sesion):
    try:
        registros = mis_registros(sesion)
        print("\n===== MIS REGISTROS DE TIEMPO =====")
        if not registros:
            print("No tienes registros de tiempo.")
        for reg in registros:
            print(f"{reg._fecha_trabajada} | {reg._horas_trabajadas} h | "
                f"{reg._proyecto._nombre} | {reg._descripcion_tarea}")
    except PermissionError as error:
        print(error)
    except FormularioCancelado:
        avisar_cancelacion()
    except Exception:
        print("No se pudieron recuperar los datos. Revisa la conexión e inténtalo nuevamente.")


def mostrar_proyectos(sesion):
    try:
        proyectos = mis_proyectos(sesion)
        print("\n===== MIS PROYECTOS =====")
        if not proyectos:
            print("No estás asignado a ningún proyecto.")
        for p in proyectos:
            print(f"ID: {p._id_proyecto} | {p._nombre} | Inicio: {p._fecha_inicio}")
            print("Descripción:", p._descripcion)
    except PermissionError as error:
        print(error)
    except FormularioCancelado:
        avisar_cancelacion()
    except Exception:
        print("No se pudieron recuperar los datos. Revisa la conexión e inténtalo nuevamente.")


def mostrar_departamentos(sesion):
    try:
        departamentos = mis_departamentos(sesion)
        print("\n===== MI DEPARTAMENTO =====")
        if not departamentos:
            print("No tienes un departamento asignado.")
        for d in departamentos:
            print(f"ID: {d._id_departamento} | {d._nombre}")
    except PermissionError as error:
        print(error)
    except FormularioCancelado:
        avisar_cancelacion()
    except Exception:
        print("No se pudieron recuperar los datos. Revisa la conexión e inténtalo nuevamente.")


def modificar_mis_datos(sesion):
    try:
        empleado = mi_ficha(sesion)
        if empleado is None:
            print("No se encontró el empleado.")
            return
        print("Solo puedes editar tu propio nombre y correo.")
        nombre = leer_texto(f"Nombre [{empleado._nombre}] (Enter = mantener): ",
                        obligatorio=False, campo="Nombre", maximo=50, persona=True)
        correo = leer_correo(f"Correo [{empleado._correo}] (Enter = mantener): ",
                            obligatorio=False,
                            ocupado=lambda c: EmpleadoDAO.correo_ocupado(c, empleado._id))
        nombre = nombre or empleado._nombre
        correo = correo or empleado._correo
        if nombre == empleado._nombre and correo == empleado._correo:
            print("No ingresaste cambios.")
        elif actualizar_mis_datos(sesion, nombre, correo):
            print("Datos personales actualizados correctamente.")
        else:
            print("No se pudieron actualizar los datos.")
    except (PermissionError, ValueError) as error:
        print(f"No se pudo actualizar tu ficha: {error}")
    except FormularioCancelado:
        avisar_cancelacion()
    except Exception:
        print("No se pudo guardar la modificación. Revisa la conexión e inténtalo nuevamente.")


def solicitar_registro_horas(sesion):
    print("\n===== REGISTRAR MIS HORAS =====")
    aviso_cancelacion()
    try:
        proyectos = mis_proyectos(sesion)
        if not proyectos:
            print("No tienes proyectos asignados, por lo que no puedes registrar horas.")
            return None
        print("\nProyectos asignados:")
        for proyecto in proyectos:
            print(f"{proyecto._id_proyecto}. {proyecto._nombre}")
        ids = {p._id_proyecto for p in proyectos}

        def validar_proyecto(valor):
            if valor.strip() == "0":
                return 0
            try:
                numero = int(valor)
            except ValueError as error:
                raise ValueError("Ingrese un ID de proyecto numérico.") from error
            if numero not in ids:
                raise ValueError("Seleccione uno de los proyectos asignados.")
            return numero

        proyecto_id = pedir_dato("ID del proyecto (0 para cancelar): ", validar_proyecto)
        if proyecto_id == 0:
            avisar_cancelacion()
            return None
        horas = leer_entero("Horas trabajadas: ", minimo=1, maximo=24)
        fecha = leer_fecha("Fecha trabajada (AAAA-MM-DD): ")
        descripcion = leer_texto("Descripción de la tarea: ", campo="La descripción", maximo=100)
        registro = registrar_mis_horas(sesion, proyecto_id, horas, fecha, descripcion)
        print(f"Registro creado correctamente. ID: {registro._id_registro}")
        return registro
    except FormularioCancelado:
        avisar_cancelacion()
    except (PermissionError, ValueError) as error:
        print(f"No se pudieron registrar las horas: {error}")
    except Exception:
        print("No se pudieron guardar las horas. Revisa la conexión e inténtalo nuevamente.")
    return None


def _opciones_menu_privado(usuario_actual):
    es_admin = usuario_actual["rol"] == "admin"
    es_rrhh = puede_contratar(usuario_actual)
    opciones = [
        ("ficha", "Mi ficha"),
        ("modificar", "Modificar mis datos (nombre y correo)"),
        ("registros", "Mis registros de tiempo"),
        ("proyectos", "Mis proyectos"),
        ("departamentos", "Mi departamento"),
    ]
    if es_admin:
        opciones.extend([
            ("registro_usuario", "Registrar usuario para un empleado"),
            ("modulos", "Abrir módulos EcoTech (administración)"),
        ])
    opciones.extend([
        ("horas", "Registrar mis horas"),
        ("apis", "Servicios externos (APIs)"),
    ])
    if es_rrhh:
        opciones.extend([
            ("contratar", "Contratar empleado y asignarlo a departamento (RRHH)"),
            ("asignar", "Asignar empleado existente a departamento (RRHH)"),
        ])
    opciones.append(("cerrar", "Cerrar sesión"))
    return {str(numero): entrada for numero, entrada in enumerate(opciones, start=1)}


def menu_privado(usuario_actual, menu_modulos=None):
    try:
        exigir_sesion(usuario_actual)
    except PermissionError as error:
        print(error)
        return "9"

    while True:
        try:
            exigir_sesion(usuario_actual)
        except PermissionError as error:
            print(error)
            return "9"

        opciones = _opciones_menu_privado(usuario_actual)
        limpiar_pantalla()
        print("\n===== MENÚ PRIVADO ECOTECH =====")
        for numero, (_, descripcion) in opciones.items():
            print(f"{numero}. {descripcion}")
        print("0. Salir")
        aviso_cancelacion()
        opcion = input("Seleccione una opción: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return "0"

        seleccion = opciones.get(opcion)
        if seleccion is None:
            print("Opción no válida o no autorizada.")
            input("\nPresione Enter para continuar...")
            continue

        accion = seleccion[0]
        if accion == "cerrar":
            return "9"
        if accion == "ficha":
            mostrar_perfil(usuario_actual)
        elif accion == "modificar":
            modificar_mis_datos(usuario_actual)
        elif accion == "registros":
            mostrar_registros(usuario_actual)
        elif accion == "proyectos":
            mostrar_proyectos(usuario_actual)
        elif accion == "departamentos":
            mostrar_departamentos(usuario_actual)
        elif accion == "horas":
            solicitar_registro_horas(usuario_actual)
        elif accion == "apis":
            menu_apis(usuario_actual)
            continue
        elif accion == "contratar":
            contratar_y_asignar_empleado(usuario_actual)
        elif accion == "asignar":
            asignar_empleado_existente(usuario_actual)
        elif accion == "registro_usuario":
            solicitar_registro(usuario_actual)
        elif accion == "modulos":
            if menu_modulos is not None:
                menu_modulos()
                continue
            print("Los módulos no están disponibles.")
        input("\nPresione Enter para continuar...")
