import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import WeatherRecord, WindDirectionEnum

# Твоє підключення
DATABASE_URL = "postgresql+psycopg2://postgres:3489@localhost:5432/weather_db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def load_csv_to_db(csv_path):
    print(f"Зчитуємо дані з {csv_path}...")
    df = pd.read_csv(csv_path).where(pd.notnull(pd.read_csv(csv_path)), None)

    records_to_insert = []

    for index, row in df.iterrows():
        # Безпечна обробка дати
        try:
            last_upd = datetime.strptime(str(row.get('last_updated', '')), '%Y-%m-%d %H:%M')
        except (ValueError, TypeError):
            last_upd = datetime.now()

        # Безпечна обробка Enum (дефолт 'N' - Північ)
        try:
            raw_dir = row.get('wind_direction') or row.get('wind_dir') or 'N'
            wind_dir_val = str(raw_dir).upper()
            wind_dir = WindDirectionEnum(wind_dir_val)
        except ValueError:
            wind_dir = WindDirectionEnum.N

        # Створення запису на основі наявної ORM-моделі
        record = WeatherRecord(
            country=row.get('country', 'Unknown'),
            wind_degree=row.get('wind_degree', 0),
            wind_kph=row.get('wind_kph', 0.0),
            wind_direction=wind_dir,
            last_updated=last_upd,
            sunrise=row.get('sunrise', '06:00 AM')
        )

        records_to_insert.append(record)

        # Зберігаємо пачками по 1000 для швидкості
        if len(records_to_insert) >= 1000:
            session.bulk_save_objects(records_to_insert)
            session.commit()
            records_to_insert = []
            print(f"Завантажено {int(index) + 1} записів...")

    # Зберігаємо залишок
    if records_to_insert:
        session.bulk_save_objects(records_to_insert)
        session.commit()

    print("Всі дані успішно завантажено в базу PostgreSQL!")


if __name__ == "__main__":
    csv_file_path = "data/GlobalWeatherRepository-selected-columns.csv"
    load_csv_to_db(csv_file_path)