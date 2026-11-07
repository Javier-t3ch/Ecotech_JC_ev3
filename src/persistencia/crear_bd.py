from persistencia.conexion import abrir_conexion, obtener_motor
from dominio.cargo import CARGOS


def _tablas_sqlite():
    return [
        """CREATE TABLE IF NOT EXISTS empleado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            direccion TEXT NOT NULL,
            numero TEXT NOT NULL,
            correo TEXT NOT NULL,
            fecha_contrato TEXT NOT NULL,
            salario REAL NOT NULL,
            id_cargo INTEGER NOT NULL,
            FOREIGN KEY (id_cargo) REFERENCES cargo(id)
        )""",
        """CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            empleado_id INTEGER NOT NULL UNIQUE,
            rol TEXT NOT NULL DEFAULT 'empleado'
                CHECK (rol IN ('admin', 'empleado')),
            FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE RESTRICT
        )""",
        """CREATE TABLE IF NOT EXISTS departamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL,
            id_gerente INTEGER
        )""",
        """CREATE TABLE IF NOT EXISTS proyecto (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL,
            fecha_inicio TEXT NOT NULL, descripcion TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS registro_tiempo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            horas_trabajadas INTEGER NOT NULL CHECK (horas_trabajadas > 0),
            fecha_trabajada TEXT NOT NULL, descripcion_tarea TEXT NOT NULL,
            empleado_id INTEGER NOT NULL, proyecto_id INTEGER NOT NULL,
            FOREIGN KEY (empleado_id) REFERENCES empleado(id),
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
        )""",
        """CREATE TABLE IF NOT EXISTS departamento_empleado (
            departamento_id INTEGER NOT NULL, empleado_id INTEGER NOT NULL,
            PRIMARY KEY (departamento_id, empleado_id),
            FOREIGN KEY (departamento_id) REFERENCES departamento(id),
            FOREIGN KEY (empleado_id) REFERENCES empleado(id)
        )""",
        """CREATE TABLE IF NOT EXISTS departamento_proyecto (
            departamento_id INTEGER NOT NULL, proyecto_id INTEGER NOT NULL,
            PRIMARY KEY (departamento_id, proyecto_id),
            FOREIGN KEY (departamento_id) REFERENCES departamento(id),
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
        )""",
        """CREATE TABLE IF NOT EXISTS indicador_api (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fuente TEXT NOT NULL,
            codigo TEXT NOT NULL,
            fecha TEXT NOT NULL,
            valor REAL NOT NULL CHECK (valor > 0),
            unidad TEXT NOT NULL,
            verificado_en TEXT NOT NULL,
            UNIQUE (fuente, codigo, fecha)
        )""",
        """CREATE TABLE IF NOT EXISTS clima_api (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fuente TEXT NOT NULL,
            ciudad TEXT NOT NULL,
            fecha_hora TEXT NOT NULL,
            temperatura REAL NOT NULL,
            humedad REAL NOT NULL CHECK (humedad BETWEEN 0 AND 100),
            codigo_clima INTEGER NOT NULL,
            estado TEXT NOT NULL,
            verificado_en TEXT NOT NULL,
            UNIQUE (fuente, ciudad, fecha_hora)
        )""",
        """CREATE TABLE IF NOT EXISTS proyecto_empleado (
            proyecto_id INTEGER NOT NULL, empleado_id INTEGER NOT NULL,
            PRIMARY KEY (proyecto_id, empleado_id),
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id),
            FOREIGN KEY (empleado_id) REFERENCES empleado(id)
        )""",
    ]


