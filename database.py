from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#DATABASE_URL = "postgresql+psycopg2://postgres:3489@localhost:5432/weather_db"
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/weather_mysql"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Успішно підключено до бази даних! Результат:", result.scalar())
except Exception as e:
    print("Помилка підключення:", e)