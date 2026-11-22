"""Punto de entrada: simulación de 14 operaciones completas.

Demuestra try/except, try/except/else, try/except/finally y
encadenamiento de excepciones en un escenario real.
"""
from src.sistema import SistemaIntegral
from src.entidades import Cliente
from src.servicios import (
    AlquilerEquipos,
    AsesoriaEspecializada,
    ReservaSalas,
)
from src.excepciones import (
    ClienteInvalidoError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)
from src.logger import log


SEPARADOR = "-" * 70


def _encabezado(titulo: str):
    print(f"\n{SEPARADOR}\n>> {titulo}\n{SEPARADOR}")


def main() -> None:
    print("=" * 70)
    print(" SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ ".center(70, "="))
    print("=" * 70)

    sistema = SistemaIntegral()

    # ================= OPERACIONES CON CLIENTES =================
    _encabezado("Operaciones con CLIENTES")

    # OP 1: cliente válido
    try:
        ana = Cliente("Ana Torres", "ana@example.com", "3001234567", "CC123")
        sistema.registrar_cliente(ana)
        print(f"[OP1 OK]   {ana}")
    except ClienteInvalidoError as e:
        log.error(f"OP1 falló: {e}")

    # OP 2: cliente inválido (nombre corto)
    try:
        malo = Cliente("Lu", "lu@example.com", "3001112222")
        sistema.registrar_cliente(malo)
    except ClienteInvalidoError as e:
        print(f"[OP2 FAIL] Rechazado por validación: {e}")

    # OP 3: cliente válido
    try:
        carlos = Cliente("Carlos Pérez", "carlos@example.com", "3109998888")
        sistema.registrar_cliente(carlos)
        print(f"[OP3 OK]   {carlos}")
    except ClienteInvalidoError as e:
        log.error(f"OP3 falló: {e}")

    # OP 4: email inválido
    try:
        Cliente("Pedro Ruiz", "correo-malo", "3000000000")
    except ClienteInvalidoError as e:
        print(f"[OP4 FAIL] {e}")

    # ================= OPERACIONES CON SERVICIOS =================
    _encabezado("Operaciones con SERVICIOS")

    # OP 5: sala válida
    try:
        sala = ReservaSalas("Sala Ejecutiva", 50000, 12)
        sistema.agregar_servicio(sala)
        print(f"[OP5 OK]   {sala}")
    except ServicioInvalidoError as e:
        log.error(f"OP5 falló: {e}")

    # OP 6: equipo válido
    try:
        equipo = AlquilerEquipos("Proyector 4K", 30000, "Video")
        sistema.agregar_servicio(equipo)
        print(f"[OP6 OK]   {equipo}")
    except ServicioInvalidoError as e:
        log.error(f"OP6 falló: {e}")

    # OP 7: asesoría válida
    try:
        asesoria = AsesoriaEspecializada("Consultoría Cloud", 120000, "TI")
        sistema.agregar_servicio(asesoria)
        print(f"[OP7 OK]   {asesoria}")
    except ServicioInvalidoError as e:
        log.error(f"OP7 falló: {e}")

    # OP 8: servicio con precio inválido
    try:
        ReservaSalas("Sala Fantasma", -100, 5)
    except ServicioInvalidoError as e:
        print(f"[OP8 FAIL] {e}")

    # ================= OPERACIONES CON RESERVAS =================
    _encabezado("Operaciones con RESERVAS")

    # OP 9: reserva exitosa (confirmar + procesar)  → try/except/else
    try:
        r9 = sistema.crear_reserva(ana, sala, 6, impuesto=0.19, descuento=0.05)
    except ReservaInvalidaError as e:
        print(f"[OP9 FAIL] {e}")
    else:
        r9.confirmar()
        r9.procesar()
        print(f"[OP9 OK]   {r9}")

    # OP 10: servicio deshabilitado → ServicioNoDisponibleError
    try:
        asesoria.deshabilitar()
        r10 = sistema.crear_reserva(carlos, asesoria, 2)
        r10.confirmar()
        r10.procesar()
    except ServicioNoDisponibleError as e:
        print(f"[OP10 FAIL] {e}")
    finally:
        asesoria.habilitar()

    # OP 11: duración negativa → ReservaInvalidaError
    try:
        sistema.crear_reserva(ana, equipo, -3)
    except ReservaInvalidaError as e:
        print(f"[OP11 FAIL] {e}")

    # OP 12: procesar sin confirmar → OperacionNoPermitidaError
    try:
        r12 = sistema.crear_reserva(carlos, equipo, 4, seguro=True)
        r12.procesar()  # aún en PENDIENTE
    except OperacionNoPermitidaError as e:
        print(f"[OP12 FAIL] {e}")

    # OP 13: cancelación y doble cancelación
    try:
        r13 = sistema.crear_reserva(ana, equipo, 2)
        r13.cancelar()
        print(f"[OP13 OK]   {r13}")
        r13.cancelar()  # segunda vez → error
    except OperacionNoPermitidaError as e:
        print(f"[OP13 FAIL] {e}")

    # OP 14: cliente no registrado → ReservaInvalidaError
    try:
        fantasma = Cliente("Fantasma Test", "fantasma@test.com", "3000000001")
        sistema.crear_reserva(fantasma, sala, 3)
    except ReservaInvalidaError as e:
        print(f"[OP14 FAIL] {e}")

    # ================= RESUMEN FINAL =================
    _encabezado("RESUMEN DEL SISTEMA")
    for k, v in sistema.resumen().items():
        print(f"  {k:<12}: {v}")

    print("\n  Reservas registradas:")
    for r in sistema.reservas:
        print(f"    · {r}")

    print(f"\n  Log de eventos: logs/sistema.log")
    print(f"  Ejecución finalizada correctamente.\n")


if __name__ == "__main__":
    main()