from flask import Blueprint, request, jsonify
from app.services.weather_service import WeatherService
from app.database.db_handler import DatabaseHandler

api_bp = Blueprint('api', __name__)
weather_service = WeatherService()
db_handler = DatabaseHandler()

@api_bp.route('/weather/current', methods=['GET'])
def get_current_weather():
    """Get current weather for a city"""
    city = request.args.get('city')
    
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    
    try:
        # Get fresh data from API
        weather_data = weather_service.get_current_weather(city)
        
        # Save to database
        db_handler.save_weather_data(weather_data)
        
        return jsonify(weather_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/weather/history', methods=['GET'])
def get_weather_history():
    """Get historical weather data"""
    city = request.args.get('city')
    limit = request.args.get('limit', 10, type=int)
    
    try:
        historical_data = db_handler.get_historical_data(city, limit)
        return jsonify([data.to_dict() for data in historical_data])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/weather/summary', methods=['GET'])
def get_weather_summary():
    """Get weather summary for multiple cities"""
    cities = request.args.get('cities', '')
    
    if not cities:
        return jsonify({'error': 'Cities parameter is required'}), 400
    
    city_list = [city.strip() for city in cities.split(',')]
    summaries = []
    
    for city in city_list[:5]:  # Limit to 5 cities
        try:
            weather_data = weather_service.get_current_weather(city)
            db_handler.save_weather_data(weather_data)
            summaries.append(weather_data)
        except Exception as e:
            summaries.append({'city': city, 'error': str(e)})
    
    return jsonify(summaries)