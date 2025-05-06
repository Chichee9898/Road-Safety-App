# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SafetyReportViewSet
from .views import RoadAlertList
from .views import ReportViewSet
from .views import submit_report
from .views import predict_flood_risk
from . import views
from .views import register_device_token

router = DefaultRouter()
router.register(r'reports', SafetyReportViewSet)
router.register(r'reports', ReportViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/road-alerts/', RoadAlertList.as_view(), name='road-alerts'),
    path('api/reports/', submit_report, name='submit_report'),
    path('api/report-trends/', views.report_trends),
    path('api/predict-flood-risk/', predict_flood_risk, name='predict_flood_risk'),
    path('api/safe-route/', views.safe_route_suggestion, name='safe_route'),
    path('api/register-token/', register_device_token),

    ]
