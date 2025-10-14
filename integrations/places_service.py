import requests
from django.conf import settings

class PlacesService:
    """Service for Google Places API integration"""
    
    def __init__(self):
        self.api_key = settings.GOOGLE_MAPS_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api/place"
    
    def search_nearby(self, latitude, longitude, radius=5000, place_type=None):
        """Search for nearby places"""
        if not self.api_key:
            return {"error": "Google Maps API key not configured"}
        
        try:
            url = f"{self.base_url}/nearbysearch/json"
            params = {
                'location': f"{latitude},{longitude}",
                'radius': radius,
                'key': self.api_key
            }
            if place_type:
                params['type'] = place_type
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_place_details(self, place_id):
        """Get details for a specific place"""
        if not self.api_key:
            return {"error": "Google Maps API key not configured"}
        
        try:
            url = f"{self.base_url}/details/json"
            params = {
                'place_id': place_id,
                'key': self.api_key
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}