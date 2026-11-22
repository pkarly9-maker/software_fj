"""Configuración centralizada del logger del sistema."""
import logging
import os
from logging.handlers import RotatingFileHandler

_FORMATO = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def obtener_logger(nombre: str = "software_fj") -> logging.Logger:
    logger = logging.getLogger(nombre)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    os.makedirs("logs", exist_ok=True)

    fh = RotatingFileHandler(
        "logs/sistema.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    fh.setFormatter(_FORMATO)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setFormatter(_FORMATO)
    ch.setLevel(logging.WARNING)  # solo warnings/errores al stdout

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


log = obtener_logger()
