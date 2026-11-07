from dominio.pronostico import PronosticoDia
from servicios.clima_api import CIUDADES, describir_estado


class DeserializadorPronostico:
    @staticmethod
    def desde_api(datos, codigo_ciudad):
        if codigo_ciudad not in CIUDADES:
            raise ValueError("Seleccione una ciudad disponible.")
        if not isinstance(datos, dict) or not isinstance(datos.get("daily"), dict):
            raise ValueError("La API no entregó un pronóstico válido.")
        unidades = datos.get("daily_units")
        if not isinstance(unidades, dict) or (
            unidades.get("temperature_2m_min") != "°C"
            or unidades.get("temperature_2m_max") != "°C"
            or unidades.get("precipitation_probability_max") != "%"
            or unidades.get("precipitation_sum") != "mm"
            or unidades.get("wind_speed_10m_max") != "km/h"
        ):
            raise ValueError("Las unidades del pronóstico no corresponden a las solicitadas.")
        diario = datos["daily"]
        claves = (
            "time", "temperature_2m_min", "temperature_2m_max",
            "precipitation_probability_max", "precipitation_sum",
            "wind_speed_10m_max", "weather_code",
        )
        if any(not isinstance(diario.get(clave), list) or len(diario[clave]) < 3 for clave in claves):
            raise ValueError("El pronóstico no contiene tres días completos.")
        nombre_ciudad = CIUDADES[codigo_ciudad][0]
        dias = []
        for i in range(3):
            codigo = diario["weather_code"][i]
            dias.append(PronosticoDia(
                ciudad=nombre_ciudad,
                fecha=diario["time"][i],
                minima=diario["temperature_2m_min"][i],
                maxima=diario["temperature_2m_max"][i],
                probabilidad_lluvia=diario["precipitation_probability_max"][i],
                precipitacion_mm=diario["precipitation_sum"][i],
                viento_max_kmh=diario["wind_speed_10m_max"][i],
                codigo_clima=codigo,
                estado=describir_estado(codigo) if type(codigo) is int else "",
            ))
        if len({dia.fecha for dia in dias}) != len(dias) or any(dias[i].fecha >= dias[i+1].fecha for i in range(2)):
            raise ValueError("Las fechas del pronóstico no son válidas.")
        return dias
