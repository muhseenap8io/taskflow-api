from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

from taskflow_api.database.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user"
    )


class Task(Base):
    __tablename__="tasks"

    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column(String(100))
    description:Mapped[str|None]
    priority:Mapped[int]
    status: Mapped[str] = mapped_column(
    String(20),
    default="pending"
)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    user: Mapped["User"] = relationship(
        back_populates="tasks"
    )