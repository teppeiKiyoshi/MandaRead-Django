# Generated by Django 4.0.1 on 2022-02-12 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessonbank', '0020_alter_lessonassessment_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonassessment',
            name='reading_type',
        ),
    ]