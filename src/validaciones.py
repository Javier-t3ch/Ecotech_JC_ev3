from datetime import date
from decimal import Decimal, InvalidOperation
import re

from complementos.entrada_segura import leer_con_asteriscos


_SIMBOLOS_PERSONA = " -'.’"
_SIMBOLOS_DESCRIPCION = " .,;:!?¿¡()/-+%&'\"°º#_"
_SIMBOLOS_DIRECCION = " .,/#°º-()'’"
_CORREO = re.compile(
    r"^[A-Za-z0-9_+%-]+(?:\.[A-Za-z0-9_+%-]+)*@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63}$"
)
_TELEFONO = re.compile(r"\+?[0-9 ()-]+\Z")


def validar_texto(valor, *, tipo="descripcion", campo="El campo", maximo=100):
    if not isinstance(valor, str):
        raise ValueError(f"{campo} debe ser texto.")
    valor = valor.strip()
    if not valor:
        raise ValueError(f"{campo} es obligatorio.")
    if len(valor) > maximo:
        raise ValueError(f"{campo} no puede superar {maximo} caracteres.")

    simbolos = {
        "persona": _SIMBOLOS_PERSONA,
        "departamento": " ",
        "proyecto": " ",
        "descripcion": _SIMBOLOS_DESCRIPCION,
        "direccion": _SIMBOLOS_DIRECCION,
    }
    if tipo not in simbolos:
        raise ValueError("Tipo de texto no reconocido.")
    permitidos = simbolos[tipo]
    if tipo in ("persona", "departamento", "proyecto"):
        if not any(c.isalpha() for c in valor):
            raise ValueError(f"{campo} debe contener al menos una letra.")
    else:
        if not any(c.isalnum() for c in valor):
            raise ValueError(f"{campo} debe contener letras o números.")

    for caracter in valor:
        es_letra = caracter.isalpha()
        es_numero = caracter.isdecimal()
        if tipo == "persona":
            valido = es_letra or caracter in permitidos
        else:
            valido = es_letra or es_numero or caracter in permitidos
        if not valido:
            raise ValueError(f"{campo} contiene símbolos no permitidos.")
    return valor


def validar_correo(correo):
    if not isinstance(correo, str):
        raise ValueError("El correo debe ser texto.")
    correo = correo.strip()
    if len(correo) > 100 or not _CORREO.fullmatch(correo):
        raise ValueError("Ingrese un correo válido (máximo 100 caracteres).")
    return correo


def validar_telefono(numero):
    if not isinstance(numero, str):
        numero = str(numero)
    numero = numero.strip()
    cantidad_digitos = len(re.findall(r"[0-9]", numero))
    if len(numero) > 20 or not _TELEFONO.fullmatch(numero) or not 8 <= cantidad_digitos <= 15:
        raise ValueError("El teléfono debe contener entre 8 y 15 dígitos; se admiten +, espacios, paréntesis y guiones.")
    return numero


_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_SALARIO = re.compile(r"^[0-9]{1,10}(?:[.,][0-9]{1,2})?$")

MAX_NOMBRE = 50
MAX_CORREO = 100
MAX_TELEFONO = 20
MAX_ID = 2_147_483_647
MAX_SALARIO = Decimal("9999999999.99")
MAX_BYTES_CLAVE = 72


class FormularioCancelado(Exception):
    pass



def leer_entrada(mensaje, leer=None):

    if leer is None:
        leer = input
    try:
        valor = leer(mensaje)
    except (EOFError, KeyboardInterrupt) as error:
        raise FormularioCancelado() from error
    if valor.strip().casefold() in ("cancelar", ":q", "salir"):
        raise FormularioCancelado()
    return valor


def leer_secreto(mensaje):
    while True:
        valor = leer_entrada(mensaje, leer_con_asteriscos)
        if len(valor.encode("utf-8")) > MAX_BYTES_CLAVE:
            print(f"La contraseña no puede superar {MAX_BYTES_CLAVE} bytes UTF-8.")
            continue
        return valor


def pedir_dato(mensaje, validador, leer=None):

    while True:
        try:
            return validador(leer_entrada(mensaje, leer))
        except (TypeError, ValueError) as error:
            print(f"{error} Intente nuevamente o escriba CANCELAR.")


def _resumen_id_disponible(registro):
    if isinstance(registro, dict):
        numero = registro.get("id")
        nombre = registro.get("nombre_usuario") or registro.get("nombre")
    else:
        numero = next((getattr(registro, campo) for campo in
                       ("_id", "_id_departamento", "_id_proyecto", "_id_registro", "id")
                       if getattr(registro, campo, None) is not None), None)
        nombre = next((getattr(registro, campo) for campo in
                       ("_nombre", "nombre_usuario", "_descripcion_tarea")
                       if getattr(registro, campo, None)), None)
    return f"ID: {numero}" + (f" | {nombre}" if nombre else "")


