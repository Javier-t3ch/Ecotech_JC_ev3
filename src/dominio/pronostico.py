from datetime import date
import math


class PronosticoDia:
    def __init__(self, ciudad, fecha, minima, maxima, probabilidad_lluvia,
                precipitacion_mm, viento_max_kmh, codigo_clima, estado):
        if not isinstance(ciudad, str) or not ciudad.strip():
            raise ValueError("La ciudad no es válida.")
        if not isinstance(fecha, str):
            raise ValueError("La fecha del pronóstico no es válida.")
        try:
            fecha = date.fromisoformat(fecha)
        except ValueError as error:
            raise ValueError("La fecha del pronóstico no es válida.") from error
        numeros = (minima, maxima, probabilidad_lluvia, precipitacion_mm, viento_max_kmh)
        if any(type(n) not in (int, float) or not math.isfinite(n) for n in numeros):
            raise ValueError("El pronóstico contiene números inválidos.")
        if minima > maxima or not 0 <= probabilidad_lluvia <= 100 or precipitacion_mm < 0 or viento_max_kmh < 0:
            raise ValueError("El pronóstico tiene valores fuera del rango permitido.")
        if type(codigo_clima) is not int or codigo_clima < 0 or codigo_clima > 99:
            raise ValueError("El código meteorológico no es válido.")
        if not isinstance(estado, str) or not estado.strip():
            raise ValueError("El estado del tiempo no es válido.")
        self.ciudad = ciudad.strip()
        self.fecha = fecha.isoformat()
        self.minima = float(minima)
        self.maxima = float(maxima)
        self.probabilidad_lluvia = float(probabilidad_lluvia)
        self.precipitacion_mm = float(precipitacion_mm)
        self.viento_max_kmh = float(viento_max_kmh)
        self.codigo_clima = codigo_clima
        self.estado = estado.strip()

    def orientacion(self):
        if self.codigo_clima in (95, 96, 99) or self.probabilidad_lluvia >= 70 or self.precipitacion_mm >= 10:
            return "Riesgo meteorológico elevado: evaluar reprogramar trabajos exteriores."
        if self.viento_max_kmh >= 40 or self.probabilidad_lluvia >= 40 or self.precipitacion_mm >= 3:
            return "Precaución: revisar medidas y condiciones antes de trabajar al aire libre."
        return "Condiciones relativamente favorables; confirmar el pronóstico antes de trabajar."
