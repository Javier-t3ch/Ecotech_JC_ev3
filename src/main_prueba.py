import math
import requests

URL_DOLAR = "https://mindicador.cl/api/dolar"


def obtener_datos():
    respuesta = requests.get(URL_DOLAR, timeout=(3, 5))
    print(f"Estado HTTP: {respuesta.status_code}")
    respuesta.raise_for_status()
    return respuesta.json()


def extraer_primero(datos):
    if not isinstance(datos, dict):
        raise ValueError("La respuesta no es un objeto JSON.")
    if datos.get("codigo") != "dolar":
        raise ValueError("El indicador recibido no es el dólar.")
    if datos.get("unidad_medida") != "Pesos":
        raise ValueError("La unidad del indicador no es pesos.")
    serie = datos.get("serie")
    if not isinstance(serie, list) or not serie:
        raise ValueError("No hay valores disponibles en la serie.")
    registro = serie[0]
    if not isinstance(registro, dict):
        raise ValueError("El registro no tiene el formato esperado.")
    fecha = registro.get("fecha")
    valor = registro.get("valor")
    if not isinstance(fecha, str) or not fecha.strip():
        raise ValueError("Falta la fecha del indicador.")
    if type(valor) not in (int, float) or not math.isfinite(valor) or valor <= 0:
        raise ValueError("El valor del indicador no es válido.")
    return fecha, valor


def mostrar_indicador(datos, origen):
    fecha, valor = extraer_primero(datos)
    print(f"Código: {datos['codigo']}")
    print(f"Dólar observado: {valor:.2f} CLP por USD")
    print(f"Fecha del registro: {fecha}")
    print(f"Origen: {origen}")


def main():
    print("\n=== PRUEBA DE API: DÓLAR OBSERVADO ===")
    print("1. Consultar API real")
    print("2. Probar fallo: serie vacía (simulación)")
    print("3. Probar respuesta válida (simulación)")
    opcion = input("Elige una opción: ").strip()
    try:
        if opcion == "1":
            mostrar_indicador(obtener_datos(), "mindicador.cl (consulta real)")
        elif opcion == "2":
            mostrar_indicador({"codigo": "dolar", "unidad_medida": "Pesos", "serie": []}, "datos simulados")
        elif opcion == "3":
            mostrar_indicador({"codigo": "dolar", "unidad_medida": "Pesos", "serie": [{"fecha": "2026-01-02T00:00:00Z", "valor": 900.0}]}, "datos simulados (valor ficticio)")
        else:
            print("Elige una opción entre 1 y 3.")
    except requests.exceptions.RequestException:
        print("No pudimos consultar el servicio. Revisa tu conexión e inténtalo otra vez.")
    except (ValueError, KeyError, TypeError) as error:
        print(f"No se pudo usar el indicador: {error}")


if __name__ == "__main__":
    main()
