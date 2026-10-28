
from datetime import date
from getpass import getpass
import math
import re


_CORREO = re.compile(r"^[^@\s]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}$")
_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def leer_texto(mensaje, *, obligatorio=True, campo="Este campo", maximo=200, persona=False):
    while True:
        valor = input(mensaje).strip()
        if not valor:
            if not obligatorio:
                return ""
            print(f"{campo} es obligatorio. Intente nuevamente.")
            continue
        if len(valor) > maximo:
            print(f"{campo} no puede superar {maximo} caracteres.")
            continue
        if persona and not all(c.isalpha() or c in " -'.’" for c in valor):
            print("El nombre solo puede contener letras, espacios, guiones o apostrofes.")
            continue
        if any(ord(c) < 32 for c in valor):
            print("No se permiten caracteres de control.")
            continue
        return valor


def leer_telefono(mensaje, *, obligatorio=True):
    while True:
        valor = input(mensaje).strip()
        if not valor and not obligatorio:
            return ""
        digitos = re.sub(r"\D", "", valor)
        if (not re.fullmatch(r"\+?[0-9 ()-]+", valor)
                or not 8 <= len(digitos) <= 15):
            print("Ingrese un telefono valido: entre 8 y 15 digitos; puede usar +, espacios o guiones.")
            continue
        return valor


def leer_correo(mensaje, *, obligatorio=True, ocupado=None):
    while True:
        valor = input(mensaje).strip()
        if not valor and not obligatorio:
            return ""
        if len(valor) > 150 or not _CORREO.fullmatch(valor):
            print("Ingrese un correo valido, por ejemplo nombre@empresa.cl.")
            continue
        if ocupado is not None and ocupado(valor):
            print("Ya existe un registro con ese correo. Ingrese otro.")
            continue
        return valor


def leer_fecha(mensaje, *, obligatorio=True):
    while True:
        valor = input(mensaje).strip()
        if not valor and not obligatorio:
            return None
        if not _FECHA.fullmatch(valor):
            print("Ingrese una fecha con formato AAAA-MM-DD, por ejemplo 2026-10-20.")
            continue
        try:
            return date.fromisoformat(valor)
        except ValueError:
            print("La fecha no existe. Revise el dia y el mes.")


def leer_entero(mensaje, *, obligatorio=True, minimo=1):
    while True:
        valor = input(mensaje).strip()
        if not valor and not obligatorio:
            return None
        try:
            numero = int(valor)
        except ValueError:
            print("Ingrese un numero entero valido.")
            continue
        if numero < minimo:
            print(f"Ingrese un numero mayor o igual a {minimo}.")
            continue
        return numero


def leer_real(mensaje, *, obligatorio=True, minimo=0):
    while True:
        valor = input(mensaje).strip()
        if not valor and not obligatorio:
            return None
        try:
            numero = float(valor.replace(",", "."))
        except ValueError:
            print("Ingrese un numero valido; puede usar coma o punto decimal.")
            continue
        if not math.isfinite(numero) or numero < minimo:
            print(f"Ingrese un monto finito mayor o igual a {minimo}.")
            continue
        return numero


def leer_confirmacion(mensaje):
    while True:
        valor = input(mensaje).strip().lower()
        if valor in ("s", "n"):
            return valor
        print("Responda 's' para si o 'n' para no.")


def leer_contrasena(mensaje="Contrasena (minimo 8 caracteres): "):
    while True:
        valor = getpass(mensaje)
        if len(valor) >= 8:
            return valor
        print("La contrasena debe tener al menos 8 caracteres. Intente nuevamente.")


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
    return leer_confirmacion(
        "¿Deseas intentar nuevamente el formulario? (s/n): "
    ) == "s"