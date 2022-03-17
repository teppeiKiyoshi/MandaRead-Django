from django.db import models
from lessonbank.models import LessonBank

class Dictionary(models.Model):
    HSK_LEVEL = (
        ('HSK-1', 'HSK-1'),
        ('HSK-2', 'HSK-2')
    )
    PART_OF_SPEECH = (
        ('noun', 'noun'),
        ('pronoun', 'pronoun'),
        ('verb', 'verb'),
        ('adjective', 'adjective'),
        ('adverb', 'adverb'),
        ('preposition', 'preposition'),
        ('conjunction', 'conjunction'),
        ('interjection', 'interjection')
    )

    from_lesson = models.ForeignKey(LessonBank, null=True, blank=True, on_delete=models.CASCADE)
    hanzi = models.CharField(max_length=50)
    pinyin = models.CharField(max_length=50)
    definition = models.CharField(max_length=255)
    part_of_speech = models.CharField(max_length=50, null=True, blank=True, choices=PART_OF_SPEECH)
    example = models.CharField(null=True, blank=True, max_length=250)
    translation = models.CharField(null=True, blank=True, max_length=250)

    def __str__(self):
        return f"{self.hanzi} - {self.definition}"