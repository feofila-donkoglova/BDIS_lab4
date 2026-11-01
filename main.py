from datetime import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import WeatherRecord, WindRecord

DATABASE_URL = "postgresql+psycopg2://postgres:3489@localhost:5432/weather_db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def search_weather():
    session = Session()
    print("\n=== Погодний пошуковий портал ===")
    country_input = input("Введіть назву країни (наприклад, Afghanistan, Ukraine): ").strip()
    date_input = input("Введіть дату у форматі YYYY-MM-DD (наприклад, 2024-05-16): ").strip()

    try:
        search_date = datetime.strptime(date_input, "%Y-%m-%d").date()
    except ValueError:
        print("Помилка: Неправильний формат дати! Використовуйте YYYY-MM-DD.")
        session.close()
        return

    # Робимо запит із JOIN обох таблиць, ігноруючи регістр (ilike) та порівнюючи лише дату (func.date)
    results = session.query(WeatherRecord, WindRecord).join(
        WindRecord, WeatherRecord.id == WindRecord.weather_id
    ).filter(
        WeatherRecord.country.ilike(f"%{country_input}%"),
        func.date(WeatherRecord.last_updated) == search_date
    ).all()

    if not results:
        print("\nПогоду за вашим запитом не знайдено.")
    else:
        print(f"\nЗнайдено записів: {len(results)}")
        for weather, wind in results:
            print("-" * 40)
            print(f"Країна: {weather.country}")
            print(f"Оновлено (повний час): {weather.last_updated}")
            print(f"Схід сонця: {weather.sunrise}")
            print(f"Швидкість вітру: {wind.wind_kph} км/год")
            print(f"Напрямок вітру: {wind.wind_direction.value}")

            safe_text = "Так, безпечно" if wind.is_safe_to_go_outside else "Ні, небезпечно!"
            print(f"Чи варто виходити на вулицю: {safe_text}")

    session.close()


if __name__ == "__main__":
    while True:
        search_weather()
        cont = input("\nШукати ще? (y/n): ")
        if cont.lower() != 'y':
            print("Роботу завершено.")
            break