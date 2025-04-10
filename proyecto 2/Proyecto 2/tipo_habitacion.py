import pyodbc
import datetime
import conexion_bd as conexion

"""
Este módulo define la clase `TipoHabitacion`, que se encarga de gestionar los tipos de habitaciones
en el sistema, incluyendo la carga de tipos de habitación disponibles y habitaciones disponibles
según un rango de fechas.
"""

class TipoHabitacion:
    """
    Clase que representa un tipo de habitación en el hotel.

    Atributos:
    - codtipo (int): Código único del tipo de habitación.
    - descripcion (str): Descripción del tipo de habitación.
    - costo (float): Costo asociado al tipo de habitación.
    - estado (int): Estado del tipo de habitación (1 = activo, 0 = inactivo).
    """

    def __init__(self, codtipo, descripcion, costo, estado):
        """
        Constructor de la clase TipoHabitacion.

        Parámetros:
        - codtipo (int): Código único del tipo de habitación.
        - descripcion (str): Descripción del tipo de habitación.
        - costo (float): Costo asociado al tipo de habitación.
        - estado (int): Estado del tipo de habitación (1 = activo, 0 = inactivo).
        """
        self.codtipo = codtipo
        self.descripcion = descripcion
        self.costo = costo
        self.estado = estado

    def cargarTipoHabitacion(self):
        """
        Método que consulta la base de datos para obtener los tipos de habitación disponibles.

        Retorna:
        - tipos (list): Lista de tuplas con los tipos de habitación disponibles.
          Cada tupla contiene el código del tipo de habitación y su descripción.
        """
        connection = conexion.conectar()  # Conectar a la base de datos
        tipos = []  # Lista para almacenar los resultados
        try:
            if connection is not None:
                cursor = connection.cursor()
                # Consulta SQL para obtener los tipos de habitación disponibles
                cursor.execute("""
                    SELECT DISTINCT(th.codtipo) AS codtipo, th.descripcion 
                    FROM tipo_habitacion th, habitaciones h
                    WHERE th.codtipo = h.codtipo AND h.codestado = '1'
                    ORDER BY th.descripcion
                """)
                tipos = cursor.fetchall()  # Obtener los resultados de la consulta
                cursor.close()  # Cerrar el cursor
        except pyodbc.Error as ex:
            # Manejo de errores en la consulta SQL
            print(f"Error al consultar los tipos de habitación: {ex}")
        finally:
            # Cerrar la conexión a la base de datos
            connection.close()
        return tipos

    def cargarHabitacionDisponible(self, fecha_inicial, fecha_final, codtipo):
        """
        Método que consulta la base de datos para obtener las habitaciones disponibles
        de un tipo específico en un rango de fechas.

        Parámetros:
        - fecha_inicial (str): Fecha inicial del rango (formato: 'YYYY-MM-DD').
        - fecha_final (str): Fecha final del rango (formato: 'YYYY-MM-DD').
        - codtipo (int): Código del tipo de habitación.

        Retorna:
        - disponibles (list): Lista de habitaciones disponibles.
        """
        connection = conexion.conectar()  # Conectar a la base de datos
        disponibles = []  # Lista para almacenar los resultados
        try:
            if connection is not None:
                cursor = connection.cursor()
                # Consulta SQL para obtener las habitaciones disponibles
                cursor.execute('''
                    SELECT * 
                    FROM habitaciones h
                    WHERE h.codtipo = ? 
                    AND NOT EXISTS (
                        SELECT 1
                        FROM reserva r
                        WHERE r.numero = h.numero
                        AND r.fecha_reserva BETWEEN ? AND ?
                    )
                    ORDER BY h.numero;
                ''', (codtipo, fecha_inicial, fecha_final))
                disponibles = cursor.fetchall()  # Obtener los resultados de la consulta
                cursor.close()  # Cerrar el cursor
        except pyodbc.Error as ex:
            # Manejo de errores en la consulta SQL
            print(f"Error al consultar HABITACIONES DISPONIBLES: {ex}")
        finally:
            # Cerrar la conexión a la base de datos
            connection.close()
        return disponibles

