# Generated by Django 4.0.1 on 2022-01-30 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_alter_profile_image'),
        ('lessonbank', '0007_lessonitem_new_word'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonbank',
            name='read_by',
            field=models.ManyToManyField(to='landing.Profile'),
        ),
    ]
