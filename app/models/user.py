from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.core.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    routes: Mapped[list["Route"]] = relationship(
        "Route", back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User: {self.first_name}>"
