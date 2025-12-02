import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contact.models import BASE

load_dotenv()

DB_HOST: str = os.getenv("DB_HOST")
DB_PORT: int = os.getenv("DB_PORT")
DB_USER: str = os.getenv("DB_USER")
DB_NAME: str = os.getenv("DB_NAME")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
BASE.metadata.create_all(bind=engine)


session = sessionmaker(
    bind=engine,
    autoflush=True
)

db_session = session()

# try:
#     connection = engine.connect()
#     connection.close()
#     print("ping, connected")
# except Exception as e:
#     print(e)