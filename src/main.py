from dominio.Gestion_departamento import GestionDepartamento
from dominio.gestionPermisos import GestionPermisos
from persistencia.crear_bd import crear_tablas
from persistencia.semilla_db import ejecutar_semilla
from persistencia.semilla_admin import preparar_admin
from menus.menu_usuario import solicitar_login, menu_privado
from menus.menu_dominio_empleado import menu_dominio_empleado
from menus.menu_dominio_departamento import menu_dominio_departamento
from menus.menu_dominio_proyecto import menu_dominio_proyecto
from menus.menu_dominio_registroTiempo import menu_dominio_registro_tiempo
from menus.menu_dominio_usuario import menu_dominio_usuario
from menus.menu_dominio_gestionPermisos import menu_dominio_gestionPermisos
from menus.menu_dominio_gestionDepartamento import menu_dominio_gestionDepartamento
from complementos.complementos import limpiar_pantalla


def menu_modulos():
    gestion_permisos = GestionPermisos()
    gestion_departamentos = GestionDepartamento()
    while True:
        limpiar_pantalla()
        print("\n===== MÓDULOS ECOTECH =====")
        print("1. Empleado")
        print("2. Departamento")
        print("3. Proyecto")
        print("4. Registro de Tiempo")
        print("5. Usuario (cuentas reales)")
        print("6. Gestión de Permisos (demostración)")
        print("7. Gestión de Departamento (demostración)")
        print("0. Volver al menú privado")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            menu_dominio_empleado()
        elif opcion == "2":
            menu_dominio_departamento()
        elif opcion == "3":
            menu_dominio_proyecto()
        elif opcion == "4":
            menu_dominio_registro_tiempo()
        elif opcion == "5":
            menu_dominio_usuario()
        elif opcion == "6":
            menu_dominio_gestionPermisos(gestion_permisos)
        elif opcion == "7":
            menu_dominio_gestionDepartamento(gestion_departamentos)
        elif opcion == "0":
            return
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")


def main():
    while True:
        usuario_actual = solicitar_login()
        if usuario_actual is None:
            if input("Enter para reintentar o 0 para salir: ").strip() == "0":
                return
            continue
        opcion = menu_privado(usuario_actual, menu_modulos=menu_modulos)
        usuario_actual = None
        if opcion == "0":
            return
        print("Sesión cerrada. Ingrese nuevamente.")


if __name__ == "__main__":
    try:
        crear_tablas()
        ejecutar_semilla()
        preparar_admin()
    except Exception:
        print("No fue posible preparar la base de datos y el acceso inicial.")
    else:
        main()
