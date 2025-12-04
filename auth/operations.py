from sqlalchemy import select
from auth.models import User, UserRole
from core.database import AsyncSessionLocal

async def create_new_user(
    username:str,
    email:str,
    password:str,
    role: UserRole
) -> User | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = select(User).where((User.username == username) | (User.email == email))
            result = await session.execute(stmt)
            existing_user = result.scalar_one_or_none()

            if existing_user:
                return None

            try:
                new_user = User()
                new_user.username = username
                new_user.email = email 
                new_user.set_password(password)
                new_user.role = role

                session.add(new_user)
                return new_user
            except:
                await session.rollback()
                return None


async def get_user(email:str) -> User | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            statement = select(User).where(User.email == email)
            result = await session.execute(statement)
            existing_user = result.scalar_one_or_none()

            if existing_user: return existing_user

            return None

async def get_user_by_id(id:int) -> User | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            statement = select(User).where(User.id == id)
            result = await session.execute(statement)
            existing_user = result.scalar_one_or_none()

            if existing_user: return existing_user

            return None