class ReservaContext:
    habita_seleccionado = ""

reserva_context = ReservaContext()

def habitacion_seleccionada(num_habitacion):
    reserva_context.habita_seleccionado = num_habitacion