def _tablas_mysql():
    return [
        """CREATE TABLE IF NOT EXISTS empleado (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL, direccion VARCHAR(200) NOT NULL,
            numero VARCHAR(30) NOT NULL, correo VARCHAR(150) NOT NULL,
            fecha_contrato DATE NOT NULL, salario DECIMAL(12,2) NOT NULL,
            id_cargo INT NOT NULL,
            FOREIGN KEY (id_cargo) REFERENCES cargo(id)
        )""",
        """CREATE TABLE IF NOT EXISTS usuario (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre_usuario VARCHAR(40) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            empleado_id INT NOT NULL UNIQUE,
            rol VARCHAR(10) NOT NULL DEFAULT 'empleado',
            CONSTRAINT ck_usuario_rol CHECK (rol IN ('admin', 'empleado')),
            FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE RESTRICT
        )""",
        """CREATE TABLE IF NOT EXISTS departamento (
            id INT PRIMARY KEY AUTO_INCREMENT, nombre VARCHAR(100) NOT NULL,
            id_gerente INT
        )""",
        """CREATE TABLE IF NOT EXISTS proyecto (
            id INT PRIMARY KEY AUTO_INCREMENT, nombre VARCHAR(100) NOT NULL,
            fecha_inicio DATE NOT NULL, descripcion TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS registro_tiempo (
            id INT PRIMARY KEY AUTO_INCREMENT, horas_trabajadas INT NOT NULL,
            fecha_trabajada DATE NOT NULL, descripcion_tarea TEXT NOT NULL,
            empleado_id INT NOT NULL, proyecto_id INT NOT NULL,
            FOREIGN KEY (empleado_id) REFERENCES empleado(id),
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
        )""",
        """CREATE TABLE IF NOT EXISTS departamento_empleado (
            departamento_id INT NOT NULL, empleado_id INT NOT NULL,
            PRIMARY KEY (departamento_id, empleado_id),
            FOREIGN KEY (departamento_id) REFERENCES departamento(id),
            FOREIGN KEY (empleado_id) REFERENCES empleado(id)
        )""",
        """CREATE TABLE IF NOT EXISTS departamento_proyecto (
            departamento_id INT NOT NULL, proyecto_id INT NOT NULL,
            PRIMARY KEY (departamento_id, proyecto_id),
            FOREIGN KEY (departamento_id) REFERENCES departamento(id),
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
        )""",
        """CREATE TABLE IF NOT EXISTS indicador_api (
            id INT PRIMARY KEY AUTO_INCREMENT,
            fuente VARCHAR(100) NOT NULL,
            codigo VARCHAR(30) NOT NULL,
            fecha DATE NOT NULL,
            valor DECIMAL(15,5) NOT NULL,
            unidad VARCHAR(30) NOT NULL,
            verificado_en VARCHAR(40) NOT NULL,
            UNIQUE KEY uq_indicador_observacion (fuente, codigo, fecha),
            CONSTRAINT ck_indicador_valor CHECK (valor > 0)
        )""",
        """CREATE TABLE IF NOT EXISTS clima_api (
            id INT PRIMARY KEY AUTO_INCREMENT,
            fuente VARCHAR(100) NOT NULL,
            ciudad VARCHAR(100) NOT NULL,
            fecha_hora VARCHAR(32) NOT NULL,
            temperatura DOUBLE NOT NULL,
            humedad DOUBLE NOT NULL,
            codigo_clima INT NOT NULL,
            estado VARCHAR(100) NOT NULL,
            verificado_en VARCHAR(40) NOT NULL,
            UNIQUE KEY uq_clima_observacion (fuente, ciudad, fecha_hora),
            CONSTRAINT ck_clima_humedad CHECK (humedad BETWEEN 0 AND 100)
        )""",
        """CREATE TABLE IF NOT EXISTS proyecto_empleado (
            proyecto_id INT NOT NULL, empleado_id INT NOT NULL,
            PRIMARY KEY (proyecto_id, empleado_id),
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id),
            FOREIGN KEY (empleado_id) REFERENCES empleado(id)
        )""",
    ]


def _migrar_empleado_sqlite(cursor):
    cursor.execute("PRAGMA table_info(empleado)")
    columnas = {fila[1] for fila in cursor.fetchall()}
    if not columnas or "id_cargo" in columnas:
        return
    if "cargo" not in columnas:
        raise ValueError("La tabla empleado tiene un esquema desconocido.")
    cursor.execute("""CREATE TABLE empleado_migracion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL, direccion TEXT NOT NULL,
        numero TEXT NOT NULL, correo TEXT NOT NULL,
        fecha_contrato TEXT NOT NULL, salario REAL NOT NULL,
        id_cargo INTEGER NOT NULL,
        FOREIGN KEY (id_cargo) REFERENCES cargo(id)
    )""")
    cursor.execute("""INSERT INTO empleado_migracion
        (id, nombre, direccion, numero, correo, fecha_contrato, salario, id_cargo)
        SELECT id, nombre, direccion, numero, correo, fecha_contrato, salario,
        CASE WHEN LOWER(TRIM(cargo)) LIKE '%recursos humanos%'
                OR LOWER(TRIM(cargo)) LIKE '%reclutad%' THEN 2
            ELSE 1 END
        FROM empleado""")
    cursor.execute("DROP TABLE empleado")
    cursor.execute("ALTER TABLE empleado_migracion RENAME TO empleado")


