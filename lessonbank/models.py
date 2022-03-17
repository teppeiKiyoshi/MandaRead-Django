from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class LessonBank(models.Model):
    hsk = models.PositiveIntegerField(default=1, null=False, blank=False, validators=[MinValueValidator(1), MaxValueValidator(2)])
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    read_by = models.ManyToManyField(User, blank=True)
    enable_table = models.BooleanField(default=True)

    def __str__(self):
        return "HSK" + str(self.hsk) + " " + self.title

class LessonAssessment(models.Model):
    QUESTION_TYPE = (
        ('Multiple Choice', 'Multiple Choice'),
        ('Fill in the Blanks', 'Fill in the Blanks'),
        ('True or False', 'True or False')
    )

    question_type = models.CharField(max_length=100, default='Multiple Choice', choices=QUESTION_TYPE)
    question = models.CharField(max_length=500, null=False, blank=False)
    choices = models.TextField(null=True, blank=True)
    answer = models.CharField(max_length=255)
    appearances_in_tests = models.ManyToManyField(LessonBank)

    def __str__(self):
        return self.question