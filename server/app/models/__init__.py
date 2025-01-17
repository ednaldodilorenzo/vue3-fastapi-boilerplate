# need access to this before importing models
from app.database import Base

from .usuario import Usuario
from .individuo import Individuo

__all__ = [
    "Base",
    "Usuario",
    "Individuo",
]
