"""Entidades generales del sistema: Entidad abstracta y Cliente."""
from abc import ABC, abstractmethod
import re

from .excepciones import ClienteInvalidoError


class Entidad(ABC):
    """Clase abstracta raíz de todas las entidades del sistema."""

    _contador_global = 0

    def __init__(self):
        Entidad._contador_global += 1
        self._id = Entidad._contador_global

    @property
    def id(self) -> int:
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una representación legible de la entidad."""
        ...


class Cliente(Entidad):
    """Cliente con validaciones estrictas y atributos encapsulados."""

    _EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")
    _TEL_RE = re.compile(r"^\d{7,15}$")

    def __init__(self, nombre, email, telefono, documento=None):
        super().__init__()
        self.__nombre = self._validar_nombre(nombre)
        self.__email = self._validar_email(email)
        self.__telefono = self._validar_telefono(telefono)
        self.__documento = (
            documento.strip()
            if isinstance(documento, str) and documento.strip()
            else None
        )

    # ---------- Validadores (encapsulados) ----------
    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        if not isinstance(nombre, str):
            raise ClienteInvalidoError(
                f"El nombre debe ser texto; se recibió {type(nombre).__name__}."
            )
        nombre = nombre.strip()
        if len(nombre) < 3:
            raise ClienteInvalidoError(
                "El nombre debe tener al menos 3 caracteres."
            )
        return nombre

    @classmethod
    def _validar_email(cls, email: str) -> str:
        if not isinstance(email, str):
            raise ClienteInvalidoError("El email debe ser texto.")
        if not cls._EMAIL_RE.match(email):
            raise ClienteInvalidoError(f"Email inválido: {email!r}")
        return email.lower()

    @classmethod
    def _validar_telefono(cls, telefono) -> str:
        tel = str(telefono) if telefono is not None else ""
        if not cls._TEL_RE.match(tel):
            raise ClienteInvalidoError(f"Teléfono inválido: {telefono!r}")
        return tel

    # ---------- Propiedades (encapsulación) ----------
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        self.__nombre = self._validar_nombre(valor)

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str):
        self.__email = self._validar_email(valor)

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        self.__telefono = self._validar_telefono(valor)

    @property
    def documento(self):
        return self.__documento

    # ---------- Implementación del método abstracto ----------
    def describir(self) -> str:
        doc = f", doc: {self.__documento}" if self.__documento else ""
        return (
            f"Cliente#{self.id} {self.__nombre} <{self.__email}> "
            f"tel:{self.__telefono}{doc}"
        )

    def __str__(self) -> str:
        return self.describir()

    def __eq__(self, other) -> bool:
        return isinstance(other, Cliente) and self.__email == other.__email

    def __hash__(self) -> int:
        return hash(self.__email)
    