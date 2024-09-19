from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField, JSONField
from .functions import get_alignment_list, get_backgrounds_list


class CharacterClass(models.Model):
    name = models.CharField(verbose_name='Класс')
    hp_dice = models.IntegerField(verbose_name='Дайсы очков жизни')
    saving_throws = models.CharField(verbose_name='Спасброски')
    armor = models.TextField(verbose_name="Броня")
    weapons = models.TextField(verbose_name='Оружие')
    tools = models.TextField(verbose_name='Инструменты')
    spellcasting_ability = models.CharField(blank=True, verbose_name='Базовая характеристика')
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

    def get_purchase_features(self):
        return reverse('purchase_features', kwargs={'race_slug': self.slug})


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


class Skills(models.Model):
    name = models.CharField(verbose_name='Название')
    about = models.TextField(verbose_name='Описание')
    character_class = models.ManyToManyField(CharacterClass, related_name='skills', verbose_name='Класс')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Character(models.Model):
    alignments = get_alignment_list()
    backgrounds = get_backgrounds_list()

    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE,
                                        related_name='character_class', verbose_name='Класс')
    race = models.ForeignKey(Race, on_delete=models.CASCADE,
                             related_name='character_race', verbose_name='Раса')
    character_name = models.CharField(max_length=25, verbose_name='Имя персонажа', blank=True)
    background = models.CharField(max_length=25, verbose_name='Предыстория', blank=True, choices=backgrounds)
    alignment = models.CharField(max_length=25, verbose_name='Мировоззрение', blank=True, choices=alignments)
    player_name = models.CharField(max_length=25, verbose_name='Имя игрока', blank=True)
    level = models.IntegerField(validators=[MaxValueValidator(20), MinValueValidator(1)],
                                verbose_name='Уровень', default=1)
    experience = models.IntegerField(verbose_name='Опыт', default=1)
    characteristics = models.JSONField(blank=True, null=True, verbose_name='Характеристики')
    modifiers = models.JSONField(blank=True, null=True, verbose_name='Модификаторы')
    proficiency_bonus = models.IntegerField(verbose_name='Бонус мастерства', default=2, blank=True)
    saving_throws = models.JSONField(verbose_name='Спасброски', blank=True, null=True)
    skills = models.ManyToManyField(Skills, related_name='character', verbose_name='Навыки')
    spells = models.ManyToManyField(Spells, related_name='character', verbose_name='Заклинания')

    def get_absolute_url(self):
        return reverse('show_character', kwargs={'character_id': self.pk})
