from dominio.indicador import Indicador
from servicios.indicadores_api import extraer_primero


class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos):
        fecha, valor = extraer_primero(datos)
        return Indicador(fecha=fecha, valor=valor)