def _migrar_empleado_mysql(cursor):
    cursor.execute("""SELECT COLUMN_NAME FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'empleado'""")
    columnas = {fila[0] for fila in cursor.fetchall()}
    if "cargo" not in columnas:
        return
    if "id_cargo" not in columnas:
        cursor.execute("ALTER TABLE empleado ADD COLUMN id_cargo INT NULL")
    cursor.execute("""UPDATE empleado SET id_cargo = CASE
        WHEN LOWER(TRIM(cargo)) LIKE '%recursos humanos%'
        OR LOWER(TRIM(cargo)) LIKE '%reclutad%' THEN 2 ELSE 1 END
        WHERE id_cargo IS NULL""")
    cursor.execute("ALTER TABLE empleado MODIFY COLUMN id_cargo INT NOT NULL")
    cursor.execute("""SELECT COUNT(*) FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'empleado'
        AND COLUMN_NAME = 'id_cargo' AND REFERENCED_TABLE_NAME = 'cargo'""")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""ALTER TABLE empleado ADD CONSTRAINT fk_empleado_cargo
            FOREIGN KEY (id_cargo) REFERENCES cargo(id)""")
    cursor.execute("ALTER TABLE empleado DROP COLUMN cargo")


def _migrar_usuario_sqlite(cursor):
    """Conserva usuarios y hashes existentes; agrega el rol por defecto."""
    cursor.execute("PRAGMA table_info(usuario)")
    columnas = {fila[1] for fila in cursor.fetchall()}
    if columnas and "rol" not in columnas:
        cursor.execute("""ALTER TABLE usuario ADD COLUMN rol TEXT NOT NULL
            DEFAULT 'empleado' CHECK (rol IN ('admin', 'empleado'))""")


def _migrar_usuario_mysql(cursor):
    cursor.execute("""SELECT COLUMN_NAME FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'usuario'
        AND COLUMN_NAME = 'rol'""")
    if cursor.fetchone() is None:
        cursor.execute("""ALTER TABLE usuario ADD COLUMN rol VARCHAR(10)
            NOT NULL DEFAULT 'empleado'""")
        cursor.execute("""ALTER TABLE usuario ADD CONSTRAINT ck_usuario_rol
            CHECK (rol IN ('admin', 'empleado'))""")


def crear_tablas():
    conexion = abrir_conexion()
    motor = obtener_motor()
    try:
        cursor = conexion.cursor()
        if motor == "sqlite":
            cursor.execute("PRAGMA foreign_keys = OFF")
            cursor.execute("""CREATE TABLE IF NOT EXISTS cargo (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL UNIQUE
            )""")
            for id_cargo, nombre in CARGOS.items():
                cursor.execute("INSERT OR IGNORE INTO cargo (id, nombre) VALUES (?, ?)",
                            (id_cargo, nombre))
            _migrar_empleado_sqlite(cursor)
            for sql in _tablas_sqlite():
                cursor.execute(sql)
            _migrar_usuario_sqlite(cursor)
            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_empleado_correo ON empleado(correo)")
            errores = cursor.execute("PRAGMA foreign_key_check").fetchall()
            if errores:
                raise ValueError("Se encontraron relaciones inválidas durante la migración.")
        else:
            cursor.execute("""CREATE TABLE IF NOT EXISTS cargo (
                id INT PRIMARY KEY, nombre VARCHAR(70) NOT NULL UNIQUE
            )""")
            for id_cargo, nombre in CARGOS.items():
                cursor.execute("""INSERT INTO cargo (id, nombre) VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE nombre = VALUES(nombre)""", (id_cargo, nombre))
            cursor.execute(_tablas_mysql()[0])
            _migrar_empleado_mysql(cursor)
            for sql in _tablas_mysql()[1:]:
                cursor.execute(sql)
            _migrar_usuario_mysql(cursor)
            cursor.execute("""SELECT COUNT(*) FROM information_schema.STATISTICS
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'empleado'
                AND COLUMN_NAME = 'correo' AND NON_UNIQUE = 0""")
            if cursor.fetchone()[0] == 0:
                cursor.execute("CREATE UNIQUE INDEX uq_empleado_correo ON empleado(correo)")
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        if motor == "sqlite":
            conexion.execute("PRAGMA foreign_keys = ON")
        conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print("Tablas de EcoTech preparadas correctamente.")
