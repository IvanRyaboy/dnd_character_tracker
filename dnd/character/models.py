import random

from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from .functions import convert_money, get_alignment_list, get_backgrounds_list


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CharacterClass(models.Model):
    name = models.CharField(verbose_name='Класс')
    hp_dice = models.IntegerField(verbose_name='Дайсы очков жизни')
    saving_throws = models.CharField(verbose_name='Спасброски')
    armor = models.TextField(verbose_name="Броня")
    weapons = models.TextField(verbose_name='Оружие')
    tools = models.TextField(verbose_name='Инструменты')
    spellcasting_ability = models.CharField(blank=True, verbose_name='Базовая характеристика')
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='URL', unique=True)
    quantity_of_spells = models.JSONField(blank=True, null=True, verbose_name='Количество заклинаний от уровня')

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


class Weapons(models.Model):
    name = models.CharField(max_length=35, verbose_name='Название')
    type = models.CharField(max_length=25, verbose_name='Тип')
    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Стоимость')
    damage = models.CharField(max_length=5, verbose_name='Урон')
    damage_type = models.CharField(max_length=25, verbose_name='Тип урона')
    weight = models.IntegerField(verbose_name='Вес')
    property = models.JSONField(blank=True, null=True, verbose_name='Свойства')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    def show_price(self):
        money = convert_money(self.price)
        string = ""
        for m in money.keys():
            if money.get(m) != 0:
                string += str(money.get(m)) + ' ' + m
        return string

    def get_absolute_url(self):
        return reverse('weapon', kwargs={'spell_id': self.pk})

    class Meta:
        ordering = ['name']


class Armor(models.Model):
    name = models.CharField(max_length=25, verbose_name='Название')
    type = models.CharField(max_length=35, verbose_name='Тип')
    armor_class = models.CharField(verbose_name='Класс защиты')
    price = models.IntegerField(verbose_name='Стоимость')
    weight = models.IntegerField(verbose_name='Вес')
    stealth_interference = models.BooleanField(default=True, verbose_name='Помеха на Скрытность')
    requirement_strength = models.IntegerField(verbose_name='Требование к Силе')
    on_off = models.CharField(verbose_name='Надевание/Снятие')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    def show_price(self):
        money = convert_money(self.price)
        string = ""
        for m in money.keys():
            if money.get(m) != 0:
                string += str(money.get(m)) + ' ' + m
        return string

    def get_absolute_url(self):
        return reverse('armor', kwargs={'armor_id': self.pk})

    class Meta:
        ordering = ['name']


class Character(models.Model):
    alignments = get_alignment_list()
    backgrounds = get_backgrounds_list()

    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE,
                                        related_name='character_class', verbose_name='Класс')
    race = models.ForeignKey(Race, on_delete=models.CASCADE,
                             related_name='character_race', verbose_name='Раса')
    character_name = models.CharField(max_length=25, verbose_name='Имя персонажа', blank=True, null=True)
    background = models.CharField(max_length=25, verbose_name='Предыстория', blank=True, choices=backgrounds, null=True)
    alignment = models.CharField(max_length=25, verbose_name='Мировоззрение', blank=True, choices=alignments, null=True)
    player_name = models.CharField(max_length=25, verbose_name='Имя игрока', blank=True, null=True)
    level = models.IntegerField(validators=[MaxValueValidator(20), MinValueValidator(1)],
                                verbose_name='Уровень', default=1, null=True)
    experience = models.IntegerField(verbose_name='Опыт', default=1, null=True)
    characteristics = models.JSONField(blank=True, null=True, verbose_name='Характеристики')
    modifiers = models.JSONField(blank=True, null=True, verbose_name='Модификаторы')
    proficiency_bonus = models.IntegerField(verbose_name='Бонус мастерства', default=2, blank=True, null=True)
    saving_throws = models.JSONField(verbose_name='Спасброски', blank=True, null=True)
    skills = models.ManyToManyField(Skills, related_name='character', verbose_name='Навыки', null=True)
    spells = models.ManyToManyField(Spells, related_name='character', verbose_name='Заклинания', null=True)
    money = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Деньги(медные монеты)",
                                default=random.randint(1, 4) * 3000, null=True)
    weapons = models.ManyToManyField(Weapons, related_name='character', verbose_name='Оружие', blank=True, null=True)
    armor = models.ManyToManyField(Armor, related_name='character', verbose_name='Доспехи', blank=True, null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('show_character', kwargs={'character_id': self.pk})

    def __str__(self):
        return self.character_name
