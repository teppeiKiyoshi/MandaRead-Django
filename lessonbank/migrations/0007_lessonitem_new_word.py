# Generated by Django 4.0.1 on 2022-01-30 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonbank', '0006_alter_lessonbank_hsk'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonitem',
            name='new_word',
            field=models.BooleanField(default=False),
        ),
    ]