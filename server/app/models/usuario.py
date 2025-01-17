from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

# from sqlalchemy.ext.asyncio import AsyncAttrs


from . import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, index=True
    )
    username: Mapped[str] = mapped_column(index=True, unique=True)
    senha: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    papel: Mapped[str] = mapped_column(nullable=False)
    ativo: Mapped[bool] = mapped_column(nullable=False, default=True)
