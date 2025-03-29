import random
from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from .functions import *  # Импорт вспомогательных функций


# Модель для представления игрока (связь с пользователем Django)
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь один-к-одному с моделью User

    def __str__(self):
        return self.user.username  # Возвращает имя пользователя в строковом представлении


# Модель для представления класса персонажа
class CharacterClass(models.Model):
    name = models.CharField(verbose_name='Класс')  # Название класса
    hp_dice = models.IntegerField(verbose_name='Дайсы очков жизни')  # Количество очков жизни (кубик)
    saving_throws = models.CharField(verbose_name='Спасброски')  # Спасброски класса
    armor = models.TextField(verbose_name="Броня")  # Типы брони, доступные классу
    weapons = models.TextField(verbose_name='Оружие')  # Типы оружия, доступные классу
    tools = models.TextField(verbose_name='Инструменты')  # Инструменты, доступные классу
    spellcasting_ability = models.CharField(blank=True, verbose_name='Базовая характеристика')  # Характеристика для заклинаний
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='URL', unique=True)  # Уникальный URL для класса
    quantity_of_spells = models.JSONField(blank=True, null=True, verbose_name='Количество заклинаний от уровня')  # Количество заклинаний по уровням

    def __str__(self):
        return self.name  # Возвращает название класса

    def get_absolute_url(self):
        return reverse('class', kwargs={'class_slug': self.slug})  # Возвращает URL для деталей класса


# Модель для хранения информации о классе
class ClassInformation(models.Model):
    name = models.CharField(verbose_name='Название')  # Название информации
    character_class = models.OneToOneField(CharacterClass, on_delete=models.CASCADE, verbose_name='Класс',
                                           related_name='info')  # Связь с классом
    table = models.TextField(verbose_name="Таблица уровней", blank=True)  # Таблица уровней
    description = models.TextField(verbose_name='Описание')  # Описание класса


# Модель для представления расы персонажа
class Race(models.Model):
    name = models.CharField(verbose_name='Расса')  # Название расы
    size = models.FloatField(verbose_name='Размер')  # Размер расы
    speed = models.IntegerField(verbose_name='Скорость')  # Скорость передвижения
    weight = models.FloatField(verbose_name='Вес')  # Вес расы
    languages = models.CharField(max_length=255, blank=True, verbose_name='Языки')  # Языки, которые знает раса
    abilities = ArrayField(models.CharField(), blank=True, verbose_name='Способности')  # Способности расы
    abil_score_inc = models.JSONField(blank=True, null=True, verbose_name='Очки усиления')  # Бонусы к характеристикам
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='URL', unique=True)  # Уникальный URL для расы

    def __str__(self):
        return self.name  # Возвращает название расы

    def get_absolute_url(self):
        return reverse('race', kwargs={'race_slug': self.slug})  # Возвращает URL для деталей расы

    def get_purchase_features(self):
        return reverse('purchase_features', kwargs={'race_slug': self.slug})  # Возвращает URL для покупки характеристик


# Модель для хранения информации о расе
class RaceInformation(models.Model):
    name = models.CharField(verbose_name='Название')  # Название информации
    race = models.OneToOneField(Race, on_delete=models.CASCADE, verbose_name='Расса',
                                related_name='info')  # Связь с расой
    description = models.TextField(verbose_name="Описание")  # Описание расы


# Модель для представления заклинаний
class Spells(models.Model):
    name = models.CharField(verbose_name='Название')  # Название заклинания
    character_class = models.ManyToManyField(CharacterClass, related_name='spells', verbose_name='Класс')  # Классы, которые могут использовать заклинание
    level = models.IntegerField(verbose_name='Уровень', default=1)  # Уровень заклинания
    spell_type = models.CharField(verbose_name='Тип', default='Очарование')  # Тип заклинания
    time = models.CharField(verbose_name='Время накладывания', blank=True)  # Время накладывания
    distance = models.CharField(verbose_name="Дистанция", blank=True)  # Дистанция заклинания
    components = models.CharField(verbose_name='Компоненты', blank=True)  # Компоненты заклинания
    duration = models.CharField(verbose_name='Длительность', blank=True)  # Длительность заклинания
    description = models.TextField(verbose_name='Описание')  # Описание заклинания
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')  # Уникальный URL для заклинания

    def __str__(self):
        return self.name  # Возвращает название заклинания

    def get_absolute_url(self):
        return reverse('spell', kwargs={'spell_slug': self.slug})  # Возвращает URL для деталей заклинания


# Модель для представления навыков
class Skills(models.Model):
    name = models.CharField(verbose_name='Название')  # Название навыка
    about = models.TextField(verbose_name='Описание')  # Описание навыка
    character_class = models.ManyToManyField(CharacterClass, related_name='skills', verbose_name='Класс')  # Классы, которые могут использовать навык

    def __str__(self):
        return self.name  # Возвращает название навыка

    class Meta:
        ordering = ['name']  # Сортировка по названию


