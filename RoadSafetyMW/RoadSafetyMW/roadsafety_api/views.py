from rest_framework import viewsets
from .models import SafetyReport
from .serializers import SafetyReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RoadAlert
from .serializers import RoadAlertSerializer
from .models import Report
from .serializers import ReportSerializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import generics
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import JsonResponse
import joblib  # For loading model
import numpy as np
from rest_framework import status
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework import status
import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from pyfcm import FCMNotification

from .models import UserDeviceToken  # Your model for storing FCM tokens
from .models import UserDeviceToken



# Create your views here.

def send_push_notification_to_all(title, message):
    push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)

    # Get all tokens
    tokens = list(UserDeviceToken.objects.values_list('token', flat=True))

    if tokens:
        result = push_service.notify_multiple_devices(
            registration_ids=tokens,
            message_title=title,
            message_body=message
        )
        return result
    return None



@api_view(['POST'])
def safe_route_suggestion(request):
    # Extract data from request
    current_location = request.data.get('current_location')
    destination = request.data.get('destination')

    if not current_location or not destination:
        return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

    # Example logic: AI-based mock safer routes
    routes = [
        {"route": "Route A", "safety_score": 90, "duration": "15 mins"},
        {"route": "Route B", "safety_score": 75, "duration": "12 mins"},
        {"route": "Route C", "safety_score": 60, "duration": "10 mins"},
    ]

    # Choose top 2 safer routes
    safe_routes = sorted(routes, key=lambda x: x['safety_score'], reverse=True)[:2]

    return Response({"safe_routes": safe_routes})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_device_token(request):
    token = request.data.get('token')
    user = request.user

    if token:
        # Update if token already exists
        obj, created = UserDeviceToken.objects.update_or_create(
            user=user,
            defaults={'token': token}
        )
        return Response({'message': 'Token registered successfully'})
    return Response({'error': 'Token missing'}, status=400)

# Load once at import time
model = joblib.load('ml_models/flood_risk_model.pkl')

@api_view(['GET'])
@renderer_classes([JSONRenderer])  # ✅ Prevents HTML rendering
def road_alerts(request):
    alerts = RoadAlert.objects.all()
    serializer = RoadAlertSerializer(alerts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def predict_flood_risk(request):
    """
    Expects JSON:
      { "rainfall": float,
        "traffic":  float,
        "history":  float }
    Returns:
      { "risk_level": "Low"/"High", "code": 0/1 }
    """
    try:
        data = request.data
        rainfall = float(data.get('rainfall', 0))
        traffic  = float(data.get('traffic',  0))
        history  = float(data.get('history',  0))

        features = np.array([[rainfall, traffic, history]])
        prediction = model.predict(features)[0]

        # Map numeric output to label
        risk_map = {0: "Low", 1: "High"}
        return Response({
            "risk_level": risk_map[prediction],
            "code": int(prediction)
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def predict_flood_risk(request):
    try:
        # Expecting JSON body with keys: rainfall, traffic, history
        rainfall = float(request.data.get('rainfall', 0))
        traffic = float(request.data.get('traffic', 0))
        history = float(request.data.get('history', 0))

        # Make prediction
        features = np.array([[rainfall, traffic, history]])
        prediction = model.predict(features)[0]

        # Optional: Convert numeric prediction to string label
        risk_map = {0: "Low", 1: "Medium", 2: "High"}
        risk_level = risk_map.get(prediction, "Unknown")

        return Response({"risk_level": risk_level, "code": prediction})

    except Exception as e:
        return Response({"error": str(e)}, status=400)

def report_trends(request):
    trends = Report.objects.annotate(date=TruncDate('created_at')) \
        .values('date') \
        .annotate(count=Count('id')) \
        .order_by('date')
    
    return JsonResponse(list(trends), safe=False)

class SafetyReportViewSet(viewsets.ModelViewSet):
    queryset = SafetyReport.objects.all().order_by('-date_created')
    serializer_class = SafetyReportSerializer
    

class RoadAlertList(APIView):
    def get(self, request):
        alerts = RoadAlert.objects.all().order_by('-created_at')[:10]
        serializer = RoadAlertSerializer(alerts, many=True)
        return Response(serializer.data)

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-timestamp')
    serializer_class = ReportSerializer
    
@api_view(['POST'])
def submit_report(request):
    serializer = ReportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

class ReportCreateView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def create(self, request, *args, **kwargs):
        print("Incoming data:", request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("❌ Validation errors:", serializer.errors)  # <--- Add this
            return Response(serializer.errors, status=400)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
    

    
    

