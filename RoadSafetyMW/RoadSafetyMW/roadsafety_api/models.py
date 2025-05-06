from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserDeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"
    
class NotificationLog(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    sent_to = models.ManyToManyField(User, related_name='received_notifications')

    def __str__(self):
        return f"{self.title} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"   


class SafetyReport(models.Model):
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    severity = models.IntegerField()
    image = models.ImageField(upload_to='reports/')
    date_created = models.DateTimeField(auto_now_add=True)
    
    
# models.py
class RoadAlert(models.Model):
    location = models.CharField(max_length=255)
    description = models.TextField()
    alert_type = models.CharField(max_length=50)  # e.g., flood, accident
    created_at = models.DateTimeField(auto_now_add=True)
    

class Report(models.Model):
    REPORT_TYPES = [
        ('flood', 'Flood'),
        ('pothole', 'Pothole'),
        ('accident', 'Accident'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    confirmations = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.report_type} at {self.location}"


    