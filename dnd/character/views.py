from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import ListView
from .models import *

menu = [{'title': 'Классы', 'url_name': 'classes'},
        {'title': 'Рассы', 'url_name': 'races'},]


def main_menu(request):
    return render(request, 'character/index.html', {'menu': menu})


def classes(request):
    all_classes = CharacterClass.objects.all()
    return render(request, 'character/classes.html', {'classes': all_classes, 'menu': menu})


def races(request):
    all_races = Race.objects.all().order_by('name')
    return render(
        request, "character/races.html", {'races': all_races, 'menu': menu})


def spells(request):
    all_spells = Spells.objects.all().order_by('id')
    return render(
        request, 'character/spells.html', {'spells': all_spells, 'menu': menu})


def show_class(request, class_slug):
    character_class = get_object_or_404(CharacterClass, slug=class_slug)
    info = character_class.info

    context = {
        'class': character_class,
        'info': info,
        'title': character_class.name,
        'menu': menu,
    }
    return render(request, 'character/class.html', context=context)


def show_race(request, race_slug):
    race = get_object_or_404(Race, slug=race_slug)
    info = race.info

    context = {
        'race': race,
        'info': info,
        'title': race.name,
        'menu': menu
    }
    return render(request, 'character/race.html', context=context)


def show_spell(request, spell_slug):
    spell = get_object_or_404(Spells, slug=spell_slug)

    context = {
        'spell': spell,
        'title': spell.name,
        'menu': menu,
    }
    return render(request, 'character/spell.html', context=context)