def leer_id_existente(mensaje, buscar, *, etiqueta="El registro", obligatorio=True,
                     condicion=None, mensaje_condicion="La selección no es válida.", listar=None):
    if listar is not None:
        print("Escriba LISTAR para ver los IDs disponibles o CANCELAR para volver.")

    while True:
        texto = leer_entrada(mensaje).strip()
        if texto.casefold() == "listar" and listar is not None:
            registros = listar()
            disponibles = [registro for registro in registros
                           if condicion is None or condicion(registro)]
            if not disponibles:
                print("No hay registros disponibles para esta operación.")
            else:
                print("\n===== IDs DISPONIBLES =====")
                for registro in disponibles:
                    print(_resumen_id_disponible(registro))
                print()
            continue
        if not texto and not obligatorio:
            return None
        if not re.fullmatch(r"[0-9]{1,10}", texto):
            print("Ingrese un ID compuesto solo por dígitos, o escriba LISTAR o CANCELAR.")
            continue
        numero = int(texto)
        if not 1 <= numero <= MAX_ID:
            print(f"El ID debe estar entre 1 y {MAX_ID}.")
            continue
        objeto = buscar(numero)
        if objeto is None:
            print(f"{etiqueta} no existe. Pruebe con otro ID, LISTAR o CANCELAR.")
            continue
        if condicion is not None and not condicion(objeto):
            print(f"{mensaje_condicion} Escriba LISTAR para ver las opciones disponibles.")
            continue
        return numero


def avisar_cancelacion():
    print("Operación cancelada. No se guardaron los datos de este formulario.")


def aviso_cancelacion():
    print("(Durante un formulario escriba CANCELAR en cualquier campo para volver al menú.)")


def leer_texto(mensaje, *, obligatorio=True, campo="Este campo", maximo=MAX_NOMBRE,
               persona=False, tipo="descripcion"):
    while True:
        valor = leer_entrada(mensaje).strip()
        if not valor and not obligatorio:
            return ""
        try:
            return validar_texto(
                valor, tipo="persona" if persona else tipo, campo=campo, maximo=maximo
            )
        except ValueError as error:
            print(f"{error} Intente nuevamente o escriba CANCELAR.")


def leer_telefono(mensaje, *, obligatorio=True):
    while True:
        valor = leer_entrada(mensaje).strip()
        if not valor and not obligatorio:
            return ""
        try:
            return validar_telefono(valor)
        except ValueError as error:
            print(f"{error} Intente nuevamente o escriba CANCELAR.")


def leer_correo(mensaje, *, obligatorio=True, ocupado=None):
    while True:
        valor = leer_entrada(mensaje).strip()
        if not valor and not obligatorio:
            return ""
        try:
            valor = validar_correo(valor)
        except ValueError as error:
            print(f"{error} Intente nuevamente o escriba CANCELAR.")
            continue
        if ocupado is not None and ocupado(valor):
            print("Ya existe un registro con ese correo. Ingrese otro.")
            continue
        return valor


def leer_fecha(mensaje, *, obligatorio=True):
    while True:
        valor = leer_entrada(mensaje).strip()
        if not valor and not obligatorio:
            return None
        if not _FECHA.fullmatch(valor):
            print("Ingrese una fecha con formato AAAA-MM-DD, por ejemplo 2026-10-20.")
            continue
        try:
            return date.fromisoformat(valor)
        except ValueError:
            print("La fecha no existe. Revise el dia y el mes.")


def leer_entero(mensaje, *, obligatorio=True, minimo=1, maximo=MAX_ID):
    while True:
        valor = leer_entrada(mensaje).strip()
        if not valor and not obligatorio:
            return None
        if not re.fullmatch(r"[0-9]{1,10}", valor):
            print("Ingrese un número entero válido de hasta 10 dígitos.")
            continue
        numero = int(valor)
        if not minimo <= numero <= maximo:
            print(f"Ingrese un número entre {minimo} y {maximo}.")
            continue
        return numero


def leer_real(mensaje, *, obligatorio=True, minimo=0, maximo=MAX_SALARIO):
    while True:
        valor = leer_entrada(mensaje).strip()
        if not valor and not obligatorio:
            return None
        if not _SALARIO.fullmatch(valor):
            print("Ingrese un monto con hasta 10 dígitos enteros y 2 decimales, sin separador de miles.")
            continue
        try:
            numero = Decimal(valor.replace(",", "."))
        except InvalidOperation:
            print("Ingrese un monto numérico válido.")
            continue
        if not Decimal(str(minimo)) <= numero <= Decimal(str(maximo)):
            print(f"Ingrese un monto entre {minimo} y {maximo}.")
            continue
        return float(numero)


def leer_confirmacion(mensaje):
    while True:
        valor = leer_entrada(mensaje).strip().lower()
        if valor in ("s", "n"):
            return valor
        print("Responda 's' para si o 'n' para no.")


def leer_contrasena(mensaje="Contrasena (minimo 8 caracteres): "):
    while True:
        valor = leer_secreto(mensaje)
        if len(valor) >= 8:
            return valor
        print("La contraseña debe tener al menos 8 caracteres. Intente nuevamente.")


class ErrorFormulario(ValueError):
    pass


def explicar_error(error, operacion):
    if isinstance(error, ErrorFormulario):
        print(f"No se pudo completar el formulario: {error}")

    elif isinstance(error, ValueError):
        print(
            f"No se pudo {operacion}. "
            "Revisa que los datos ingresados sean válidos."
        )

    else:
        print(
            f"No se pudo {operacion}. "
            "Comprueba los datos y la conexión e intenta nuevamente."
        )


def preguntar_reintento():
    try:
        return leer_confirmacion(
            "¿Deseas intentar nuevamente el formulario? (s/n, CANCELAR para volver): "
        ) == "s"
    except FormularioCancelado:
        return False
