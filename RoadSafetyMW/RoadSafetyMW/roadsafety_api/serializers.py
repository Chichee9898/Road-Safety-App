from rest_framework import serializers
from .models import SafetyReport
from .models import RoadAlert
from .models import Report

class SafetyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyReport
        fields = '__all__'
        

class RoadAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadAlert
        fields = '__all__'
        
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['title', 'description', 'location', 'report_type']

