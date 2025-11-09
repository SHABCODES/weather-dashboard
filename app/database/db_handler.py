from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.weather import Base, WeatherData
from config import Config
from datetime import datetime, timedelta

class DatabaseHandler:
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.create_tables()
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)
    
    def save_weather_data(self, weather_data):
        session = self.Session()
        try:
            # Check if recent data exists for this city
            existing = session.query(WeatherData).filter(
                WeatherData.city == weather_data['city']
            ).order_by(WeatherData.timestamp.desc()).first()
            
            # Save if no recent data or data is older than 10 minutes
            if not existing or self._should_update(existing.timestamp):
                weather_record = WeatherData(**weather_data)
                session.add(weather_record)
                session.commit()
                return weather_record
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_historical_data(self, city=None, limit=10):
        session = self.Session()
        try:
            query = session.query(WeatherData)
            if city:
                query = query.filter(WeatherData.city.ilike(f"%{city}%"))
            return query.order_by(WeatherData.timestamp.desc()).limit(limit).all()
        finally:
            session.close()
    
    def _should_update(self, last_timestamp):
        return datetime.utcnow() - last_timestamp > timedelta(minutes=10)