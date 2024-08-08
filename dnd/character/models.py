from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField, JSONField


class CharacterClass(models.Model):
    name = models.CharField(verbose_name='Класс')
    hp_dice = models.IntegerField(verbose_name='Дайсы очков жизни')
    saving_throws = models.CharField(verbose_name='Спасброски')
    armor = models.TextField(verbose_name="Броня")
    weapons = models.TextField(verbose_name='Оружие')
    tools = models.TextField(verbose_name='Инструменты')
    skills = ArrayField(models.CharField(), blank=True, verbose_name='Навыки')
    spellcasting_ability = models.CharField(blank=True)
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='URL', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('class', kwargs={'class_slug': self.slug})


class ClassInformation(models.Model):
    name = models.CharField(verbose_name='Название')
    character_class = models.OneToOneField(CharacterClass, on_delete=models.CASCADE, verbose_name='Класс',
                                           related_name='info')
    table = models.TextField(verbose_name="Таблица уровней", blank=True)
    description = models.TextField(verbose_name='Описание')


class Race(models.Model):
    name = models.CharField(verbose_name='Расса')
    size = models.FloatField(verbose_name='Размер')
    speed = models.FloatField(verbose_name='Скорость')
    weight = models.FloatField(verbose_name='Вес')
    languages = models.CharField(max_length=255, blank=True, verbose_name='Языки')
    abilities = ArrayField(models.CharField(), blank=True, verbose_name='Способности')
    abil_score_inc = models.JSONField(blank=True, null=True, verbose_name='Очки усиления')
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='URL', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('race', kwargs={'race_slug': self.slug})


class RaceInformation(models.Model):
    name = models.CharField(verbose_name='Название')
    race = models.OneToOneField(Race, on_delete=models.CASCADE, verbose_name='Расса',
                                related_name='info')
    description = models.TextField(verbose_name="Описание")


class Spells(models.Model):
    name = models.CharField(verbose_name='Название')
    character_class = models.ManyToManyField(CharacterClass, related_name='spells', verbose_name='Класс')
    level = models.IntegerField(verbose_name='Уровень', default=1)
    spell_type = models.CharField(verbose_name='Тип', default='Очарование')
    time = models.CharField(verbose_name='Время накладывания', blank=True)
    distance = models.CharField(verbose_name="Дистанция", blank=True)
    components = models.CharField(verbose_name='Компоненты', blank=True)
    duration = models.CharField(verbose_name='Длительность', blank=True)
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('spell', kwargs={'spell_slug': self.slug})
