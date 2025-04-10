"""
Esta clase se encarga de la conexión a la base de datos
"""
import pyodbc
    
def conectar():
    server = '200.29.112.79\\sqlexpress'
    database = 'hoteljal'
    username = 'desarrollo'
    password = 'dzgUNLqXLQ0='
    driver = '{ODBC Driver 17 for SQL Server}'
    
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    try:
        connection = pyodbc.connect(connection_string)
        #print('Conexión exitosa')
        return connection
    except pyodbc.Error as ex:
        print(f'Error al conectar a la base de datos: {ex}')
        return None


def consultar_habitacion():
    connection = conectar()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM habitaciones where codestado=1')
        rows = cursor.fetchall()
        for row in rows:
            print(f'Las Habitaciones Disponibles son : ')
            print(f'ID: {row.numero}, Número: {row.descripcion}, Estado: {row.piso}')
            print('-------------------------------------------------------')
        cursor.close()
    connection.close()

def crear_habitacion (numero, descripcion, piso, tipo, codestado):
    connection = conectar()
    try:
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO habitaciones values (?, ?, ?, ?, ?)', (numero, descripcion, piso, tipo, codestado))
            connection.commit()
            print('Habitación creada exitosamente')
            cursor.close()
    except pyodbc.Error as ex:
        print(f'Error al crear la habitación: {ex}')
    connection.close()  

def main():
    consultar_habitacion()
    crear_habitacion('102','Habitacion 102','1','1','1')  # Ajusta los valores según tu base de datos


if __name__ == '__main__':
    main()