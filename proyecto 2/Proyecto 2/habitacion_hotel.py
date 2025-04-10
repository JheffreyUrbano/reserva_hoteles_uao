"""
Módulo que define clases para representar habitaciones de hotel.

Este módulo incluye una clase base `HabitacionBase` y tres clases derivadas
para representar habitaciones dobles, triples y cuádruples.

Clases:
- HabitacionBase: Clase base para habitaciones de hotel.
- HabitacionDoble: Clase para habitaciones dobles.
- HabitacionTriple: Clase para habitaciones triples.
- HabitacionCuadruple: Clase para habitaciones cuádruples.
"""
import flet as ft
import conexion_bd as conexion
import pyodbc

class Habitacion:
    """
    Clase base que representa una habitación de hotel.

    Atributos:
    - __numero (int): Número de la habitación.
    - __costo (float): Costo de la habitación.
    - __reservada (bool): Estado de la habitación (reservada o disponible).
    - __tipo (str): Tipo de habitación.

    Métodos:
    - reservar(): Marca la habitación como reservada.
    - cancelar_reserva(): Cancela la reserva de la habitación.
    - is_reservada(): Devuelve el estado de reserva de la habitación.
    - get_numero(): Devuelve el número de la habitación.
    - get_costo(): Devuelve el costo de la habitación.
    - get_tipo(): Devuelve el tipo de la habitación.
    - __str__(): Devuelve una representación en cadena de la habitación.
    """

    def __init__(self, numero, descripcion, piso, codtipo, codestado):
        """
        Constructor de la clase HabitacionBase.

        Parámetros:
        - numero (int): Número de la habitación.
        - costo (float): Costo de la habitación.
        - tipo (str): Tipo de la habitación.
        """
        self.__numero = numero
        self.__descripcion = descripcion
        self.__piso = piso
        self.__codtipo = codtipo
        self.__codestado = codestado


    def habitaciones_disponibles(self):
        """
        Este método consulta la base de datos y devuelve un diccionario con la información de habitaciones disponibles.
        """
        disponibles = {}
        connection = conexion.conectar()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute('''
                           SELECT h.numero, h.descripcion AS habitacion, eh.descripcion AS estado, th.descripcion AS tipo, th.costo
                            FROM habitaciones AS h INNER JOIN
                            estados_h AS eh ON h.codestado = eh.codestado INNER JOIN
                            tipo_habitacion AS th ON h.codtipo = th.codtipo
                           ''')
            rows = cursor.fetchall()
            for row in rows:
                disponibles[row.numero] = {
                    'habitacion': row.habitacion,
                    'estado': row.estado,
                    'tipo': row.tipo,
                    'costo': row.costo
                }
            cursor.close()
        connection.close()
        return disponibles
    
    def cambiar_estado(self, nuevo_estado):
        """
        Cambia el estado de la habitación en la base de datos.
        
        Parámetros:
        - nuevo_estado (int): El nuevo estado de la habitación (1 = disponible, 2 = reservado, etc.).
        """
        connection = conexion.conectar()
        try:
            if connection is not None:
                cursor = connection.cursor()
                cursor.execute(
                    'UPDATE habitaciones SET codestado = ? WHERE numero = ?',
                    (nuevo_estado, self.__numero)
                )
                connection.commit()
                #print(f"Estado de la habitación {self.__numero} cambiado a {nuevo_estado}.")
        except pyodbc.Error as ex:
            print(f"Error al cambiar el estado de la habitación: {ex}")
        finally:
            cursor.close()
            connection.close()
    
    # sets y gets

    def set_numero(self, numero):
        """
        Establece el número de la habitación.

        Parámetros:
        - numero (int): Nuevo número de la habitación.
        """
        self.__numero = numero

    def get_numero(self):
        """
        Devuelve el número de la habitación.

        Retorno:
        - int: Número de la habitación.
        """
        return self.__numero

    def set_descripcion(self, descripcion):
        """
        Establece la descripción de la habitación.

        Parámetros:
        - descripcion (str): Nueva descripción de la habitación.
        """
        self.__descripcion = descripcion

    def get_descripcion(self):
        """
        Devuelve la descripción de la habitación.

        Retorno:
        - str: Descripción de la habitación.
        """
        return self.__descripcion

    def set_piso(self, piso):
        """
        Establece el piso de la habitación.

        Parámetros:
        - piso (int): Nuevo piso de la habitación.
        """
        self.__piso = piso

    def get_piso(self):
        """
        Devuelve el piso de la habitación.

        Retorno:
        - int: Piso de la habitación.
        """
        return self.__piso

    def set_codtipo(self, codtipo):
        """
        Establece el código de tipo de la habitación.

        Parámetros:
        - codtipo (str): Nuevo código de tipo de la habitación.
        """
        self.__codtipo = codtipo

    def get_codtipo(self):
        """
        Devuelve el código de tipo de la habitación.

        Retorno:
        - str: Código de tipo de la habitación.
        """
        return self.__codtipo

    def set_codestado(self, codestado):
        """
        Establece el código de estado de la habitación.

        Parámetros:
        - codestado (str): Nuevo código de estado de la habitación.
        """
        self.__codestado = codestado

    def get_codestado(self):
        """
        Devuelve el código de estado de la habitación.

        Retorno:
        - str: Código de estado de la habitación.
        """
        return self.__codestado

    
        
class HabitacionDoble(Habitacion):
    """
    Clase que representa una habitación doble.

    Hereda de:
    - HabitacionBase

    Atributos adicionales:
    - __tipo (str): Tipo de habitación (Doble).
    """

    def __init__(self, numero, descripcion, piso, codtipo, codestado):
        """
        Constructor de la clase HabitacionDoble.

        Parámetros:
        - numero (int): Número de la habitación.
        - descripcion (str): Descripción de la habitación.
        - piso (int): Piso de la habitación.
        - codtipo (str): Código de tipo de la habitación.
        - codestado (str): Código de estado de la habitación.
        """
        super().__init__(numero, descripcion, piso, codtipo, codestado)


class HabitacionTriple(Habitacion):
    """
    Clase que representa una habitación triple.

    Hereda de:
    - HabitacionBase

    Atributos adicionales:
    - __tipo (str): Tipo de habitación (Triple).
    """
    def __init__(numero, descripcion, piso, codtipo, codestado):
        super().__init__(numero, descripcion, piso, codtipo, codestado)


class HabitacionCuadruple(Habitacion):
    """
    Clase que representa una habitación cuádruple.

    Hereda de:
    - HabitacionBase

    Atributos adicionales:
    - __tipo (str): Tipo de habitación (Cuadruple).
    """
    def __init__(self, numero, descripcion, piso, codtipo, codestado):
        super().__init__(numero, descripcion, piso, codtipo, codestado)
        self.__tipo = "Cuadruple"
    
    

