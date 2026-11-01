import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import WeatherRecord, WindRecord, WindDirectionEnum

#DATABASE_URL = "postgresql+psycopg2://postgres:3489@localhost:5432/weather_db"
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/weather_mysql"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def load_csv_to_db(csv_path):
    print(f"Зчитуємо реальні дані з {csv_path}...")

    df = pd.read_csv(
        csv_path,
        sep=None,
        engine="python",
        decimal=",",
        encoding="utf-8-sig",
    )


    df.columns = df.columns.str.strip().str.lower()

    print(df.columns.tolist())
    print(df.head())
    print(df.dtypes)

    df = df.astype(object).where(df.notnull(), None)

    required = ["country", "last_updated", "sunrise", "wind_degree",
                "wind_kph", "wind_mph", "wind_direction", "gust_mph", "gust_kph"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"У CSV немає колонок: {missing}. Є: {df.columns.tolist()}")

    records_to_insert = []


    for index, row in df.iterrows():
        # Дати
        try:
            last_upd = datetime.strptime(str(row.get('last_updated', '')), '%Y-%m-%d %H:%M')
        except (ValueError, TypeError):
            last_upd = datetime.now()

        try:
            raw_dir = row.get('wind_direction', 'N')
            wind_dir_val = str(raw_dir).upper()
            wind_dir = WindDirectionEnum(wind_dir_val)
        except ValueError:
            wind_dir = WindDirectionEnum.N

        wind_kph_val = float(row.get('wind_kph', 0.0) or 0.0)

        raw_sunrise = str(row.get('sunrise', '06:00 AM'))
        try:
            sunrise_time = datetime.strptime(raw_sunrise, '%I:%M %p').time()
        except ValueError:
            sunrise_time = datetime.strptime('06:00 AM', '%I:%M %p').time()

        weather = WeatherRecord(
            country=row.get('country', 'Unknown'),
            last_updated=last_upd,
            sunrise=sunrise_time
        )

        # 2. Створюємо запис для вітру і прив'язуємо до погоди
        wind = WindRecord(
            wind_degree=int(row.get('wind_degree', 0) or 0),
            wind_kph=wind_kph_val,
            wind_direction=wind_dir,
            wind_mph=float(row.get('wind_mph', 0.0) or 0.0),
            wind_gust_mph=float(row.get('gust_mph', 0.0) or 0.0),
            wind_gust_kph=float(row.get('gust_kph', 0.0) or 0.0),
            is_safe_to_go_outside=(wind_kph_val <= 36.0)  # Логіка для нової колонки
        )

        weather.wind = wind
        records_to_insert.append(weather)

        if len(records_to_insert) >= 1000:
            session.add_all(records_to_insert)
            session.commit()
            records_to_insert = []
            print(f"Завантажено {int(index) + 1} записів...")

    if records_to_insert:
        session.add_all(records_to_insert)
        session.commit()

    print("Всі дані завантажено в базу!")


if __name__ == "__main__":
    csv_file_path = "data/GlobalWeatherRepository.csv"
    load_csv_to_db(csv_file_path)