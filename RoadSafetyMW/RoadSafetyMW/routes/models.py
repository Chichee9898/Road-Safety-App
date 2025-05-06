from django.db import models

class Incident(models.Model):
    location_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    weather = models.CharField(max_length=100)
    incident_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
from django.db import models

# Create your models here.
