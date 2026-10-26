import requests
import math
import requests
from menu_usuario import solicitar_login, menu_privado


"""""
URL_DOLAR = "https://mindicador.cl/api/dolar"


def obtener_datos():
    """Solicita el indicador y devuelve el JSON convertido a datos de Python."""
    respuesta = requests.get(URL_DOLAR, timeout=(3, 5))
    print(f"Estado HTTP: {respuesta.status_code}")
    respuesta.raise_for_status()
    return respuesta.json()


def extraer_primero(datos):
    """Valida la respuesta y devuelve la fecha y el valor del primer registro."""
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
    """Valida y presenta la información, sin consultar la red ni guardar datos."""
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
            datos = obtener_datos()
            mostrar_indicador(datos, "mindicador.cl (consulta real)")
        elif opcion == "2":
            datos = {"codigo": "dolar", "unidad_medida": "Pesos", "serie": []}
            mostrar_indicador(datos, "datos simulados")
        elif opcion == "3":
            datos = {
                "codigo": "dolar",
                "unidad_medida": "Pesos",
                "serie": [{"fecha": "2026-01-02T00:00:00Z", "valor": 900.0}],
            }
            mostrar_indicador(datos, "datos simulados (valor ficticio)")
        else:
            print("Elige una opción entre 1 y 3.")

    except requests.exceptions.RequestException:
        print("No pudimos consultar el servicio. Revisa tu conexión e inténtalo otra vez.")
    except (ValueError, KeyError, TypeError) as error:
        print(f"No se pudo usar el indicador: {error}")


if __name__ == "__main__":
    main()
""""

def main():
    while True:
        usuario_actual = solicitar_login()
        if usuario_actual is None:
            if input("Enter para reintentar o 0 para salir: ") == "0":
                return
            continue
        opcion = menu_privado(usuario_actual)
        usuario_actual = None # Terminar el acceso de esta sesión.
        if opcion == "0":
            return
        print("Sesión cerrada. Ingrese nuevamente.")
if __name__ == "__main__":
    main()