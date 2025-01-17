import enum
from sqlalchemy import BigInteger, event
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Individuo(Base):
    __tablename__ = "individuo"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, index=True
    )
    nome: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    telefone: Mapped[str] = mapped_column(nullable=False)
    nascimento: Mapped[date] = mapped_column(nullable=False)
    apelido: Mapped[str] = mapped_column(nullable=False)
    cpf: Mapped[str] = mapped_column()
    extenso: Mapped[str] = mapped_column(nullable=False, server_default="")


@event.listens_for(Individuo, "before_insert")
@event.listens_for(Individuo, "before_update")
def before_individuo_changes(mapper, connection, target):
    target.filter = " ".join([target.nome, target.apelido, target.cpf, target.email])
