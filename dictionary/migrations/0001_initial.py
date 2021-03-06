# Generated by Django 4.0.1 on 2022-01-29 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hsk', models.CharField(choices=[('HSK-1', 'HSK-1'), ('HSK-2', 'HSK-2')], default='HSK-1', max_length=10)),
                ('hanzi', models.CharField(max_length=50)),
                ('pinyin', models.CharField(max_length=50)),
                ('part_of_speech', models.CharField(max_length=50)),
                ('definition', models.CharField(max_length=255)),
                ('example', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
