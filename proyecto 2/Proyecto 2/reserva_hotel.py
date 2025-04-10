import datetime
import habitacion_hotel
import huesped_hotel
import conexion_bd as conexion
import pyodbc

"""
Este módulo define la clase `Reserva`, que se encarga de gestionar las reservas
en el sistema, incluyendo la creación, eliminación y consulta de reservas.
"""

class Reserva:
    """
    Clase que representa una reserva en el hotel.

    Atributos:
    - reservanum (int): Número único de la reserva.
    - habitanum (int): Número de la habitación reservada.
    - codcliente (int): Código del cliente que realiza la reserva.
    - fecha_reserva (str): Fecha de la reserva (formato: 'YYYY-MM-DD').
    - cantidad_dias (int): Número de días de la reserva.
    - fecha_salida (str): Fecha de salida (formato: 'YYYY-MM-DD').
    """

    def __init__(self, reservanum, habitanum, codcliente, fecha_reserva, cantidad_dias, fecha_salida):
        """
        Constructor de la clase Reserva.

        Parámetros:
        - reservanum (int): Número único de la reserva.
        - habitanum (int): Número de la habitación reservada.
        - codcliente (int): Código del cliente que realiza la reserva.
        - fecha_reserva (str): Fecha de la reserva (formato: 'YYYY-MM-DD').
        - cantidad_dias (int): Número de días de la reserva.
        - fecha_salida (str): Fecha de salida (formato: 'YYYY-MM-DD').
        """
        self.__reservanum = reservanum
        self.__habitanum = habitanum
        self.__codcliente = codcliente
        self.__fecha_reserva = fecha_reserva
        self.__cantidad_dias = cantidad_dias
        self.__fecha_salida = fecha_salida
        self.__estado = "0"  # Estado inicial de la reserva (0 = Activa, 1 = Registrada, 2 = Cancelada)
    
    def eliminar_reserva(self):
        """
        Elimina una reserva de la base de datos.

        Retorna:
        - error (str): Mensaje de error si ocurre algún problema, vacío si la operación es exitosa.
        """
        error = " "
        connection = conexion.conectar()
        try:
            if connection is not None:
                cursor = connection.cursor()
                cursor.execute('DELETE FROM reserva WHERE reservano = ?', (self.__reservanum,))
                connection.commit()
        except pyodbc.IntegrityError as ex:
            error = "Error de integridad: " + str(ex)
        except ValueError as ex:
            error = "Error de valor: " + str(ex)
        except pyodbc.Error as ex:
            error = "Error de conexión: " + str(ex)
        finally:
            cursor.close()
            connection.close()
        return error

    def reserva_numero(self):
        """
        Obtiene el siguiente número de reserva disponible.

        Retorna:
        - reservano (int): Número de reserva disponible.
        """
        connection = conexion.conectar()
        try:
            if connection is not None:
                cursor = connection.cursor()
                # Consulta SQL para obtener el siguiente número de reserva
                cursor.execute('''SELECT isnull((MAX(convert(float,reservano))+1),1) 
                               AS campo 
                               FROM reserva''')
                rows = cursor.fetchall()
                for row in rows:
                    reservano = row[0]
                    
                cursor.close()
                return reservano
        except pyodbc.Error as ex:
            print(f"Error al consultar los datos: {ex}")
        finally:
            connection.close()
    
    
    def guardar_reserva(self):
        """
        Guarda una nueva reserva en la base de datos.

        Retorna:
        - error (str): Mensaje de error si ocurre algún problema, vacío si la operación es exitosa.
        """
        error = " "
        connection = conexion.conectar()
        try:
            if connection is not None:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO reserva (reservano, numero, codcliente, fecha_reserva, cantidad_dias, fecha_salida) VALUES (?, ?, ?, ?, ?, ?)',
                               (self.__reservanum, self.__habitanum, self.__codcliente, self.__fecha_reserva, self.__cantidad_dias, self.__fecha_salida))
                connection.commit()
        except pyodbc.IntegrityError as ex:
            error = "Error de integridad: " + str(ex)
        except ValueError as ex:
            error = "Error de valor: " + str(ex)
        except pyodbc.Error as ex:
            error = "Error de conexión: " + str(ex)
        finally:
            cursor.close()
            connection.close()
        return error
    
    def consultar_reservas_por_cliente(self):
        """
        Consulta las reservas asociadas a un cliente en la base de datos.

        Retorna:
        - resultados (list): Lista de reservas asociadas al cliente.
        """
        connection = conexion.conectar()
        resultados = []
        try:
            if connection is not None:
                cursor = connection.cursor()
                cursor.execute(
                    'SELECT reservano, fecha_reserva, fecha_salida FROM reserva WHERE codcliente = ?',
                    (self.__codcliente,)
                )
                resultados = cursor.fetchall()
                cursor.close()
        except pyodbc.Error as ex:
            print(f"Error al consultar las reservas del cliente: {ex}")
        finally:
            connection.close()
        return resultados
    
    def __str__(self):
        """
        Representación en cadena de la reserva.

        Retorna:
        - str: Información de la reserva.
        """
        return print(f"Reserva de {self.huesped.get_nombre()} en habitación " \
                    f"{self.habitacion.get_numero()} del {self.fecha_entrada} al "\
                    f"{self.fecha_salida} - Estado: {self.estado}")


