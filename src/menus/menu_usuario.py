
def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para ver el perfil.")
        return
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"Empleado: {usuario_actual['empleado_id']}")

def consultar_indicador(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para consultar indicadores.")
        return

    def menu_privado(usuario_actual):
        if usuario_actual is None:
            print("Debe iniciar sesión.")
        return "9"
    
    while True:
        print("1 Registrar, 2 Perfil, 3 Indicador, 9 Cerrar sesión, 0 Salir")
        opcion = input("Opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
        if opcion == "1":
            solicitar_registro()
        elif opcion == "2":
            mostrar_perfil(usuario_actual)
        elif opcion == "3":
            consultar_indicador(usuario_actual)
        else:
            print("Opción no válida.")