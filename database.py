from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Явно вказуємо драйвер psycopg2, який у вас вже встановлено
DATABASE_URL = "postgresql+psycopg2://postgres:3489@localhost:5432/weather_db"

# Створюємо двигун для підключення до бази
engine = create_engine(DATABASE_URL)

# Фабрика сесій (через них ми будемо записувати/читати дані)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для наших майбутніх моделей таблиць
Base = declarative_base()


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


from sqlalchemy import text

# Спробуємо виконати простий запит для перевірки
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Успішно підключено до бази даних! Результат:", result.scalar())
except Exception as e:
    print("Помилка підключення:", e)