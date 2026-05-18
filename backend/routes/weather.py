"""
Weather API integration using OpenWeatherMap
"""
from flask import Blueprint, request, jsonify
import requests
import os

weather_bp = Blueprint('weather', __name__)

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5'

@weather_bp.route('/weather/current', methods=['GET'])
def get_current_weather():
    """Get current weather data by coordinates or city name"""
    
    if not OPENWEATHER_API_KEY:
        return jsonify({
            'error': 'OpenWeatherMap API key not configured',
            'hint': 'Set OPENWEATHER_API_KEY in .env file'
        }), 503
    
    # Get location parameters
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    city = request.args.get('city', '').strip()
    
    if not ((lat and lon) or city):
        return jsonify({
            'error': 'Either (lat, lon) or city parameter is required'
        }), 422
    
    try:
        # Build API request
        params = {
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'  # Celsius
        }
        
        if lat and lon:
            params['lat'] = lat
            params['lon'] = lon
        else:
            params['q'] = city
        
        # Call OpenWeatherMap API
        response = requests.get(
            f'{OPENWEATHER_BASE_URL}/weather',
            params=params,
            timeout=10
        )
        
        if response.status_code == 401:
            return jsonify({'error': 'Invalid API key'}), 503
        
        if response.status_code == 404:
            return jsonify({'error': 'Location not found'}), 404
        
        if response.status_code != 200:
            return jsonify({
                'error': 'Weather API request failed',
                'status': response.status_code
            }), 502
        
        data = response.json()
        
        # Extract relevant weather information
        weather_info = {
            'location': {
                'name': data.get('name', 'Unknown'),
                'country': data.get('sys', {}).get('country', ''),
                'lat': data.get('coord', {}).get('lat'),
                'lon': data.get('coord', {}).get('lon')
            },
            'weather': {
                'condition': data.get('weather', [{}])[0].get('main', 'Unknown'),
                'description': data.get('weather', [{}])[0].get('description', ''),
                'icon': data.get('weather', [{}])[0].get('icon', '')
            },
            'temperature': {
                'current': data.get('main', {}).get('temp'),
                'feels_like': data.get('main', {}).get('feels_like'),
                'min': data.get('main', {}).get('temp_min'),
                'max': data.get('main', {}).get('temp_max')
            },
            'humidity': data.get('main', {}).get('humidity'),
            'pressure': data.get('main', {}).get('pressure'),
            'wind': {
                'speed': data.get('wind', {}).get('speed'),
                'direction': data.get('wind', {}).get('deg')
            },
            'clouds': data.get('clouds', {}).get('all'),
            'visibility': data.get('visibility'),
            'rain': data.get('rain', {}).get('1h', 0),  # Rain volume for last 1 hour
            'timestamp': data.get('dt')
        }
        
        return jsonify(weather_info), 200
    
    except requests.Timeout:
        return jsonify({'error': 'Weather API request timed out'}), 504
    except requests.RequestException as e:
        return jsonify({'error': f'Weather API error: {str(e)}'}), 502
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@weather_bp.route('/weather/forecast', methods=['GET'])
def get_weather_forecast():
    """Get 5-day weather forecast"""
    
    if not OPENWEATHER_API_KEY:
        return jsonify({
            'error': 'OpenWeatherMap API key not configured'
        }), 503
    
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    city = request.args.get('city', '').strip()
    
    if not ((lat and lon) or city):
        return jsonify({
            'error': 'Either (lat, lon) or city parameter is required'
        }), 422
    
    try:
        params = {
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        
        if lat and lon:
            params['lat'] = lat
            params['lon'] = lon
        else:
            params['q'] = city
        
        response = requests.get(
            f'{OPENWEATHER_BASE_URL}/forecast',
            params=params,
            timeout=10
        )
        
        if response.status_code != 200:
            return jsonify({
                'error': 'Forecast API request failed',
                'status': response.status_code
            }), 502
        
        data = response.json()
        
        # Process forecast data
        forecast_list = []
        for item in data.get('list', []):
            forecast_list.append({
                'timestamp': item.get('dt'),
                'datetime': item.get('dt_txt'),
                'temperature': item.get('main', {}).get('temp'),
                'humidity': item.get('main', {}).get('humidity'),
                'weather': item.get('weather', [{}])[0].get('main'),
                'description': item.get('weather', [{}])[0].get('description'),
                'rain': item.get('rain', {}).get('3h', 0),
                'wind_speed': item.get('wind', {}).get('speed')
            })
        
        return jsonify({
            'location': {
                'name': data.get('city', {}).get('name'),
                'country': data.get('city', {}).get('country'),
                'lat': data.get('city', {}).get('coord', {}).get('lat'),
                'lon': data.get('city', {}).get('coord', {}).get('lon')
            },
            'forecast': forecast_list
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Forecast error: {str(e)}'}), 500
