import math
from datetime import datetime, timezone


class Clima:
    def __init__(self, ciudad, fecha_hora, temperatura, humedad, codigo_clima,
                 estado, verificado_en=None, fuente="open-meteo.com"):
        if not isinstance(ciudad, str) or not ciudad.strip():
            raise ValueError("La ciudad es obligatoria.")
        if not isinstance(fecha_hora, str):
            raise ValueError("La fecha y hora del clima no son válidas.")
        try:
            momento = datetime.fromisoformat(fecha_hora.strip().replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError("La fecha y hora del clima no son válidas.") from error
        if type(temperatura) not in (int, float) or not math.isfinite(temperatura):
            raise ValueError("La temperatura del clima no es válida.")
        if type(humedad) not in (int, float) or not math.isfinite(humedad) or not 0 <= humedad <= 100:
            raise ValueError("La humedad debe estar entre 0 y 100.")
        if type(codigo_clima) is not int or not 0 <= codigo_clima <= 99:
            raise ValueError("El código meteorológico no es válido.")
        if not isinstance(estado, str) or not estado.strip():
            raise ValueError("El estado del tiempo no es válido.")
        if not isinstance(fuente, str) or not fuente.strip():
            raise ValueError("La fuente del clima es obligatoria.")
        if verificado_en is None:
            verificado_en = datetime.now(timezone.utc).isoformat(timespec="seconds")
        else:
            if not isinstance(verificado_en, str):
                raise ValueError("La fecha de verificación no es válida.")
            try:
                datetime.fromisoformat(verificado_en.replace("Z", "+00:00"))
            except ValueError as error:
                raise ValueError("La fecha de verificación no es válida.") from error
        self.ciudad = ciudad.strip()
        self.fecha_hora = momento.isoformat(timespec="minutes")
        self.temperatura = float(temperatura)
        self.humedad = float(humedad)
        self.codigo_clima = codigo_clima
        self.estado = estado.strip()
        self.verificado_en = verificado_en
        self.fuente = fuente.strip()
