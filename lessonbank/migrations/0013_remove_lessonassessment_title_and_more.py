# Generated by Django 4.0.1 on 2022-02-01 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonbank', '0012_alter_lessonbank_hsk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonassessment',
            name='title',
        ),
        migrations.AddField(
            model_name='lessonassessment',
            name='appearances_in_tests',
            field=models.ManyToManyField(null=True, to='lessonbank.LessonBank'),
        ),
    ]