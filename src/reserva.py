"""Reserva: integra cliente, servicio y estado con manejo de excepciones."""
from enum import Enum

from .excepciones import (
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from .logger import log


class EstadoReserva(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"
    FALLIDA = "FALLIDA"


class Reserva:
    _contador = 0

    def __init__(
        self, cliente, servicio, duracion_horas,
        impuesto=0.0, descuento=0.0, **extras
    ):
        # --- Validaciones con parámetros faltantes ---
        if cliente is None:
            raise ParametroFaltanteError("Reserva requiere un cliente.")
        if servicio is None:
            raise ParametroFaltanteError("Reserva requiere un servicio.")
        try:
            horas = float(duracion_horas)
        except (TypeError, ValueError) as exc:
            raise ReservaInvalidaError(
                f"Duración inválida: {duracion_horas!r}"
            ) from exc
        if horas <= 0:
            raise ReservaInvalidaError("La duración debe ser positiva.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = horas
        self.impuesto = float(impuesto)
        self.descuento = float(descuento)
        self.extras = extras
        self.estado = EstadoReserva.PENDIENTE
        self.costo_total = 0.0

        Reserva._contador += 1
        self.id = Reserva._contador

    # ---------- Transiciones de estado ----------
    def confirmar(self) -> bool:
        if self.estado != EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado "
                f"{self.estado.value}."
            )
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.servicio.nombre!r} no está disponible."
            )
        self.estado = EstadoReserva.CONFIRMADA
        log.info(
            f"Reserva #{self.id} confirmada para {self.cliente.nombre}."
        )
        return True

    def procesar(self) -> float:
        if self.estado != EstadoReserva.CONFIRMADA:
            raise OperacionNoPermitidaError(
                "Solo se pueden procesar reservas confirmadas. "
                f"Estado actual: {self.estado.value}."
            )
        try:
            self.costo_total = self.servicio.calcular_costo(
                self.duracion_horas,
                impuesto=self.impuesto,
                descuento=self.descuento,
                **self.extras,
            )
        except Exception as exc:
            self.estado = EstadoReserva.FALLIDA
            log.error(f"Reserva #{self.id} falló al procesar: {exc}")
            # Encadenamiento de excepciones
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva #{self.id}."
            ) from exc
        else:
            self.estado = EstadoReserva.PROCESADA
            log.info(
                f"Reserva #{self.id} procesada. "
                f"Costo total: ${self.costo_total:.2f}"
            )
            return self.costo_total

    def cancelar(self) -> bool:
        if self.estado == EstadoReserva.PROCESADA:
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva ya procesada."
            )
        if self.estado == EstadoReserva.CANCELADA:
            raise OperacionNoPermitidaError(
                "La reserva ya está cancelada."
            )
        self.estado = EstadoReserva.CANCELADA
        log.info(f"Reserva #{self.id} cancelada.")
        return True

    def describir(self) -> str:
        return (
            f"Reserva#{self.id} | {self.cliente.nombre} -> "
            f"{self.servicio.nombre} | {self.duracion_horas}h | "
            f"estado={self.estado.value} | costo=${self.costo_total:.2f}"
        )

    def __str__(self) -> str:
        return self.describir()
    