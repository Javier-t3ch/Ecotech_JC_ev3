import math
import requests

URL_DOLAR = "https://mindicador.cl/api/dolar"


def obtener_datos():
    respuesta = requests.get(URL_DOLAR, timeout=(3, 5))
    respuesta.raise_for_status()
    return respuesta.json()


def extraer_primero(datos):
    if not isinstance(datos, dict) or datos.get("codigo") != "dolar":
        raise ValueError("La respuesta no corresponde al dólar observado.")
    if datos.get("unidad_medida") != "Pesos":
        raise ValueError("La unidad del dólar no es válida.")
    serie = datos.get("serie")
    if not isinstance(serie, list) or not serie:
        raise ValueError("La respuesta no contiene observaciones.")
    registro = serie[0]
    if not isinstance(registro, dict):
        raise ValueError("El registro del indicador no es válido.")
    fecha, valor = registro.get("fecha"), registro.get("valor")
    if not isinstance(fecha, str) or not fecha.strip():
        raise ValueError("La fecha del indicador no es válida.")
    if type(valor) not in (int, float) or not math.isfinite(valor) or valor <= 0:
        raise ValueError("El valor del indicador no es válido.")
    return fecha, valor
