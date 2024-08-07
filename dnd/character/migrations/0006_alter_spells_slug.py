# Generated by Django 5.0.7 on 2024-08-01 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0005_spells_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spells',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
    ]
