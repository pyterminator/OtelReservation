from datetime import datetime
from core.database import BASE
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Integer, Boolean

class Contact(BASE):
    __tablename__ = "contact_form"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None] = mapped_column(String(60), nullable=True)
    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(17))
    message: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)