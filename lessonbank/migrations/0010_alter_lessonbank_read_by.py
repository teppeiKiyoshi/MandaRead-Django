# Generated by Django 4.0.1 on 2022-01-30 12:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessonbank', '0009_alter_lessonbank_read_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonbank',
            name='read_by',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
