from .models import *
from django.contrib import admin


@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ClassInformation)
class ClassInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['name']


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(RaceInformation)
class RaceInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['name']


@admin.register(Spells)
class SpellsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['name']
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
    ordering = ['id']


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['name']


@admin.register(Weapons)
class WeaponsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['type', 'name']


@admin.register(Armor)
class ArmorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['type']
