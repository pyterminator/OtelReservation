import enum
from sqlalchemy import Enum
from core.database import BASE
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, DateTime
from utils.hashing import Hash

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(BASE):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    _password: Mapped[str] = mapped_column("password", String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    # updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    def set_password(self, raw_password: str):
        self._password = Hash.encrypt(raw_password)

    @property
    def password(self):
        raise AttributeError("Password field is write-only.")

    def check_password(self, raw_password: str) -> bool:
        return Hash.verify(raw_password, self._password)