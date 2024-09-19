# Generated by Django 5.1 on 2024-09-17 11:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='characteristics',
            field=models.JSONField(blank=True, null=True, verbose_name='Характеристики'),
        ),
        migrations.AddField(
            model_name='character',
            name='modifiers',
            field=models.JSONField(blank=True, null=True, verbose_name='Модификаторы'),
        ),
        migrations.AlterField(
            model_name='character',
            name='alignment',
            field=models.CharField(blank=True, choices=[('lawful good', 'Упорядоченно добрый'), ('neutral good', 'Добрый'), ('chaotic good', 'Хаотично добрый'), ('lawful neutral', 'Упорядоченный'), ('true neutral', 'Истинно нейтральный'), ('chaotic neutral', 'Хаотичный'), ('lawful evil', 'Упорядоченно злой'), ('neutral evil', 'Злой'), ('chaotic evil', 'Хаотично злой'), ('unaligned', 'Вне мировоззрения')], max_length=25, verbose_name='Мировоззрение'),
        ),
        migrations.AlterField(
            model_name='character',
            name='background',
            field=models.CharField(blank=True, choices=[('artist', 'Артист'), ('homeless', 'Безпризорник'), ('noble', 'Благородный'), ('guild craftsman', 'Гидьдейский ремесленник'), ('sailor', 'Моряк'), ('sage', 'Мудрец'), ('folk hero', 'Народный герой'), ('hermit', 'Отшельник'), ('pirate', 'Пират'), ('criminal', 'Преступник'), ('soldier', 'Солдат'), ('foreigner', 'Чужеземец'), ('charlatan', 'Шарлатан')], max_length=25, verbose_name='Предыстория'),
        ),
        migrations.AlterField(
            model_name='character',
            name='experience',
            field=models.IntegerField(default=1, verbose_name='Опыт'),
        ),
        migrations.AlterField(
            model_name='character',
            name='level',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(1)], verbose_name='Уровень'),
        ),
    ]
