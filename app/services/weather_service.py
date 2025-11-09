import requests
from config import Config

class WeatherService:
    def __init__(self):
        self.api_key = Config.WEATHER_API_KEY
        self.base_url = Config.WEATHER_BASE_URL
    
    def get_current_weather(self, city):
        """Fetch current weather data from API"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._transform_weather_data(data)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Weather API error: {str(e)}")
    
    def _transform_weather_data(self, api_data):
        """Transform API response to our format"""
        return {
            'city': api_data['name'],
            'country': api_data['sys']['country'],
            'temperature': api_data['main']['temp'],
            'feels_like': api_data['main']['feels_like'],
            'humidity': api_data['main']['humidity'],
            'pressure': api_data['main']['pressure'],
            'description': api_data['weather'][0]['description'],
            'wind_speed': api_data['wind']['speed']
        }