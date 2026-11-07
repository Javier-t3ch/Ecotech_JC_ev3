from servicios.indicadores import consultar_indicador, obtener_historial


def mostrar_consulta(sesion):
    print("\n===== CONSULTAR DÓLAR OBSERVADO =====")
    try:
        indicador, origen, mensaje = consultar_indicador(sesion)
        print(mensaje)
        if indicador is None:
            return
        print(f"Origen: {origen} | Fuente: {indicador.fuente}")
        print(f"Fecha: {indicador.fecha} | Valor: {indicador.valor:.2f} {indicador.unidad}")
        print(f"Momento de verificación: {indicador.verificado_en}")
    except PermissionError as error:
        print(error)
    except Exception:
        print("No se pudo recuperar la información del dólar.")


def mostrar_historial(sesion):
    print("\n===== HISTORIAL DEL DÓLAR =====")
    try:
        historial = obtener_historial(sesion)
        if not historial:
            print("Aún no existen observaciones guardadas.")
        for dato in historial:
            print(f"{dato.fecha}: {dato.valor:.2f} {dato.unidad} | "
                f"{dato.fuente} | Verificado: {dato.verificado_en}")
        print("Origen: BD local (sin consultar la API).")
    except PermissionError as error:
        print(error)
    except Exception:
        print("No se pudo consultar el historial local.")
