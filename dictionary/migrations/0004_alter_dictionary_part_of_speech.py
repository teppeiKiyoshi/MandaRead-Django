# Generated by Django 4.0.1 on 2022-01-31 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0003_alter_dictionary_part_of_speech'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionary',
            name='part_of_speech',
            field=models.CharField(blank=True, choices=[('noun', 'noun'), ('pronoun', 'pronoun'), ('verb', 'verb'), ('adjective', 'adjective'), ('adverb', 'adverb'), ('preposition', 'preposition'), ('conjunction', 'conjunction'), ('interjection', 'interjection')], max_length=50, null=True),
        ),
    ]
