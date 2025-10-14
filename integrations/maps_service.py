import requests
from django.conf import settings

class MapsService:
    """Service for Google Maps API integration"""
    
    def __init__(self):
        self.api_key = settings.GOOGLE_MAPS_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api"
    
    def geocode_address(self, address):
        """Convert address to latitude/longitude"""
        if not self.api_key:
            return {"error": "Google Maps API key not configured"}
        
        try:
            url = f"{self.base_url}/geocode/json"
            params = {
                'address': address,
                'key': self.api_key
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                location = data['results'][0]['geometry']['location']
                return {
                    'latitude': location['lat'],
                    'longitude': location['lng'],
                    'formatted_address': data['results'][0]['formatted_address']
                }
            return {"error": "Location not found"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_distance(self, origin, destination):
        """Calculate distance between two locations"""
        if not self.api_key:
            return {"error": "Google Maps API key not configured"}
        
        try:
            url = f"{self.base_url}/distancematrix/json"
            params = {
                'origins': origin,
                'destinations': destination,
                'key': self.api_key
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}