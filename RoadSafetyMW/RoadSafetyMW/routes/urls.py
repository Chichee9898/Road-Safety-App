from django.urls import path
from .views import safe_routes

urlpatterns = [
    path('safe_routes/', safe_routes),
]

