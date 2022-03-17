from django.db import models
from django.contrib.auth.models import User

class UserLog(models.Model):
    log_by = models.CharField(max_length=150)
    action = models.CharField(max_length=150)
    date_time_logged = models.DateTimeField()

    def __str__(self):
        return "\"" + self.log_by + "\" " + self.action

class AchievementLog(models.Model):
    ACHIEVEMENT_NAME = (
        ('Wheat of Prosperity', 'Wheat of Prosperity'),
        ('Terracota Helmet', 'Terracota Helmet'),
        ('Golden Konghou', 'Golden Konghou'),
        ('Lù Antlers', 'Lù Antlers'),
        ('Lost Coin of Shihuangdi', 'Lost Coin of Shihuangdi'),
    )

    achieved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.CharField(max_length=150, null=True, choices=ACHIEVEMENT_NAME)
    date_time_achieved = models.DateTimeField()

    def __str__(self):
        return "\"" + self.achieved_by.username + "\" has achieved \"" + self.achievement + "\""