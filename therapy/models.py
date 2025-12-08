from datetime import datetime
from core.database import BASE
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Integer, Boolean

class Therapy(BASE):
    __tablename__ = "therapies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000))
    

    img_file: Mapped[str] = mapped_column(String(255), nullable=True)
    img_size: Mapped[str] = mapped_column(String(255), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)