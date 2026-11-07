import math
from datetime import datetime, date, timezone


class Indicador:
    def __init__(self, fecha, valor, verificado_en=None, fuente="mindicador.cl"):
        if isinstance(fecha, datetime):
            fecha = fecha.date()
        elif isinstance(fecha, str):
            try:
                fecha = datetime.fromisoformat(fecha.strip().replace("Z", "+00:00")).date()
            except ValueError as error:
                raise ValueError("La fecha del indicador no es válida.") from error
        if not isinstance(fecha, date):
            raise ValueError("La fecha del indicador no es válida.")
        if type(valor) not in (int, float) or not math.isfinite(valor) or valor <= 0:
            raise ValueError("El valor del indicador debe ser positivo y finito.")
        if not isinstance(fuente, str) or not fuente.strip():
            raise ValueError("La fuente del indicador es obligatoria.")
        if verificado_en is None:
            verificado_en = datetime.now(timezone.utc).isoformat(timespec="seconds")
        elif not isinstance(verificado_en, str):
            raise ValueError("La fecha de verificación no es válida.")
        else:
            try:
                datetime.fromisoformat(verificado_en.replace("Z", "+00:00"))
            except ValueError as error:
                raise ValueError("La fecha de verificación no es válida.") from error
        self.fecha = fecha.isoformat()
        self.valor = float(valor)
        self.fuente = fuente.strip()
        self.codigo = "dolar"
        self.unidad = "CLP/USD"
        self.verificado_en = verificado_en
