"""SistemaIntegral: gestiona clientes, servicios y reservas en memoria."""
from .excepciones import (
    ClienteInvalidoError,
    ReservaInvalidaError,
)
from .logger import log
from .reserva import EstadoReserva, Reserva


class SistemaIntegral:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    # ---------- Clientes ----------
    def registrar_cliente(self, cliente):
        if any(c.email == cliente.email for c in self.clientes):
            raise ClienteInvalidoError(
                f"Ya existe un cliente con email {cliente.email}"
            )
        self.clientes.append(cliente)
        log.info(f"Cliente registrado: {cliente.describir()}")
        return cliente

    # ---------- Servicios ----------
    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)
        log.info(f"Servicio agregado: {servicio.describir()}")
        return servicio

    # ---------- Reservas ----------
    def crear_reserva(
        self, cliente, servicio, duracion_horas,
        impuesto=0.0, descuento=0.0, **extras
    ) -> Reserva:
        if cliente not in self.clientes:
            raise ReservaInvalidaError(
                "El cliente no está registrado en el sistema."
            )
        if servicio not in self.servicios:
            raise ReservaInvalidaError(
                "El servicio no pertenece al catálogo del sistema."
            )
        reserva = Reserva(
            cliente, servicio, duracion_horas,
            impuesto, descuento, **extras,
        )
        self.reservas.append(reserva)
        log.info(f"Reserva creada: {reserva.describir()}")
        return reserva

    def procesar_todas(self):
        for r in self.reservas:
            try:
                r.confirmar()
                r.procesar()
            except Exception as exc:
                log.warning(
                    f"Reserva #{r.id} no procesada: {exc}"
                )

    # ---------- Reporte ----------
    def resumen(self) -> dict:
        return {
            "clientes": len(self.clientes),
            "servicios": len(self.servicios),
            "reservas": len(self.reservas),
            "procesadas": sum(
                1 for r in self.reservas
                if r.estado == EstadoReserva.PROCESADA
            ),
            "canceladas": sum(
                1 for r in self.reservas
                if r.estado == EstadoReserva.CANCELADA
            ),
            "fallidas": sum(
                1 for r in self.reservas
                if r.estado == EstadoReserva.FALLIDA
            ),
        }
    