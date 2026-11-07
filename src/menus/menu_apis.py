import requests

from complementos.complementos import limpiar_pantalla
from menus.menu_indicadores import mostrar_consulta, mostrar_historial
from validaciones import (
    FormularioCancelado, avisar_cancelacion, aviso_cancelacion, pedir_dato,
)
from servicios.autorizacion import exigir_sesion
from servicios.clima import consultar_clima, historial_clima
from servicios.clima_api import CIUDADES
from servicios.pagos_internacionales import estimar_pago, validar_monto_clp
from servicios.pronostico_clima import consultar_pronostico


def _elegir_ciudad():
    print("\nCiudades disponibles:")
    for codigo, (nombre, _, _) in CIUDADES.items():
        print(f"{codigo}. {nombre}")

    def validar(valor):
        valor = valor.strip()
        if valor == "0" or valor in CIUDADES:
            return valor
        raise ValueError("Seleccione una ciudad de la lista o 0 para volver.")

    return pedir_dato("Ciudad (0 para volver): ", validar)


def _consultar_clima(sesion):
    print("\n===== CONSULTAR CLIMA ACTUAL =====")
    aviso_cancelacion()
    try:
        codigo = _elegir_ciudad()
        if codigo == "0":
            return
        clima, origen, mensaje = consultar_clima(sesion, codigo)
        limpiar_pantalla()
        print("\n===== RESULTADO DE LA CONSULTA =====")
        print(mensaje)
        if clima is None:
            return
        print(f"Ciudad: {clima.ciudad} | Fuente: {clima.fuente} | Origen: {origen}")
        print(f"Fecha y hora del dato: {clima.fecha_hora}")
        print(f"Temperatura: {clima.temperatura:.1f} °C")
        print(f"Humedad relativa: {clima.humedad:.0f} %")
        print(f"Estado del tiempo: {clima.estado}")
        print(f"Última verificación: {clima.verificado_en}")
    except FormularioCancelado:
        avisar_cancelacion()
    except PermissionError as error:
        print(error)
    except Exception:
        print("No se pudo consultar el clima. Inténtelo nuevamente.")


def _historial_clima(sesion):
    print("\n===== HISTORIAL DEL CLIMA  =====")
    aviso_cancelacion()
    try:
        codigo = _elegir_ciudad()
        if codigo == "0":
            return
        resultados = historial_clima(sesion, codigo)
        limpiar_pantalla()
        print("\n===== HISTORIAL DEL CLIMA  =====")
        if not resultados:
            print("Todavía no existen observaciones guardadas para esa ciudad.")
            return
        for clima in resultados:
            print(f"{clima.fecha_hora} | {clima.ciudad} | {clima.temperatura:.1f} °C | "
                f"{clima.humedad:.0f} % | {clima.estado}")
        print("Origen: BD local (sin consultar la API).")
    except FormularioCancelado:
        avisar_cancelacion()
    except PermissionError as error:
        print(error)
    except Exception:
        print("No se pudo recuperar el historial local del clima.")


def _estimar_pago_internacional(sesion):
    print("\n===== ESTIMAR MONTO INTERNACIONAL (CLP A USD) =====")
    print("Esta función calcula un equivalente de referencia: NO realiza pagos ni modifica salarios.")
    aviso_cancelacion()
    try:
        monto = pedir_dato("Monto en pesos chilenos (CLP): ", validar_monto_clp)
        estimacion, mensaje = estimar_pago(sesion, monto)
        limpiar_pantalla()
        print("\n===== ESTIMACIÓN CLP A USD =====")
        print(mensaje)
        if estimacion is None:
            return
        print(f"Monto en pesos: {estimacion['monto_clp']:.2f} CLP")
        print(f"Dólar de referencia: {estimacion['tasa_clp_usd']:.2f} CLP por USD")
        print(f"Equivalente estimado: {estimacion['monto_usd']:.2f} USD")
        print(f"Fecha del indicador: {estimacion['fecha']}")
        print(f"Fuente: {estimacion['fuente']} | Origen: {estimacion['origen']}")
        print("No incluye comisiones, impuestos ni el tipo de cambio efectivo del banco.")
        if estimacion["origen"] != "API":
            print("ATENCIÓN: calculado con un dato local de respaldo, posiblemente desactualizado.")
    except FormularioCancelado:
        avisar_cancelacion()
    except PermissionError as error:
        print(error)
    except ValueError as error:
        print(f"No fue posible calcular el equivalente: {error}")
    except Exception:
        print("No se pudo completar la estimación. Inténtelo nuevamente.")


def _planificacion_climatica(sesion):
    print("\n===== PLANIFICACIÓN CLIMÁTICA (PRÓXIMOS 3 DÍAS) =====")
    print("Pronóstico orientativo para actividades de proyectos al aire libre.")
    aviso_cancelacion()
    try:
        codigo = _elegir_ciudad()
        if codigo == "0":
            return
        dias, consultado_en = consultar_pronostico(sesion, codigo)
        limpiar_pantalla()
        print(f"\n===== PRONÓSTICO DE {dias[0].ciudad.upper()} =====")
        print(f"Fuente: Open-Meteo | Consulta UTC: {consultado_en}")
        for dia in dias:
            print(f"\nFecha: {dia.fecha} | Estado: {dia.estado}")
            print(f"Temperatura: {dia.minima:.1f} a {dia.maxima:.1f} °C")
            print(f"Prob. precipitación: {dia.probabilidad_lluvia:.0f}% | "
                f"Precipitación: {dia.precipitacion_mm:.1f} mm")
            print(f"Viento máximo previsto: {dia.viento_max_kmh:.1f} km/h")
            print(f"Orientación: {dia.orientacion()}")

    except FormularioCancelado:
        avisar_cancelacion()
    except PermissionError as error:
        print(error)
    except requests.exceptions.RequestException:
        print("No se pudo consultar el pronóstico. Revisa la conexión y vuelve a intentar.")
        print("El historial del clima contiene observaciones pasadas, no un pronóstico de respaldo.")
    except (ValueError, KeyError, TypeError):
        print("La respuesta del pronóstico no contiene los datos esperados.")
    except Exception:
        print("No se pudo consultar el pronóstico.")


def menu_apis(sesion):
    try:
        exigir_sesion(sesion)
    except PermissionError as error:
        print(error)
        return
    while True:
        limpiar_pantalla()
        print("\n===== SERVICIOS EXTERNOS (APIs) =====")
        print("1. Consultar dólar observado")
        print("2. Historial del dólar ")
        print("3. Consultar clima actual")
        print("4. Historial del clima actual ")
        print("5. Estimar monto internacional (CLP a USD)")
        print("6. Planificación climática (pronóstico 3 días)")
        print("0. Volver al menú privado")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "0":
            return
        limpiar_pantalla()
        if opcion == "1":
            mostrar_consulta(sesion)
        elif opcion == "2":
            mostrar_historial(sesion)
        elif opcion == "3":
            _consultar_clima(sesion)
        elif opcion == "4":
            _historial_clima(sesion)
        elif opcion == "5":
            _estimar_pago_internacional(sesion)
        elif opcion == "6":
            _planificacion_climatica(sesion)
        else:
            print("Opción no válida.")
        input("\nPresione Enter para continuar...")
