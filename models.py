import enum
from database import Base
from sqlalchemy import Column, Date, Enum, Float, Integer, String, Time


# Створюємо Python Enum для напрямку вітру (вимога завдання: enumeration)
class WindDirectionEnum(enum.Enum):
  N = "N"
  NNE = "NNE"
  NE = "NE"
  ENE = "ENE"
  E = "E"
  ESE = "ESE"
  SE = "SE"
  SSE = "SSE"
  S = "S"
  SSW = "SSW"
  SW = "SW"
  WSW = "WSW"
  W = "W"
  WNW = "WNW"
  NW = "NW"
  NNW = "NNW"
  VARIABLE = "Variable"


class WeatherRecord(Base):
  __tablename__ = "weather_records"

  id = Column(Integer, primary_key=True, index=True)
  country = Column(String(100), nullable=False)  # Текстова колонка
  last_updated = Column(Date, nullable=False)  # Колонка з датою
  sunrise = Column(Time, nullable=False)  # Колонка з часом

  # Колонки категорії "Вітер"
  wind_kph = Column(Float, nullable=False)  # Дробне число
  wind_degree = Column(Integer, nullable=False)  # Ціле число
  wind_direction = Column(
      Enum(WindDirectionEnum), nullable=False
  )  # Enum колонка
  wind_mph = Column(Float, nullable=True)
  gust_kph = Column(Float, nullable=True)