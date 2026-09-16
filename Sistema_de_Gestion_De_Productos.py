import sqlite3

from sqlite3 import Error

# Color opcional para mejorar legibilidad en terminal.
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class _ColorFallback:
        def __getattr__(self, _):
            return ""
    Fore = Style = _ColorFallback()

DB_NAME = "inventario.db"

def conectar_db():
    """Crea y retorna una conexión a SQLite."""
    try:
        return sqlite3.connect(DB_NAME)
    except Error as e:
        print(f"{Fore.RED}Error al conectar con la base de datos: {e}")
        return None

def crear_tabla():
    """Crea la tabla productos si no existe."""
    consulta = """
    CREATE TABLE IF NOT EXISTS productos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT NOT NULL,

        descripcion TEXT,

        cantidad INTEGER NOT NULL,

        precio REAL NOT NULL,

        categoria TEXT
    );
    """

    conexion = conectar_db()

    if conexion is None:
        return

    try:
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()

    except Error as e:
        print(f"{Fore.RED}Error al crear tabla: {e}")
    finally:
        conexion.close()

def pedir_texto_no_vacio(mensaje):
    """Solicita un texto y valida que no esté vacío."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print(f"{Fore.YELLOW}Error: este campo no puede estar vacío.")

def pedir_entero_no_negativo(mensaje):
    """Solicita un entero >= 0."""
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            return int(valor)
        
        print(f"{Fore.YELLOW}Error: ingrese un número entero válido.")

def pedir_flotante_positivo(mensaje):
    """Solicita un número flotante > 0."""
    while True:
        valor = input(mensaje).strip().replace(",", ".")
        try:
            numero = float(valor)
            if numero > 0:
                return numero
            print(f"{Fore.YELLOW}Error: el precio debe ser mayor a 0.")
        
        except ValueError:
            print(f"{Fore.YELLOW}Error: ingrese un número válido (ej: 1499.90).")

def pedir_id_producto():
    """Solicita un ID válido (> 0)."""
    while True:
        valor = input("Ingrese el ID del producto: ").strip()
        if valor.isdigit() and int(valor) > 0:
            return int(valor)
        print(f"{Fore.YELLOW}Error: el ID debe ser un entero mayor a 0.")

def registrar_producto():

    """Registra un nuevo producto en la base de datos."""

    print(f"\n{Fore.CYAN}--- REGISTRAR NUEVO PRODUCTO ---")



    nombre = pedir_texto_no_vacio("Nombre: ")

    descripcion = input("Descripción (opcional): ").strip()

    cantidad = pedir_entero_no_negativo("Cantidad disponible: ")

    precio = pedir_flotante_positivo("Precio: ")

    categoria = input("Categoría (opcional): ").strip()



    conexion = conectar_db()

    if conexion is None:

        return



    consulta = """

    INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)

    VALUES (?, ?, ?, ?, ?)

    """



    try:

        cursor = conexion.cursor()

        cursor.execute(consulta, (nombre, descripcion, cantidad, precio, categoria))

        conexion.commit()

        print(f"{Fore.GREEN}Producto registrado con éxito. ID asignado: {cursor.lastrowid}")

    except Error as e:

        print(f"{Fore.RED}Error al registrar producto: {e}")

    finally:

        conexion.close()





def listar_productos():

    """Muestra todos los productos registrados."""

    print(f"\n{Fore.CYAN}--- LISTADO DE PRODUCTOS ---")



    conexion = conectar_db()

    if conexion is None:

        return



    consulta = "SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos ORDER BY id"



    try:

        cursor = conexion.cursor()

        cursor.execute(consulta)

        productos = cursor.fetchall()



        if not productos:

            print(f"{Fore.YELLOW}No hay productos registrados.")

            return



        for producto in productos:

            print(

                f"ID: {producto[0]} | Nombre: {producto[1]} | Descripción: {producto[2] or '-'} "

                f"| Cantidad: {producto[3]} | Precio: ${producto[4]:.2f} | Categoría: {producto[5] or '-'}"

            )

    except Error as e:

        print(f"{Fore.RED}Error al listar productos: {e}")

    finally:

        conexion.close()





def buscar_producto_por_id():

    """Busca y muestra un producto por su ID."""

    print(f"\n{Fore.CYAN}--- BUSCAR PRODUCTO POR ID ---")

    producto_id = pedir_id_producto()



    conexion = conectar_db()

    if conexion is None:

        return



    consulta = "SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?"



    try:

        cursor = conexion.cursor()

        cursor.execute(consulta, (producto_id,))

        producto = cursor.fetchone()



        if producto:

            print(

                f"Encontrado -> ID: {producto[0]} | Nombre: {producto[1]} | Descripción: {producto[2] or '-'} "

                f"| Cantidad: {producto[3]} | Precio: ${producto[4]:.2f} | Categoría: {producto[5] or '-'}"

            )

        else:

            print(f"{Fore.YELLOW}No existe un producto con ese ID.")

    except Error as e:

        print(f"{Fore.RED}Error al buscar producto: {e}")

    finally:

        conexion.close()





def buscar_por_nombre_o_categoria():

    """Búsqueda opcional por nombre o categoría."""

    print(f"\n{Fore.CYAN}--- BÚSQUEDA POR NOMBRE O CATEGORÍA ---")

    termino = pedir_texto_no_vacio("Ingrese nombre o categoría a buscar: ").lower()



    conexion = conectar_db()

    if conexion is None:

        return



    consulta = """

    SELECT id, nombre, descripcion, cantidad, precio, categoria

    FROM productos

    WHERE LOWER(nombre) LIKE ? OR LOWER(categoria) LIKE ?

    ORDER BY id

    """



    try:

        cursor = conexion.cursor()

        patron = f"%{termino}%"

        cursor.execute(consulta, (patron, patron))

        resultados = cursor.fetchall()



        if not resultados:

            print(f"{Fore.YELLOW}No se encontraron coincidencias.")

            return



        for producto in resultados:

            print(

                f"ID: {producto[0]} | Nombre: {producto[1]} | Descripción: {producto[2] or '-'} "

                f"| Cantidad: {producto[3]} | Precio: ${producto[4]:.2f} | Categoría: {producto[5] or '-'}"

            )

    except Error as e:

        print(f"{Fore.RED}Error en la búsqueda: {e}")

    finally:

        conexion.close()





def actualizar_producto():

    """Actualiza los datos de un producto usando su ID."""

    print(f"\n{Fore.CYAN}--- ACTUALIZAR PRODUCTO ---")

    producto_id = pedir_id_producto()



    conexion = conectar_db()

    if conexion is None:

        return



    try:

        cursor = conexion.cursor()

        cursor.execute(

            "SELECT nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?",

            (producto_id,),

        )

        actual = cursor.fetchone()



        if not actual:

            print(f"{Fore.YELLOW}No existe un producto con ese ID.")

            return



        print("Deje en blanco un campo para conservar su valor actual.")

        nombre = input(f"Nombre [{actual[0]}]: ").strip() or actual[0]

        descripcion = input(f"Descripción [{actual[1] or '-'}]: ").strip() or actual[1]



        cantidad_input = input(f"Cantidad [{actual[2]}]: ").strip()

        if cantidad_input == "":

            cantidad = actual[2]

        elif cantidad_input.isdigit():

            cantidad = int(cantidad_input)

        else:

            print(f"{Fore.YELLOW}Cantidad inválida. Se conserva el valor anterior.")

            cantidad = actual[2]



        precio_input = input(f"Precio [{actual[3]}]: ").strip().replace(",", ".")

        if precio_input == "":

            precio = actual[3]

        else:

            try:

                precio = float(precio_input)

                if precio <= 0:

                    print(f"{Fore.YELLOW}Precio inválido. Se conserva el valor anterior.")

                    precio = actual[3]

            except ValueError:

                print(f"{Fore.YELLOW}Precio inválido. Se conserva el valor anterior.")

                precio = actual[3]



        categoria = input(f"Categoría [{actual[4] or '-'}]: ").strip() or actual[4]



        cursor.execute(

            """

            UPDATE productos

            SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?

            WHERE id = ?

            """,

            (nombre, descripcion, cantidad, precio, categoria, producto_id),

        )

        conexion.commit()

        print(f"{Fore.GREEN}Producto actualizado correctamente.")

    except Error as e:

        print(f"{Fore.RED}Error al actualizar producto: {e}")

    finally:

        conexion.close()





def eliminar_producto():

    """Elimina un producto por ID."""

    print(f"\n{Fore.CYAN}--- ELIMINAR PRODUCTO ---")

    producto_id = pedir_id_producto()



    conexion = conectar_db()

    if conexion is None:

        return



    try:

        cursor = conexion.cursor()

        cursor.execute("SELECT nombre FROM productos WHERE id = ?", (producto_id,))

        producto = cursor.fetchone()



        if not producto:

            print(f"{Fore.YELLOW}No existe un producto con ese ID.")

            return



        confirmar = input(f"¿Seguro que desea eliminar '{producto[0]}'? (s/n): ").strip().lower()

        if confirmar != "s":

            print(f"{Fore.YELLOW}Eliminación cancelada.")

            return



        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))

        conexion.commit()

        print(f"{Fore.GREEN}Producto eliminado correctamente.")

    except Error as e:

        print(f"{Fore.RED}Error al eliminar producto: {e}")

    finally:

        conexion.close()





def reporte_stock_bajo():

    """Muestra productos con cantidad igual o inferior al límite indicado."""

    print(f"\n{Fore.CYAN}--- REPORTE DE STOCK BAJO ---")

    limite = pedir_entero_no_negativo("Ingrese el límite de cantidad: ")



    conexion = conectar_db()

    if conexion is None:

        return



    consulta = """

    SELECT id, nombre, cantidad, precio, categoria

    FROM productos

    WHERE cantidad <= ?

    ORDER BY cantidad ASC, id ASC

    """



    try:

        cursor = conexion.cursor()

        cursor.execute(consulta, (limite,))

        productos = cursor.fetchall()



        if not productos:

            print(f"{Fore.GREEN}No hay productos con stock menor o igual a {limite}.")

            return



        print(f"{Fore.YELLOW}Productos con stock menor o igual a {limite}:")

        for producto in productos:
            print(
                f"ID: {producto[0]} | Nombre: {producto[1]} | Cantidad: {producto[2]} "
                f"| Precio: ${producto[3]:.2f} | Categoría: {producto[4] or '-'}"
            )

    except Error as e:
        print(f"{Fore.RED}Error al generar reporte: {e}")

    finally:
        conexion.close()

def mostrar_menu():
    """Imprime el menú principal."""
    print(f"\n{Style.BRIGHT}--- SISTEMA DE GESTIÓN DE INVENTARIO ---")
    print("1. Registrar nuevo producto")
    print("2. Visualizar productos")
    print("3. Actualizar producto por ID")
    print("4. Eliminar producto por ID")
    print("5. Buscar producto por ID")
    print("6. Buscar por nombre o categoría (opcional)")
    print("7. Reporte de stock bajo")
    print("8. Salir")

def main():
    """Punto de entrada de la aplicación en terminal."""
    crear_tabla()
    ejecutando = True

    while ejecutando:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-8): ").strip()

        match opcion:
            case "1":
                registrar_producto()
            case "2":
                listar_productos()
            case "3":
                actualizar_producto()
            case "4":
                eliminar_producto()
            case "5":
                buscar_producto_por_id()
            case "6":
                buscar_por_nombre_o_categoria()
            case "7":
                reporte_stock_bajo()
            case "8":
                print(f"{Fore.CYAN}Gracias por usar el sistema. ¡Hasta luego!")
                ejecutando = False
            case _:
                print(f"{Fore.YELLOW}Opción inválida. Elija un número del 1 al 8.")

if __name__ == "__main__":
    main()