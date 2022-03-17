# Generated by Django 4.0.1 on 2022-02-03 03:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessonbank', '0018_remove_lessonbank_answered_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonassessment',
            name='appearances_in_tests',
            field=models.ManyToManyField(to='lessonbank.LessonBank'),
        ),
        migrations.AlterField(
            model_name='lessonbank',
            name='read_by',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]