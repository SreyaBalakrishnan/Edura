"""
Custom CORS Middleware for Django 3.0 compatibility
"""
from django.http import HttpResponse


class CustomCORSMiddleware:
    """
    Custom CORS middleware that works with Django 3.0
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add CORS headers for OPTIONS requests (preflight)
        if request.method == 'OPTIONS':
            response = HttpResponse()
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response['Access-Control-Max-Age'] = '3600'
            return response

        # Get the response from the next middleware/view
        response = self.get_response(request)

        # Add CORS headers to all responses
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        return response
