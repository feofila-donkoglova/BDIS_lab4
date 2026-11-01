from sqlalchemy import create_engine
from models import Base

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/weather_mysql"
engine = create_engine(DATABASE_URL)

print("Створюємо таблиці в MySQL...")
# Ця команда автоматично генерує схему БД на основі класів у models.py
Base.metadata.create_all(engine)
print("Таблиці успішно створено!")