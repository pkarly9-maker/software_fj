"""Jerarquía de servicios ofrecidos por Software FJ."""
from abc import abstractmethod

from .entidades import Entidad
from .excepciones import ServicioInvalidoError, ServicioNoDisponibleError


class Servicio(Entidad):
    """Clase abstracta que representa un servicio genérico."""

    def __init__(self, nombre, precio_base, disponible=True):
        super().__init__()
        self.__nombre = self._validar_texto(nombre, "nombre")
        self.__precio_base = self._validar_precio(precio_base)
        self.__disponible = bool(disponible)

    # ---------- Validadores comunes ----------
    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ServicioInvalidoError(f"El {campo} es inválido.")
        return valor.strip()

    @staticmethod
    def _validar_precio(valor) -> float:
        try:
            precio = float(valor)
        except (TypeError, ValueError) as exc:
            raise ServicioInvalidoError(
                f"Precio base inválido: {valor!r}"
            ) from exc
        if precio <= 0:
            raise ServicioInvalidoError(
                "El precio base debe ser mayor que cero."
            )
        return precio

    # ---------- Propiedades ----------
    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def precio_base(self) -> float:
        return self.__precio_base

    @property
    def disponible(self) -> bool:
        return self.__disponible

    def habilitar(self):
        self.__disponible = True

    def deshabilitar(self):
        self.__disponible = False

    def _verificar_disponibilidad(self):
        if not self.__disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.nombre!r} no está disponible."
            )

    # ---------- Utilidad interna reutilizable ----------
    @staticmethod
    def _aplicar_impuesto_y_descuento(subtotal, impuesto, descuento) -> float:
        if not (0 <= descuento < 1):
            raise ServicioInvalidoError(
                "El descuento debe estar entre 0 y 1 (exclusivo)."
            )
        if impuesto < 0:
            raise ServicioInvalidoError("El impuesto no puede ser negativo.")
        return round(subtotal * (1 - descuento) * (1 + impuesto), 2)

    # ---------- Métodos abstractos (polimorfismo) ----------
    @abstractmethod
    def calcular_costo(self, duracion_horas, impuesto=0.0, descuento=0.0, **extras):
        """Calcula el costo del servicio.
        Es un método SOBRECARGADO por parámetros opcionales:
        variantes → solo horas / con impuesto / con descuento / con extras.
        """
        ...

    @abstractmethod
    def validar_parametros(self, **kwargs) -> bool:
        ...

    def describir(self) -> str:
        return (
            f"Servicio#{self.id} {self.nombre} "
            f"(base: ${self.precio_base:.2f}, disponible: {self.disponible})"
        )

    def __str__(self) -> str:
        return self.describir()


class ReservaSalas(Servicio):
    """Servicio de reserva de salas."""

    def __init__(self, nombre, precio_base, capacidad, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        self.__capacidad = self._validar_capacidad(capacidad)

    @staticmethod
    def _validar_capacidad(valor) -> int:
        try:
            cap = int(valor)
        except (TypeError, ValueError) as exc:
            raise ServicioInvalidoError(
                f"Capacidad inválida: {valor!r}"
            ) from exc
        if cap <= 0:
            raise ServicioInvalidoError(
                "La capacidad debe ser un entero positivo."
            )
        return cap

    @property
    def capacidad(self) -> int:
        return self.__capacidad

    def validar_parametros(self, **kwargs) -> bool:
        horas = kwargs.get("duracion_horas")
        if horas is None:
            raise ServicioInvalidoError(
                "Debe especificar la duración en horas."
            )
        try:
            h = float(horas)
        except (TypeError, ValueError) as exc:
            raise ServicioInvalidoError(
                "Duración inválida."
            ) from exc
        if h <= 0:
            raise ServicioInvalidoError("La duración debe ser positiva.")
        if h > 12:
            raise ServicioInvalidoError(
                "Las salas solo pueden reservarse hasta por 12 horas."
            )
        return True

    def calcular_costo(self, duracion_horas, impuesto=0.0, descuento=0.0, **extras):
        self._verificar_disponibilidad()
        self.validar_parametros(duracion_horas=duracion_horas)
        subtotal = self.precio_base * float(duracion_horas)
        if duracion_horas >= 5:
            subtotal *= 0.9  # descuento por uso prolongado
        return self._aplicar_impuesto_y_descuento(
            subtotal, impuesto, descuento
        )

    def describir(self) -> str:
        return (
            f"Reserva de Salas#{self.id} {self.nombre} "
            f"(capacidad {self.capacidad} personas)"
        )


class AlquilerEquipos(Servicio):
    """Servicio de alquiler de equipos."""

    def __init__(self, nombre, precio_base, tipo_equipo, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        self.__tipo_equipo = self._validar_texto(tipo_equipo, "tipo de equipo")

    @property
    def tipo_equipo(self) -> str:
        return self.__tipo_equipo

    def validar_parametros(self, **kwargs) -> bool:
        horas = kwargs.get("duracion_horas")
        if horas is None:
            raise ServicioInvalidoError(
                "Debe especificar la duración en horas."
            )
        try:
            h = float(horas)
        except (TypeError, ValueError) as exc:
            raise ServicioInvalidoError(
                "Duración inválida."
            ) from exc
        if h <= 0:
            raise ServicioInvalidoError("La duración debe ser positiva.")
        return True

    def calcular_costo(
        self, duracion_horas, impuesto=0.0, descuento=0.0, seguro=False, **extras
    ):
        self._verificar_disponibilidad()
        self.validar_parametros(duracion_horas=duracion_horas)
        subtotal = self.precio_base * float(duracion_horas)
        if seguro:
            subtotal += self.precio_base * 0.15
        return self._aplicar_impuesto_y_descuento(
            subtotal, impuesto, descuento
        )

    def describir(self) -> str:
        return (
            f"Alquiler de Equipos#{self.id} {self.nombre} "
            f"(tipo: {self.tipo_equipo})"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría especializada."""

    def __init__(self, nombre, precio_base, area, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        self.__area = self._validar_texto(area, "área")

    @property
    def area(self) -> str:
        return self.__area

    def validar_parametros(self, **kwargs) -> bool:
        horas = kwargs.get("duracion_horas")
        if horas is None:
            raise ServicioInvalidoError(
                "Debe especificar la duración en horas."
            )
        try:
            h = float(horas)
        except (TypeError, ValueError) as exc:
            raise ServicioInvalidoError(
                "Duración inválida."
            ) from exc
        if h <= 0:
            raise ServicioInvalidoError("La duración debe ser positiva.")
        if h > 8:
            raise ServicioInvalidoError(
                "Las asesorías no pueden exceder 8 horas."
            )
        return True

    def calcular_costo(
        self, duracion_horas, impuesto=0.0, descuento=0.0, urgente=False, **extras
    ):
        self._verificar_disponibilidad()
        self.validar_parametros(duracion_horas=duracion_horas)
        subtotal = self.precio_base * float(duracion_horas)
        if urgente:
            subtotal *= 1.25
        return self._aplicar_impuesto_y_descuento(
            subtotal, impuesto, descuento
        )

    def describir(self) -> str:
        return (
            f"Asesoría Especializada#{self.id} {self.nombre} "
            f"(área: {self.area})"
        )
    