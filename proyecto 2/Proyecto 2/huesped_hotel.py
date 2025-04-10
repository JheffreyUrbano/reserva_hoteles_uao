import pyodbc
import conexion_bd as conexion

"""
Este módulo define la clase `huesped`, que se encarga de gestionar los datos de los huéspedes
en el sistema, incluyendo la creación, modificación, eliminación y consulta de huéspedes.
"""

class huesped:
    """
    Clase que representa un huésped en el hotel.

    Atributos:
    - __nombre (str): Nombre completo del huésped.
    - __cedula (int): Número de cédula del huésped.
    - __celular (int): Número de celular del huésped.
    """

    def __init__(self, nombre, cedula, celular):
        """
        Constructor de la clase huesped.

        Parámetros:
        - nombre (str): Nombre completo del huésped.
        - cedula (int): Número de cédula del huésped.
        - celular (int): Número de celular del huésped.
        """
        self.__nombre = nombre
        self.__cedula = cedula
        self.__celular = celular

    def crear_huesped(self):
        """
        Crea un nuevo huésped en la base de datos.

        Retorna:
        - error (str): Mensaje de error si ocurre algún problema, vacío si la operación es exitosa.
        """
        error = " "
        connection = conexion.conectar()
        try:
            if connection is not None:
                cursor = connection.cursor()
                # Inserta un nuevo huésped en la tabla `clientes`
                cursor.execute('INSERT INTO clientes (codcliente, nombre, telefono) VALUES (?, ?, ?)',
                               (self.__cedula, self.__nombre, self.__celular))
                connection.commit()
        except pyodbc.IntegrityError as ex:
            error = "El huésped ya existe en la base de datos."
        except ValueError as ex:
            error = "Error de valor: " + str(ex)
        except pyodbc.Error as ex:
            error = "Error de conexión: " + str(ex)
        finally:
            cursor.close()
            connection.close()
        return error

    def borrar_huesped(self):
        """
        Borra un huésped de la base de datos.

        Retorna:
        - None
        """
        connection = conexion.conectar()
        try:
            if connection is not None:
                cursor = connection.cursor()
                # Elimina un huésped de la tabla `clientes` según su cédula
                cursor.execute(
                    'DELETE FROM clientes WHERE codcliente = ?', (self.__cedula,))
                connection.commit()
                cursor.close()
        except pyodbc.Error as ex:
            print(f'Error al borrar el huésped: {ex}')
        finally:
            connection.close()

    def modificar_huesped(self):
        """
        Modifica un huésped en la base de datos.

        Retorna:
        - None
        """
        connection = conexion.conectar()
        try:
            if connection is not None:
                cursor = connection.cursor()
                # Actualiza los datos del huésped en la tabla `clientes`
                cursor.execute('UPDATE clientes SET nombre = ?, telefono = ? WHERE codcliente = ?',
                               (self.__nombre, self.__celular, self.__cedula))
                connection.commit()
                cursor.close()
        except pyodbc.Error as ex:
            print(f'Error al modificar el huésped: {ex}')
        finally:
            connection.close()

    def consultar_huesped(self, criterio):
        """
        Consulta un huésped en la base de datos según un criterio.

        Parámetros:
        - criterio (str): Criterio de búsqueda (puede ser nombre, cédula o celular).

        Retorna:
        - resultados (list): Lista de huéspedes que coinciden con el criterio.
        """
        connection = conexion.conectar()
        resultados = []
        try:
            if connection is not None:
                cursor = connection.cursor()
                # Consulta los huéspedes que coinciden con el criterio
                cursor.execute(
                    'SELECT * FROM clientes WHERE codcliente LIKE ? OR nombre LIKE ? OR telefono LIKE ?',
                    (f"%{criterio}%", f"%{criterio}%", f"%{criterio}%")
                )
                resultados = cursor.fetchall()
                cursor.close()
        except pyodbc.Error as ex:
            print(f"Error al consultar el huésped: {ex}")
        finally:
            connection.close()
        return resultados

    # Métodos getter y setter para los atributos de la clase

    def get_nombre(self):
        """
        Devuelve el nombre del huésped.
        """
        return self.__nombre

    def set_nombre(self, nombre):
        """
        Cambia el nombre del huésped.

        Parámetros:
        - nombre (str): Nuevo nombre del huésped.

        Excepciones:
        - TypeError: Si el nombre no es una cadena o está vacío.
        """
        if not isinstance(nombre, str) or not len(nombre) > 0:
            raise TypeError("Nombre inválido")
        self.__nombre = nombre

    def get_cedula(self):
        """
        Devuelve la cédula del huésped.
        """
        return self.__cedula

    def set_cedula(self, cedula):
        """
        Cambia la cédula del huésped.

        Parámetros:
        - cedula (int): Nueva cédula del huésped.

        Excepciones:
        - ValueError: Si la cédula no es un entero válido.
        """
        if not isinstance(cedula, int) or cedula < 0 or len(str(cedula)) < 8:
            raise ValueError("Cédula inválida")
        self.__cedula = cedula

    def get_celular(self):
        """
        Devuelve el celular del huésped.
        """
        return self.__celular

    def set_celular(self, celular):
        """
        Cambia el celular del huésped.

        Parámetros:
        - celular (int): Nuevo número de celular del huésped.

        Excepciones:
        - ValueError: Si el celular no es un entero válido.
        """
        if not isinstance(celular, int) or celular < 0 or len(str(celular)) < 10:
            raise ValueError("Celular inválido")
        self.__celular = celular