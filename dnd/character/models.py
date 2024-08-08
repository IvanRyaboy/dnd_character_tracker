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
