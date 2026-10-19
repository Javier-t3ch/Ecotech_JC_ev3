class Empleado:

    def __init__(self, nombre, direccion, numero, correo, fecha_contrato, salario, cargo, id=None ):
        if nombre == "":
            raise ValueError("El nombre no puede estar vacio")

        if direccion == "":
            raise ValueError("La direccion no puede estar vacia")

        if numero == "":
            raise ValueError("El numero telefonico no puede estar vacio")

        if "@" not in correo or "." not in correo:
            raise ValueError("El correo no es valido")

        if salario < 0:
            raise ValueError("El salario no puede ser negativo")

        if cargo == "":
            raise ValueError("El cargo no puede estar vacio")

        self._id = id
        self._nombre = nombre
        self._direccion = direccion
        self._numero = numero
        self._correo = correo
        self._fecha_contrato = fecha_contrato
        self._salario = salario
        self._cargo = cargo
        self._registros_tiempo = []

    def mostrar_datos(self):
        return f"{self._id} - {self._nombre} - {self._cargo} - {self._correo} - {self._direccion}"

    def ver_salario(self):
        return self._salario

    def registrar_horas(self, registro):
        if registro._empleado != self:
            raise ValueError("El registro pertenece a otro empleado")
        if registro._horas_trabajadas <= 0:
            raise ValueError("Las horas deben ser mayores que cero")
        if registro in self._registros_tiempo:
            raise ValueError("Este registro ya fue agregado")
        self._registros_tiempo.append(registro)
        total_horas = 0
        for registro_guardado in self._registros_tiempo:
            total_horas += registro_guardado._horas_trabajadas
        return total_horas

