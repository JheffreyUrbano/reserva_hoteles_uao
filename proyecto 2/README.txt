# Sistema de Gestión de Reservas - Hotel JAL

Este proyecto es un sistema de gestión de reservas para un hotel. Permite gestionar habitaciones, clientes y reservas, así como realizar operaciones como crear, consultar, modificar y eliminar datos. La aplicación está desarrollada en Python y utiliza la biblioteca **Flet** para la interfaz gráfica y **pyodbc** para la conexión a la base de datos.

---

## Estructura del Proyecto

El proyecto está compuesto por los siguientes archivos principales:

1. **`app_hotel.py`**: Archivo principal que contiene la lógica de la interfaz gráfica y las funciones principales de la aplicación.
2. **`conexion_bd.py`**: Módulo encargado de gestionar la conexión a la base de datos.
3. **`habitacion_hotel.py`**: Módulo que define las clases relacionadas con las habitaciones del hotel.
4. **`huesped_hotel.py`**: Módulo que define la clase para gestionar los datos de los huéspedes.
5. **`reserva_hotel.py`**: Módulo que define la clase para gestionar las reservas del hotel.
6. **`tipo_habitacion.py`**: Módulo que define la clase para gestionar los tipos de habitaciones.
7. **`ReservaContext.py`**: Archivo adicional que puede contener lógica relacionada con el contexto de las reservas.

---

## Requisitos Previos

1. **Python 3.9 o superior**.
2. **Bibliotecas necesarias**:
   - `flet`
   - `pyodbc`
3. **Base de datos**:
   - El sistema está diseñado para conectarse a una base de datos SQL Server. Asegúrate de configurar correctamente los parámetros de conexión en el archivo `conexion_bd.py`.
4. **Entorno Virtual**
   -Debes cargar la carpeta ".\Proyecto 2\" para cargar el entorno virtual donde se encuentran las
librerías con sus respectivas versiones (Puedes encontrar las versiones en Requirements.txt).
5. **SQL Server**
Se debe instalar en la maquina "MS SQL Server" Versión 2017 
---

## Instalación

1. Clona el repositorio o descarga los archivos del proyecto.
2. Instala las dependencias necesarias ejecutando:
   ```bash
   pip install flet pyodbc