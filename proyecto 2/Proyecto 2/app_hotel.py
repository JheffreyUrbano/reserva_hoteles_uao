import flet as ft
import habitacion_hotel as room
import huesped_hotel as huesped
import conexion_bd as conexion
import tipo_habitacion as tipoh
import reserva_hotel as reservas
import ReservaContext


def habitacion_disponible(page):
    """
    Función que muestra las habitaciones disponibles en la interfaz.

    Parámetros:
    - page (ft.Page): Página principal de la aplicación.
    """
    # Crear una instancia de la clase Habitacion con valores predeterminados
    habitacion = room.Habitacion(0, "", 0, "", "")

    # Obtener un diccionario con las habitaciones disponibles desde la base de datos
    dict_dispo = habitacion.habitaciones_disponibles()

    # Limpiar el contenedor de vista para actualizar el contenido
    contenedor_vista.controls.clear()

    # Agregar un título y subtítulo al contenedor
    contenedor_vista.controls.append(
        ft.Column(
            [
                ft.Text("Habitaciones - Estados",
                        style="headlineMedium", color="blue"),  # Título principal
                ft.Text("Las habitaciones con su respectivo estado son:",
                        style="bodyMedium"),  # Subtítulo
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Alinear verticalmente al centro
            horizontal_alignment=ft.CrossAxisAlignment.START,  # Alinear horizontalmente a la izquierda
        )
    )

    # Recorrer el diccionario de habitaciones disponibles y agregarlas al contenedor
    for row in dict_dispo.values():
        contenedor_vista.controls.append(
            ft.Container(
                content=ft.Text(
                    f"{row['habitacion']}, Estado: {row['estado']}, Tipo: {row['tipo']}, Precio: {row['costo']}",
                    style="bodySmall",  # Estilo del texto para cada habitación
                ),
                padding=ft.padding.all(5),  # Agregar espacio alrededor del texto
            )
        )

    # Actualizar la página para reflejar los cambios
    page.update(contenedor_vista)


# ----------------------------SECCIÓN DE MANEJO DE CLIENTES-------------------------------
# Función para crear un nuevo huésped
def crear_cliente(page):
    """
    Función que permite crear un nuevo huésped en la base de datos.

    Parámetros:
    - page (ft.Page): Página principal de la aplicación.
    """
    # Campos de entrada para los datos del huésped
    nombre_huesped = ft.TextField(label="Nombre del huésped", width=300)
    cedula_huesped = ft.TextField(
        label="Cédula del huésped", keyboard_type="number", width=300)
    celular_huesped = ft.TextField(
        label="Celular del huésped", keyboard_type="number", width=300)
    mensaje = ft.Text(value="", color="green")  # Mensaje para mostrar errores o confirmaciones

    # Función para manejar la creación del huésped
    def insertar_cliente(e):
        """
        Inserta un nuevo huésped en la base de datos.

        Parámetros:
        - e: Evento que activa la función (clic en el botón).
        """
        try:
            # Validar que el nombre no esté vacío
            if not nombre_huesped.value.strip():
                raise ValueError("El nombre del huésped no puede estar vacío.")
            # Validar que el celular sea un número válido
            if not celular_huesped.value.strip().isdigit():
                raise ValueError("El celular debe ser un número válido.")

            # Crear una instancia de la clase huesped
            nuevo_huesped = huesped.huesped(
                nombre_huesped.value.strip(),
                int(cedula_huesped.value.strip()),
                int(celular_huesped.value.strip())
            )

            # Guardar el nuevo huésped en la base de datos
            error = nuevo_huesped.crear_huesped()
            if len(str(error)) > 1:
                mensaje.value = error  # Mostrar el error en la interfaz
                mensaje.color = "red"
            else:
                mensaje.value = "Huésped creado con éxito."
                mensaje.color = "green"
                # Limpiar los campos de entrada
                nombre_huesped.value = ""
                cedula_huesped.value = ""
                celular_huesped.value = ""
        except ValueError as ex:
            mensaje.value = str(ex)  # Mostrar el error en la interfaz
            mensaje.color = "red"
        page.update()

    # Agregar los campos de entrada y el botón al contenedor
    contenedor_vista.controls.clear()
    contenedor_vista.controls.append(
        ft.Column([
            nombre_huesped,
            cedula_huesped,
            celular_huesped,
            mensaje,
            ft.ElevatedButton("Crear Cliente", on_click=insertar_cliente)  # Botón para crear el cliente
        ])
    )
    page.update()


def actualizar_cliente(page):
    # Crear campos para la búsqueda y los datos del cliente
    criterio_busqueda = ft.TextField(
        label="Cédula, Nombre o Celular del huésped", width=300,
        on_change=lambda e: cliente_dropdown()
    )
    dropdown_resultados = ft.Dropdown(
        width=400, options=[], on_change=lambda e: seleccionar_cliente())
    mensaje = ft.Text(value="", color="green")

    # Campos de edición (inicialmente ocultos)
    nombre_huesped = ft.TextField(
        label="Nombre del huésped", width=300, visible=False)
    cedula_huesped = ft.TextField(
        label="Cédula del huésped", keyboard_type="number", width=300, read_only=True, visible=False)
    celular_huesped = ft.TextField(
        label="Celular del huésped", keyboard_type="number", width=300, visible=False)

    # Botón de acción (inicialmente oculto)
    boton_editar = ft.ElevatedButton(
        "Editar Cliente", on_click=lambda e: editar_cliente(e), visible=False)
    boton_eliminar = ft.ElevatedButton(
        "Eliminar Cliente", on_click=lambda e: borrar_cliente(e), visible=False)

    # Función para actualizar el Dropdown de actualizar_cliente
    def cliente_dropdown():
        try:
            if not criterio_busqueda.value.strip():
                dropdown_resultados.options = []
                page.update()
                return

            # Crear una instancia de la clase huesped
            cliente_huesped = huesped.huesped("", 0, "")
            resultados = cliente_huesped.consultar_huesped(
                criterio_busqueda.value.strip())

            if resultados:
                dropdown_resultados.options = [
                    ft.dropdown.Option(f"{cliente[0]} - {cliente[1]} - {cliente[2]}") for cliente in resultados
                ]
            else:
                dropdown_resultados.options = []

            page.update()
        except Exception as ex:
            mensaje.value = f"Error al buscar el cliente: {ex}"
            mensaje.color = "red"
            page.update()

    # Función para seleccionar un cliente del Dropdown
    def seleccionar_cliente():
        try:
            if not dropdown_resultados.value:
                return

            # Extraer los datos del cliente seleccionado
            datos_cliente = dropdown_resultados.value.split(" - ")
            cedula_huesped.value = datos_cliente[0]
            nombre_huesped.value = datos_cliente[1]
            celular_huesped.value = datos_cliente[2]

            # Hacer visibles los campos y los botones
            nombre_huesped.visible = True
            cedula_huesped.visible = True
            celular_huesped.visible = True
            boton_editar.visible = True
            boton_eliminar.visible = True

            # Limpiar el cuadro de búsqueda
            criterio_busqueda.value = ""
            dropdown_resultados.options = []

            mensaje.value = "Cliente seleccionado."
            mensaje.color = "green"
            page.update()
        except Exception as ex:
            mensaje.value = f"Error al seleccionar el cliente: {ex}"
            mensaje.color = "red"
            page.update()

    # Función para editar el cliente seleccionado
    def editar_cliente(e):
        try:
            if not nombre_huesped.value.strip():
                raise ValueError("El nombre del huésped no puede estar vacío.")
            if not celular_huesped.value.strip().isdigit():
                raise ValueError("El celular debe ser un número válido.")

            # Crear una instancia de la clase huesped
            cliente_huesped = huesped.huesped(
                nombre_huesped.value.strip(),
                int(cedula_huesped.value.strip()),
                int(celular_huesped.value.strip())
            )
            cliente_huesped.modificar_huesped()

            mensaje.value = "Cliente actualizado con éxito."
            mensaje.color = "green"

            # Limpiar los campos
            limpiar_campos()
        except ValueError as ex:
            mensaje.value = str(ex)
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error al actualizar el cliente: {ex}"
            mensaje.color = "red"
        page.update()

    # Función para borrar el cliente seleccionado
    def borrar_cliente(e):
        try:
            if not cedula_huesped.value.strip().isdigit():
                raise ValueError("La cédula debe ser un número válido.")

            # Crear una instancia de la clase huesped
            cliente_huesped = huesped.huesped(
                "", int(cedula_huesped.value.strip()), "")
            cliente_huesped.borrar_huesped()

            mensaje.value = "Huésped eliminado con éxito."
            mensaje.color = "green"

            # Limpiar los campos
            limpiar_campos()
        except ValueError as ex:
            mensaje.value = str(ex)
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error al eliminar el cliente: {ex}"
            mensaje.color = "red"
        page.update()

    # Función para limpiar los campos
    def limpiar_campos():
        nombre_huesped.value = ""
        cedula_huesped.value = ""
        celular_huesped.value = ""
        nombre_huesped.visible = False
        cedula_huesped.visible = False
        celular_huesped.visible = False
        boton_editar.visible = False
        boton_eliminar.visible = False
        page.update()

    # Actualizar la interfaz
    contenedor_vista.controls.clear()
    contenedor_vista.controls.append(
        ft.Column([
            criterio_busqueda,
            dropdown_resultados,
            nombre_huesped,
            cedula_huesped,
            celular_huesped,
            mensaje,
            ft.Row(
                [
                    boton_editar,  # Botón para editar al cliente
                    boton_eliminar,  # Botón para borrar al cliente
                ]
            ),
        ])
    )
    page.update()


# ---------------------------------FUNCION PARA MANEJO DE RESERVAS --------------------------------------
# CREACIÓN DE CLIENTE EN CASO DE NO ESTÁR REGISTRADO
def crear_reserva(page):
    # Variable global para almacenar la habitación seleccionada
    global habita_seleccionado
    habita_seleccionado = ""

    # Función para actualizar la habitación seleccionada
    def habitacion_seleccionada(num_habitacion):
        global habita_seleccionado
        habita_seleccionado = num_habitacion

    # Función para manejar la selección de habitaciones disponibles
    def seleccionar_disponibles():
        try:
            if not habitaciones_dispodropdown.value:
                return

            # Extraer los datos de la habitación disponible
            datos_disponibles = habitaciones_dispodropdown.value.split(" - ")
            # Actualiza la habitación seleccionada
            habitacion_seleccionada(datos_disponibles[0])

            mensaje.value = "Habitación seleccionada."
            mensaje.color = "green"
            page.update()
        except Exception as ex:
            mensaje.value = f"Error al seleccionar habitación disponible: {ex}"
            mensaje.color = "red"
            page.update()

    # Función para insertar una nueva reserva
    def insertar_reserva(e):
        try:
            if not habita_seleccionado:
                raise ValueError("Debe seleccionar una habitación disponible.")

            r = reservas.Reserva("", "", "", "", 0, "")
            consecutivo = r.reserva_numero()

            nueva_reserva = reservas.Reserva(
                consecutivo,
                habita_seleccionado,  # Usa la habitación seleccionada
                cedula_huesped.value.strip(),
                criterio1_busqueda.value.strip(),
                "0",
                criterio2_busqueda.value.strip()
            )

            # Guardar nueva reserva en la base de datos
            error = nueva_reserva.guardar_reserva()
            if len(str(error)) > 1:
                mensaje.value = error
                mensaje.color = "red"
            else:
                # Cambiar el estado de la habitación a "2" (reservado)
                habitacion = room.Habitacion(
                    numero=habita_seleccionado,
                    descripcion="",
                    piso=0,
                    codtipo="",
                    codestado=1  # Estado actual (disponible)
                )
                habitacion.cambiar_estado(2)  # Cambiar estado a reservado

                mensaje.value = f"Reserva número: {consecutivo} fue creada con éxito."
                mensaje.color = "green"
        except ValueError as ex:
            mensaje.value = str(ex)
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error al crear la reserva: {ex}"
            mensaje.color = "red"
        page.update()

    # Campos para ingresar los datos del huésped
    cedula_huesped = ft.TextField(
        label="Cédula del huésped", keyboard_type="number")
    nombre_huesped = ft.TextField(
        label="Nombre del huésped", width=300, visible=False)
    celular_huesped = ft.TextField(
        label="Celular del huésped", keyboard_type="number", width=300, visible=False)

    # Etiquetas para mostrar información del huésped
    nombre_label = ft.Text(
        "Nombre: ", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, visible=False)
    celular_label = ft.Text(
        "Celular: ", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, visible=False)

    # Botones para consultar y crear cliente, y para crear reserva
    boton_consultar_cliente = ft.ElevatedButton(
        "Consultar Cliente", on_click=lambda e: consultar_cliente(e), width=150)
    boton_crear_cliente = ft.ElevatedButton(
        "Crear Cliente", on_click=lambda e: insertar_cliente(e), visible=False)
    boton_crear_reserva = ft.ElevatedButton(
        "Crear Reserva", on_click=lambda e: insertar_reserva(e), width=150)

    # Función para manejar la creación del huésped
    def insertar_cliente(e):
        try:
            if not nombre_huesped.value.strip():
                raise ValueError("El nombre del huésped no puede estar vacío.")
            if not celular_huesped.value.strip().isdigit():
                raise ValueError("El celular debe ser un número válido.")

            # Crear el huésped
            nuevo_huesped = huesped.huesped(
                nombre_huesped.value.strip(),
                int(cedula_huesped.value.strip()),
                int(celular_huesped.value.strip())
            )

            # Guardar el nuevo huésped en la base de datos
            error = nuevo_huesped.crear_huesped()
            if len(str(error)) > 1:
                mensaje.value = error
                mensaje.color = "red"
            else:
                mensaje.value = "Huésped creado con éxito."
                mensaje.color = "green"
                nombre_huesped.value = ""
                cedula_huesped.value = ""
                celular_huesped.value = ""
                nombre_huesped.visible = False
                celular_huesped.visible = False
                boton_crear_cliente.visible = False
        except ValueError as ex:
            mensaje.value = str(ex)
            mensaje.color = "red"
        page.update()

    # Función para manejar la consulta del huésped
    def consultar_cliente(e):
        try:
            if not cedula_huesped.value.strip().isdigit():
                raise ValueError("La cédula debe ser un número válido.")

            # Crear una instancia de la clase huesped
            cliente_huesped = huesped.huesped(
                "", int(cedula_huesped.value.strip()), "")
            resultados = cliente_huesped.consultar_huesped(
                cedula_huesped.value.strip())

            if resultados:
                # Mostrar los datos del cliente encontrado
                nombre_huesped.value = resultados[0][1]  # Nombre
                celular_huesped.value = resultados[0][2]  # Celular
                nombre_label.value = "Nombre: " + resultados[0][1]
                celular_label.value = "Celular: " + resultados[0][2]
                mensaje.value = "Cliente encontrado."
                mensaje.color = "green"
                nombre_label.visible = True
                celular_label.visible = True
            else:
                mensaje.value = "No se encontró ningún cliente con la cédula ingresada. Por favor, ingrese los datos para crear uno nuevo."
                mensaje.color = "red"
                nombre_huesped.value = ""
                cedula_huesped.value = ""
                celular_huesped.value = ""
                nombre_label.visible = False
                celular_label.visible = False
                nombre_huesped.visible = True
                celular_huesped.visible = True
                boton_crear_cliente.visible = True
        except ValueError as ex:
            mensaje.value = str(ex)
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error al consultar el cliente: {ex}"
            mensaje.color = "red"
        page.update()

    # Campos para las fechas de la reserva
    criterio1_busqueda = ft.TextField(label="Fecha Inicial de la reserva")
    criterio2_busqueda = ft.TextField(
        label="Fecha Final", on_change=lambda e: tipo_dropdown())

    # Dropdowns para tipos de habitación y habitaciones disponibles
    dropdown_resultados = ft.Dropdown(
        label="Tipo de Habitación", width=400, options=[], on_change=lambda e: seleccionar_tipo())
    habitaciones_dispodropdown = ft.Dropdown(
        label="Habitaciones Disponibles", width=400, options=[], visible=False, on_change=lambda e: seleccionar_disponibles())

    mensaje = ft.Text(value="", color="green")

    # Función para cargar los tipos de habitación
    def tipo_dropdown():
        try:
            if not criterio1_busqueda.value.strip() or not criterio2_busqueda.value.strip():
                dropdown_resultados.options = []
                page.update()
                return

            tipo_habitacion = tipoh.TipoHabitacion(0, "", 0, 1)
            resultados = tipo_habitacion.cargarTipoHabitacion()

            if resultados:
                habitaciones_dispodropdown.options = []
                dropdown_resultados.options = [
                    ft.dropdown.Option(f"{tipo[0]} - {tipo[1]}") for tipo in resultados
                ]
                habitaciones_dispodropdown.visible = True
            else:
                mensaje.value = "No hay tipos de habitación disponibles."
                mensaje.color = "red"
            page.update()
        except Exception as ex:
            mensaje.value = f"Error al cargar tipos de habitación: {ex}"
            mensaje.color = "red"
            page.update()

    # Función para manejar la selección de tipo de habitación
    def seleccionar_tipo():
        try:
            if not dropdown_resultados.value:
                return

            datos_tipo = dropdown_resultados.value.split(" - ")
            tipo_seleccionado = datos_tipo[0]

            disponible_dropdown(tipo_seleccionado)
            mensaje.value = "Tipo seleccionado."
            mensaje.color = "green"
            page.update()
        except Exception as ex:
            mensaje.value = f"Error al seleccionar tipo: {ex}"
            mensaje.color = "red"
            page.update()

    # Función para cargar las habitaciones disponibles
    def disponible_dropdown(seleccionado):
        try:
            habita_dispo = tipoh.TipoHabitacion(0, "", 0, 1)
            resultados = habita_dispo.cargarHabitacionDisponible(
                criterio1_busqueda.value.strip(),
                criterio2_busqueda.value.strip(),
                seleccionado
            )

            if resultados:
                habitaciones_dispodropdown.options = [
                    ft.dropdown.Option(f"{hab[0]} - {hab[1]}") for hab in resultados
                ]
            else:
                habitaciones_dispodropdown.options = []
                mensaje.value = "No hay habitaciones disponibles."
                mensaje.color = "red"
            page.update()
        except Exception as ex:
            mensaje.value = f"Error al cargar habitaciones disponibles: {ex}"
            mensaje.color = "red"
            page.update()

    # Contenedor para la vista de crear reserva
    contenedor_vista.controls.clear()
    contenedor_vista.controls.append(
        ft.Column([
            ft.Row([cedula_huesped, boton_consultar_cliente, nombre_label]),
            nombre_huesped,
            celular_huesped,
            boton_crear_cliente,
            criterio1_busqueda,
            criterio2_busqueda,
            dropdown_resultados,
            habitaciones_dispodropdown,
            boton_crear_reserva,
            mensaje,
        ])
    )
    page.update()


def eliminar_reserva(page):
    # Campo para ingresar el código del cliente
    codigo_cliente = ft.TextField(
        label="Cédula del huésped", keyboard_type="number")
    dropdown_reservas = ft.Dropdown(
        label="Reservas del Cliente", width=400, options=[])
    mensaje = ft.Text(value="", color="green")
    # Mostrar el nombre del cliente
    nombre_cliente = ft.Text(value="", color="blue")
    # Mostrar el celular del cliente
    celular_cliente = ft.Text(value="", color="blue")

    # Función para cargar las reservas del cliente
    def cargar_reservas(e):
        try:
            if not codigo_cliente.value.strip().isdigit():
                # Validar que el código del cliente sea un número válido
                raise ValueError("Debe ingresar un código de cliente válido.")

            # Crear una instancia de la clase Reserva
            cliente_reservas = reservas.Reserva(
                reservanum=None,  # Número de reserva (no necesario para esta consulta)
                habitanum=None,  # Número de habitación (no necesario para esta consulta)
                codcliente=int(codigo_cliente.value.strip()),  # Código del cliente
                fecha_reserva=None,  # Fecha de reserva (no necesario para esta consulta)
                cantidad_dias=None,  # Cantidad de días (no necesario para esta consulta)
                fecha_salida=None  # Fecha de salida (no necesario para esta consulta)
            )

            # Consultar las reservas del cliente usando el método de reserva_hotel.py
            resultados = cliente_reservas.consultar_reservas_por_cliente()

            # Consultar la información del cliente
            cliente_huesped = huesped.huesped(
                "",  # Nombre del cliente (no necesario para esta consulta)
                int(codigo_cliente.value.strip()),  # Código del cliente
                ""  # Celular del cliente (no necesario para esta consulta)
            )
            cliente_info = cliente_huesped.consultar_huesped(
                codigo_cliente.value.strip())  # Consultar información del cliente

            if cliente_info:
                # Si se encuentra información del cliente, mostrarla en la interfaz
                nombre_cliente.value = f"Nombre: {cliente_info[0][1]}"
                celular_cliente.value = f"Celular: {cliente_info[0][2]}"
            else:
                # Si no se encuentra información del cliente, mostrar un mensaje
                nombre_cliente.value = "Cliente no encontrado."
                celular_cliente.value = ""

            if resultados:
                # Si se encuentran reservas, llenar el Dropdown con las reservas del cliente
                dropdown_reservas.options = [
                    ft.dropdown.Option(f"{reserva[0]} - {reserva[1]} a {reserva[2]}") for reserva in resultados
                ]
                mensaje.value = "Reservas cargadas correctamente."
                mensaje.color = "green"
            else:
                # Si no se encuentran reservas, mostrar un mensaje
                dropdown_reservas.options = []
                mensaje.value = "No se encontraron reservas para este cliente."
                mensaje.color = "red"
            page.update()
        except ValueError as ex:
            # Manejar errores de validación
            mensaje.value = str(ex)
            mensaje.color = "red"
        except Exception as ex:
            # Manejar errores generales
            mensaje.value = f"Error al cargar las reservas: {ex}"
            mensaje.color = "red"
        page.update()

    # Función para eliminar la reserva seleccionada
    def borrar_reserva(e):
        """
        Elimina la reserva seleccionada del Dropdown.

        Parámetros:
        - e: Evento que activa la función (clic en el botón).
        """
        try:
            if not dropdown_reservas.value:
                # Validar que se haya seleccionado una reserva
                raise ValueError("Debe seleccionar una reserva para eliminar.")

            # Extraer el número de la reserva seleccionada
            numero_reserva = dropdown_reservas.value.split(" - ")[0]

            # Crear una instancia de la clase Reserva
            reserva = reservas.Reserva(
                reservanum=int(numero_reserva),  # Número de reserva
                habitanum=None,  # Número de habitación (no necesario para esta operación)
                codcliente=None,  # Código del cliente (no necesario para esta operación)
                fecha_reserva=None,  # Fecha de reserva (no necesario para esta operación)
                cantidad_dias=None,  # Cantidad de días (no necesario para esta operación)
                fecha_salida=None  # Fecha de salida (no necesario para esta operación)
            )

            # Llamar al método para eliminar la reserva
            error = reserva.eliminar_reserva()
            if len(str(error)) > 1:
                # Si ocurre un error, mostrarlo en la interfaz
                mensaje.value = error
                mensaje.color = "red"
            else:
                # Si la operación es exitosa, mostrar un mensaje de éxito
                mensaje.value = f"Reserva número {numero_reserva} eliminada con éxito."
                mensaje.color = "green"
                # Limpiar los campos y el Dropdown
                dropdown_reservas.options = []
                codigo_cliente.value = ""
                nombre_cliente.value = ""
                celular_cliente.value = ""
        except ValueError as ex:
            # Manejar errores de validación
            mensaje.value = str(ex)
            mensaje.color = "red"
        except Exception as ex:
            # Manejar errores generales
            mensaje.value = f"Error al eliminar la reserva: {ex}"
            mensaje.color = "red"
        page.update()

    # Actualizar la interfaz
    contenedor_vista.controls.clear()
    contenedor_vista.controls.append(
        ft.Column([
            codigo_cliente,  # Campo para ingresar el código del cliente
            ft.ElevatedButton("Cargar Reservas", on_click=cargar_reservas),  # Botón para cargar reservas
            nombre_cliente,  # Mostrar el nombre del cliente
            celular_cliente,  # Mostrar el celular del cliente
            dropdown_reservas,  # Dropdown para seleccionar una reserva
            ft.ElevatedButton("Eliminar Reserva", on_click=borrar_reserva),  # Botón para eliminar la reserva
            mensaje  # Mensaje para mostrar errores o confirmaciones
        ])
    )
    page.update()


# Contenedor principal para cambiar vistas
contenedor_vista = ft.Column(expand=True)


def main(page: ft.Page):
    # Configuración de la página
    page.title = "Sistema de Gestión de Reservas - Hotel JAL"
    page.scroll = "auto"
    # Alinear al inicio verticalmente
    page.vertical_alignment = ft.MainAxisAlignment.START
    # Alinear al inicio horizontalmente
    page.horizontal_alignment = ft.CrossAxisAlignment.START

    # Título del menú
    titulo_menu = ft.Text(
        "Gestión de Reservas",
        style="headlineMedium",
        color="blue",
        weight="bold",
        text_align="left"  # Alinear el texto a la izquierda
    )

    # Menú de navegación
    menu = ft.Container(
        content=ft.Column(
            [
                titulo_menu,  # Agregar el título al menú
                ft.Container(
                    content=ft.NavigationRail(
                        selected_index=0,
                        destinations=[
                            ft.NavigationRailDestination(
                                icon=ft.Icons.HOTEL, label="Habitaciones"),
                            ft.NavigationRailDestination(
                                icon=ft.Icons.BOOK_ONLINE, label="Reservas"),
                            ft.NavigationRailDestination(
                                icon=ft.Icons.ADD, label="Crear Cliente"),
                            ft.NavigationRailDestination(
                                icon=ft.Icons.PERSON, label="Consultar Cliente"),
                            ft.NavigationRailDestination(
                                icon=ft.Icons.CANCEL, label="Cancelar Reserva"),
                        ],
                        on_change=lambda e: [
                            habitacion_disponible(
                                page) if e.control.selected_index == 0 else None,
                            crear_reserva(
                                page) if e.control.selected_index == 1 else None,
                            crear_cliente(
                                page) if e.control.selected_index == 2 else None,
                            actualizar_cliente(
                                page) if e.control.selected_index == 3 else None,
                            eliminar_reserva(
                                page) if e.control.selected_index == 4 else None,
                        ],
                    ),
                    expand=True,  # Asegura que el NavigationRail ocupe todo el espacio disponible
                    height=page.height  # Define una altura fija para el contenedor
                ),
            ],
            expand=True  # Asegura que el menú ocupe todo el espacio disponible
        ),
        expand=True
    )

    # Agregar el menú y el contenedor de vistas a la página
    page.add(
        ft.Row(
            [
                # Define una altura fija para el menú
                ft.Container(content=menu, height=page.height),
                contenedor_vista,
            ],
            expand=True  # Asegura que el Row ocupe todo el espacio disponible
        )
    )


if __name__ == '__main__':
    ft.app(target=main)
    