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
