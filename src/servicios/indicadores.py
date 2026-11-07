import requests
from persistencia.indicador_dao import IndicadorDAO
from servicios.autorizacion import exigir_sesion
from servicios.deserializador_indicador import DeserializadorIndicador
from servicios.indicadores_api import obtener_datos


def consultar_indicador(sesion):
    exigir_sesion(sesion)
    try:
        indicador = DeserializadorIndicador.desde_api(obtener_datos())
    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError):
        try:
            respaldo = IndicadorDAO.ultimo()
        except Exception:
            return None, "sin_datos", "El servicio no está disponible y no se pudo consultar el respaldo local."
        if respaldo is None:
            return None, "sin_datos", "El servicio no está disponible y no hay datos guardados."
        return respaldo, "BD local", "No se pudo consultar la API. Se muestra la última observación guardada, no una cotización actual."
    try:
        IndicadorDAO.guardar(indicador)
    except Exception:
        return indicador, "API", "El dato fue consultado, pero no pudo guardarse en la base local."
    return indicador, "API", "Dato consultado y guardado correctamente."


def obtener_historial(sesion):
    exigir_sesion(sesion)
    return IndicadorDAO.listar()
