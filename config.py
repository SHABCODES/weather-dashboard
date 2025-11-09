import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'your_api_key_here')
    WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///weather.db')
    DEBUG = os.getenv('DEBUG', False)
