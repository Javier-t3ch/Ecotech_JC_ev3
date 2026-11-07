from datetime import datetime, timezone

from servicios.autorizacion import exigir_sesion
from servicios.clima_api import obtener_pronostico
from servicios.deserializador_pronostico import DeserializadorPronostico


def consultar_pronostico(sesion, codigo_ciudad):
    exigir_sesion(sesion)
    datos = obtener_pronostico(codigo_ciudad)
    dias = DeserializadorPronostico.desde_api(datos, codigo_ciudad)
    consultado_en = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return dias, consultado_en
