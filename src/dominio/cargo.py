
CARGO_EMPLEADO = 1
CARGO_RECURSOS_HUMANOS = 2

CARGOS = {
    CARGO_EMPLEADO: "Empleado",
    CARGO_RECURSOS_HUMANOS: "Recursos Humanos",
}


def validar_id_cargo(id_cargo):
    if type(id_cargo) is not int or id_cargo not in CARGOS:
        raise ValueError("Seleccione un ID de cargo válido (1 o 2).")
    return id_cargo


def nombre_cargo(id_cargo):
    return CARGOS.get(id_cargo, "Desconocido")
