from django.contrib import admin
from .models import Report
from .models import NotificationLog

admin.site.register(Report)

# admin.py
# Register your models here.


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('title', 'sent_at')
    filter_horizontal = ('sent_to',)


