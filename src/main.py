from dominio.Gestion_departamento import GestionDepartamento
from dominio.gestionPermisos import GestionPermisos
from persistencia.crear_bd import crear_tablas
from menus.menu_dominio_empleado import menu_dominio_empleado
from menus.menu_dominio_departamento import menu_dominio_departamento
from menus.menu_dominio_proyecto import menu_dominio_proyecto
from menus.menu_dominio_registroTiempo import menu_dominio_registro_tiempo
from menus.menu_dominio_usuario import menu_dominio_usuario
from menus.menu_dominio_gestionPermisos import menu_dominio_gestionPermisos
from menus.menu_dominio_gestionDepartamento import menu_dominio_gestionDepartamento
from complementos.complementos import limpiar_pantalla

def main():
    usuarios = []
    gestion_permisos = GestionPermisos()
    gestion_departamentos = GestionDepartamento()

    while True:
        limpiar_pantalla()
        print("\n===== ECOTECH SOLUTIONS =====")
        print("1. Empleado")
        print("2. Departamento")
        print("3. Proyecto")
        print("4. Registro de Tiempo")
        print("5. Usuario (demostracion)")
        print("6. Gestion de Permisos (demostracion)")
        print("7. Gestion de Departamento (demostracion)")
        print("0. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            limpiar_pantalla()
            menu_dominio_empleado()
        elif opcion == "2":
            limpiar_pantalla()
            menu_dominio_departamento()
        elif opcion == "3":
            limpiar_pantalla()
            menu_dominio_proyecto()
        elif opcion == "4":
            limpiar_pantalla()
            menu_dominio_registro_tiempo()
        elif opcion == "5":
            limpiar_pantalla()
            menu_dominio_usuario(usuarios)
        elif opcion == "6":
            limpiar_pantalla()
            menu_dominio_gestionPermisos(usuarios, gestion_permisos)
        elif opcion == "7":
            limpiar_pantalla()
            menu_dominio_gestionDepartamento(gestion_departamentos)
        elif opcion == "0":
            limpiar_pantalla()
            print("Hasta luego.")
            break
        else:
            print("Opcion no valida.")
            input("Presione Enter para continuar...")
            limpiar_pantalla()

if __name__ == "__main__":
    try:
        crear_tablas()
    except Exception as error:
        print("Error al preparar la base de datos:", error)
    else:
        main()
