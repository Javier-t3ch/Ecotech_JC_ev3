import requests

from persistencia.clima_dao import ClimaDAO
from servicios.autorizacion import exigir_sesion
from servicios.clima_api import CIUDADES, obtener_clima
from servicios.deserializador_clima import DeserializadorClima


def _ciudad_valida(codigo_ciudad):
    if codigo_ciudad not in CIUDADES:
        raise ValueError("Seleccione una ciudad disponible.")
    return CIUDADES[codigo_ciudad][0]


def consultar_clima(sesion, codigo_ciudad):
    exigir_sesion(sesion)
    ciudad = _ciudad_valida(codigo_ciudad)
    try:
        clima = DeserializadorClima.desde_api(obtener_clima(codigo_ciudad), codigo_ciudad)
    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError):
        try:
            respaldo = ClimaDAO.ultimo(ciudad)
        except Exception:
            return None, "sin_datos", "El servicio no está disponible y no se pudo consultar la base local."
        if respaldo is None:
            return None, "sin_datos", "El servicio no está disponible y no hay datos climáticos guardados."
        return respaldo, "BD local", "No se pudo consultar la API. Se muestra el último dato guardado, que puede estar desactualizado."
    try:
        ClimaDAO.guardar(clima)
    except Exception:
        return clima, "API", "Datos climáticos consultados, pero no se pudieron guardar en la base local."
    return clima, "API", "Datos climáticos consultados y guardados correctamente."


def historial_clima(sesion, codigo_ciudad):
    exigir_sesion(sesion)
    ciudad = _ciudad_valida(codigo_ciudad)
    return ClimaDAO.listar(ciudad)
