# Generated by Django 5.1 on 2024-09-27 10:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0009_armor_weapons'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='armor',
            field=models.ManyToManyField(blank=True, null=True, related_name='character', to='character.armor', verbose_name='Доспехи'),
        ),
        migrations.AddField(
            model_name='character',
            name='money',
            field=models.IntegerField(default=60, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Деньги(медные монеты)'),
        ),
        migrations.AddField(
            model_name='character',
            name='weapons',
            field=models.ManyToManyField(blank=True, null=True, related_name='character', to='character.weapons', verbose_name='Оружие'),
        ),
        migrations.AlterField(
            model_name='armor',
            name='armor_class',
            field=models.CharField(verbose_name='Класс защиты'),
        ),
    ]
