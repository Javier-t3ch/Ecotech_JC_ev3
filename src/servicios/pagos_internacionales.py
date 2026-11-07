from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

from servicios.autorizacion import exigir_sesion
from servicios.indicadores import consultar_indicador


_MONTOS = re.compile(r"^[0-9]{1,12}(?:[.,][0-9]{1,2})?$")


def validar_monto_clp(texto):
    if not isinstance(texto, str) or not _MONTOS.fullmatch(texto.strip()):
        raise ValueError("Ingrese un monto CLP positivo, sin separador de miles y con hasta 2 decimales.")
    try:
        monto = Decimal(texto.strip().replace(",", "."))
    except InvalidOperation as error:
        raise ValueError("El monto ingresado no es válido.") from error
    if monto <= 0 or monto > Decimal("999999999999.99"):
        raise ValueError("El monto debe ser positivo y menor a un billón de pesos.")
    return monto


def calcular_usd(monto_clp, cotizacion):
    if not isinstance(monto_clp, Decimal) or not monto_clp.is_finite() or monto_clp <= 0:
        raise ValueError("El monto en CLP no es válido.")
    try:
        cambio = Decimal(str(cotizacion))
    except (InvalidOperation, TypeError) as error:
        raise ValueError("La cotización no es válida.") from error
    if not cambio.is_finite() or cambio <= 0:
        raise ValueError("La cotización debe ser positiva.")
    return (monto_clp / cambio).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def estimar_pago(sesion, monto_clp):
    exigir_sesion(sesion)
    if not isinstance(monto_clp, Decimal) or not monto_clp.is_finite() or monto_clp <= 0:
        raise ValueError("El monto en CLP no es válido.")
    indicador, origen, mensaje = consultar_indicador(sesion)
    if indicador is None:
        return None, mensaje
    resultado = {
        "monto_clp": monto_clp,
        "monto_usd": calcular_usd(monto_clp, indicador.valor),
        "tasa_clp_usd": indicador.valor,
        "fecha": indicador.fecha,
        "verificado_en": indicador.verificado_en,
        "fuente": indicador.fuente,
        "origen": origen,
    }
    return resultado, mensaje
