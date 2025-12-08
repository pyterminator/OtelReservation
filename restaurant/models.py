from datetime import datetime
from core.database import BASE
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, Boolean

class Restaurant(BASE):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000))

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)