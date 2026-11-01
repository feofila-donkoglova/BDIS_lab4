import enum
from sqlalchemy import Column, Integer, Float, String, DateTime, Time, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


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


class WindRecord(Base):
    __tablename__ = "wind_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    weather_id = Column(Integer, ForeignKey("weather_records.id", ondelete="CASCADE"), nullable=False, unique=True)

    # Всі колонки вітру переїхали сюди
    wind_degree = Column(Integer, nullable=False)
    wind_kph = Column(Float, nullable=False)
    wind_direction = Column(SQLEnum(WindDirectionEnum), nullable=False)
    wind_mph = Column(Float, nullable=True)
    wind_gust_mph = Column(Float, nullable=True)
    wind_gust_kph = Column(Float, nullable=True)

    weather = relationship("WeatherRecord", back_populates="wind")


class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False)
    last_updated = Column(DateTime, nullable=False)
    sunrise = Column(String(50), nullable=True)

    wind = relationship("WindRecord", back_populates="weather", uselist=False, cascade="all, delete-orphan")