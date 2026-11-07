import requests

URL_CLIMA = "https://api.open-meteo.com/v1/forecast"

CIUDADES = {
    "1": ("La Serena", -29.9045, -71.2489),
    "2": ("Santiago", -33.4489, -70.6693),
    "3": ("Valparaíso", -33.0472, -71.6127),
    "4": ("Concepción", -36.8201, -73.0444),
    "5": ("Temuco", -38.7359, -72.5904),
}


def obtener_clima(codigo_ciudad):
    if codigo_ciudad not in CIUDADES:
        raise ValueError("Seleccione una ciudad disponible.")
    _, latitud, longitud = CIUDADES[codigo_ciudad]
    respuesta = requests.get(
        URL_CLIMA,
        params={
            "latitude": latitud,
            "longitude": longitud,
            "current": "temperature_2m,relative_humidity_2m,weather_code",
            "timezone": "America/Santiago",
            "forecast_days": 1,
        },
        timeout=(3, 5),
    )
    respuesta.raise_for_status()
    return respuesta.json()


def describir_estado(codigo):
    if codigo == 0:
        return "Despejado"
    if codigo in (1, 2, 3):
        return "Parcialmente nublado o cubierto"
    if codigo in (45, 48):
        return "Niebla"
    if codigo in (51, 53, 55, 56, 57):
        return "Llovizna"
    if codigo in (61, 63, 65, 66, 67):
        return "Lluvia"
    if codigo in (71, 73, 75, 77):
        return "Nieve"
    if codigo in (80, 81, 82):
        return "Chubascos"
    if codigo in (85, 86):
        return "Chubascos de nieve"
    if codigo in (95, 96, 99):
        return "Tormenta"
    return f"Condición meteorológica código {codigo}"


def obtener_pronostico(codigo_ciudad):
    if codigo_ciudad not in CIUDADES:
        raise ValueError("Seleccione una ciudad disponible.")
    _, latitud, longitud = CIUDADES[codigo_ciudad]
    respuesta = requests.get(
        URL_CLIMA,
        params={
            "latitude": latitud,
            "longitude": longitud,
            "daily": (
                "temperature_2m_min,temperature_2m_max,"
                "precipitation_probability_max,precipitation_sum,"
                "wind_speed_10m_max,weather_code"
            ),
            "timezone": "America/Santiago",
            "forecast_days": 3,
        },
        timeout=(3, 5),
    )
    respuesta.raise_for_status()
    return respuesta.json()
