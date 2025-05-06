
from django.http import JsonResponse
from .utils import predict_risk

# Create your views here.

def safe_routes(request):
    # You would use real-time or DB data in production
    routes = [
        {
            'start_lat': -13.97,
            'start_lng': 33.79,
            'end_lat': -13.98,
            'end_lng': 33.80,
            'weather': 'Rain',
            'incidents_nearby': 2
        },
        {
            'start_lat': -13.96,
            'start_lng': 33.78,
            'end_lat': -13.95,
            'end_lng': 33.77,
            'weather': 'Clear',
            'incidents_nearby': 0
        }
    ]

    response_data = []

    for route in routes:
        risk = predict_risk(route['weather'], route['incidents_nearby'])
        recommendation = "Avoid if possible" if risk == "high" else "Proceed with caution" if risk == "medium" else "Safe to travel"

        response_data.append({
            'startLat': route['start_lat'],
            'startLng': route['start_lng'],
            'endLat': route['end_lat'],
            'endLng': route['end_lng'],
            'risk_level': risk,
            'recommendation': recommendation
        })

    return JsonResponse({'routes': response_data})
