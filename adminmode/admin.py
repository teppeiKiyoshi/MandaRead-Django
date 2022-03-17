from django.contrib import admin
from .models import UserLog, AchievementLog
from django.contrib.admin.models import LogEntry

admin.site.register(UserLog)
admin.site.register(AchievementLog)
admin.site.register(LogEntry)