# Модель для представления оружия
class Weapons(models.Model):
    name = models.CharField(max_length=35, verbose_name='Название')  # Название оружия
    type = models.CharField(max_length=25, verbose_name='Тип')  # Тип оружия
    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Стоимость')  # Стоимость оружия
    damage = models.CharField(max_length=5, verbose_name='Урон')  # Урон оружия
    damage_type = models.CharField(max_length=25, verbose_name='Тип урона')  # Тип урона
    weight = models.IntegerField(verbose_name='Вес')  # Вес оружия
    property = models.JSONField(blank=True, null=True, verbose_name='Свойства')  # Свойства оружия
    description = models.TextField(verbose_name='Описание')  # Описание оружия

    def __str__(self):
        return self.name  # Возвращает название оружия

    def show_price(self):
        money = convert_money(self.price)  # Конвертация стоимости в монеты
        string = ""
        for m in money.keys():
            if money.get(m) != 0:
                string += str(money.get(m)) + ' ' + m  # Форматирование строки с ценой
        return string

    def get_absolute_url(self):
        return reverse('weapon', kwargs={'spell_id': self.pk})  # Возвращает URL для деталей оружия

    class Meta:
        ordering = ['name']  # Сортировка по названию


# Модель для представления брони
class Armor(models.Model):
    name = models.CharField(max_length=25, verbose_name='Название')  # Название брони
    type = models.CharField(max_length=35, verbose_name='Тип')  # Тип брони
    armor_class = models.CharField(verbose_name='Класс защиты')  # Класс защиты
    price = models.IntegerField(verbose_name='Стоимость')  # Стоимость брони
    weight = models.IntegerField(verbose_name='Вес')  # Вес брони
    stealth_interference = models.BooleanField(default=True, verbose_name='Помеха на Скрытность')  # Помеха на скрытность
    requirement_strength = models.IntegerField(verbose_name='Требование к Силе')  # Требование к силе
    on_off = models.CharField(verbose_name='Надевание/Снятие')  # Время надевания/снятия
    description = models.TextField(verbose_name='Описание')  # Описание брони

    def __str__(self):
        return self.name  # Возвращает название брони

    def show_price(self):
        money = convert_money(self.price)  # Конвертация стоимости в монеты
        string = ""
        for m in money.keys():
            if money.get(m) != 0:
                string += str(money.get(m)) + ' ' + m  # Форматирование строки с ценой
        return string

    def get_absolute_url(self):
        return reverse('armor', kwargs={'armor_id': self.pk})  # Возвращает URL для деталей брони

    class Meta:
        ordering = ['name']  # Сортировка по названию


# Модель для представления персонажа
class Character(models.Model):
    alignments = get_alignment_list()  # Список мировоззрений
    backgrounds = get_backgrounds_list()  # Список предысторий

    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE,
                                        related_name='character_class', verbose_name='Класс')  # Связь с классом
    race = models.ForeignKey(Race, on_delete=models.CASCADE,
                             related_name='character_race', verbose_name='Раса')  # Связь с расой
    character_name = models.CharField(max_length=25, verbose_name='Имя персонажа', blank=True, null=True)  # Имя персонажа
    background = models.CharField(max_length=25, verbose_name='Предыстория', blank=True, choices=backgrounds, null=True)  # Предыстория
    alignment = models.CharField(max_length=25, verbose_name='Мировоззрение', blank=True, choices=alignments, null=True)  # Мировоззрение
    player_name = models.CharField(max_length=25, verbose_name='Имя игрока', blank=True, null=True)  # Имя игрока
    level = models.IntegerField(validators=[MaxValueValidator(20), MinValueValidator(1)],
                                verbose_name='Уровень', default=1, null=True)  # Уровень персонажа
    experience = models.IntegerField(verbose_name='Опыт', default=1, null=True)  # Опыт персонажа
    characteristics = models.JSONField(blank=True, null=True, verbose_name='Характеристики')  # Характеристики персонажа
    modifiers = models.JSONField(blank=True, null=True, verbose_name='Модификаторы')  # Модификаторы характеристик
    proficiency_bonus = models.IntegerField(verbose_name='Бонус мастерства', default=2, blank=True, null=True)  # Бонус мастерства
    saving_throws = models.JSONField(verbose_name='Спасброски', blank=True, null=True)  # Спасброски
    skills = models.ManyToManyField(Skills, related_name='character', verbose_name='Навыки')  # Навыки персонажа
    spells = models.ManyToManyField(Spells, related_name='character', verbose_name='Заклинания')  # Заклинания персонажа
    money = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Деньги(медные монеты)",
                                default=random.randint(1, 4) * 3000, null=True)  # Деньги персонажа
    weapons = models.ManyToManyField(Weapons, related_name='character', verbose_name='Оружие', blank=True)  # Оружие персонажа
    armor = models.ManyToManyField(Armor, related_name='character', verbose_name='Доспехи', blank=True)  # Броня персонажа
    equipment = models.JSONField(verbose_name='Снаряжение', blank=True, null=True) # Снаряжение персонажа
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)  # Связь с игроком
    max_hp = models.IntegerField(default=0)  # Максимальное количество HP
    inventory_capacity = models.IntegerField(default=0)  # Вместимость инвентаря

    def get_absolute_url(self):
        return reverse('show_character', kwargs={'character_id': self.pk})  # Возвращает URL для деталей персонажа

    def get_coins(self):
        return convert_money(self.money)  # Возвращает деньги в виде монет

    def get_initiative(self):
        return calculate_initiative(self.modifiers)  # Возвращает инициативу персонажа

    def get_current_capacity(self):
        return count_current_capacity(self.weapons, self.armor, self.inventory_capacity)  # Возвращает текущую вместимость инвентаря

    def __str__(self):
        return self.character_name  # Возвращает имя персонажа
