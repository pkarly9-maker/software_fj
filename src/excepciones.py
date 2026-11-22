"""Jerarquía de excepciones personalizadas del sistema Software FJ."""


class SistemaFJError(Exception):
    """Excepción base. Todas las excepciones del dominio heredan de aquí."""
    pass


class ValidacionError(SistemaFJError):
    """Error genérico de validación de datos."""
    pass


class ParametroFaltanteError(ValidacionError):
    """Se lanza cuando falta un parámetro obligatorio."""
    pass


class ClienteInvalidoError(ValidacionError):
    """Datos del cliente inválidos."""
    pass


class ServicioInvalidoError(ValidacionError):
    """Datos del servicio inválidos."""
    pass


class ServicioNoDisponibleError(SistemaFJError):
    """El servicio está deshabilitado para reservas."""
    pass


class ReservaInvalidaError(SistemaFJError):
    """La reserva no cumple las reglas del negocio."""
    pass


class OperacionNoPermitidaError(SistemaFJError):
    """Se intenta una operación no permitida sobre el estado actual del objeto."""
    pass
