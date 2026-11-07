from dominio.clima import Clima
from servicios.clima_api import CIUDADES, describir_estado


class DeserializadorClima:
    @staticmethod
    def desde_api(datos, codigo_ciudad):
        if codigo_ciudad not in CIUDADES:
            raise ValueError("La ciudad no está disponible.")
        if not isinstance(datos, dict) or not isinstance(datos.get("current"), dict):
            raise ValueError("La respuesta no contiene datos meteorológicos válidos.")
        unidades = datos.get("current_units")
        if unidades is not None:
            if not isinstance(unidades, dict) or unidades.get("temperature_2m") != "°C" \
                    or unidades.get("relative_humidity_2m") != "%":
                raise ValueError("Las unidades de la respuesta climática no son válidas.")
        actual = datos["current"]
        codigo = actual.get("weather_code")
        if type(codigo) is not int:
            raise ValueError("El código meteorológico no es válido.")
        return Clima(
            ciudad=CIUDADES[codigo_ciudad][0],
            fecha_hora=actual.get("time"),
            temperatura=actual.get("temperature_2m"),
            humedad=actual.get("relative_humidity_2m"),
            codigo_clima=codigo,
            estado=describir_estado(codigo),
        )
