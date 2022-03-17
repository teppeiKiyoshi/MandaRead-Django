from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ACHIEVEMENT_NAME = (
        ('Wheat of Prosperity', 'Wheat of Prosperity'),
        ('Terracota Helmet', 'Terracota Helmet'),
        ('Golden Konghou', 'Golden Konghou'),
        ('Lù Antlers', 'Lù Antlers'),
        ('Lost Coin of Shihuangdi', 'Lost Coin of Shihuangdi'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    lessons_25 = models.BooleanField(default=False)
    lessons_50 = models.BooleanField(default=False)
    lessons_100 = models.BooleanField(default=False)
    assessment_perfected = models.BooleanField(default=False)
    mock_perfected = models.BooleanField(default=False)
    

    def __str__(self):
        return f'{self.user.username} Profile'