import math
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView
from .models import *
from .forms import *

menu = [{'title': 'Классы', 'url_name': 'classes'},
        {'title': 'Рассы', 'url_name': 'races'},
        {'title': 'Заклинания', 'url_name': 'spells'},
        {'title': 'Создание персонажа', 'url_name': 'create_character'},
        {'title': 'Закуп характеристик', 'url_name': 'choose_race'}]


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


def create_character(request):
    race = Race.objects.all()
    character_class = CharacterClass.objects.all()
    if request.method == "POST":
        base_form = CharacterForm(request.POST, prefix='base')
        surviving_form = SurvivingForm(request.POST, prefix='surviving')
        if all([base_form.is_valid(), surviving_form.is_valid()]):
            return render(request, 'character/success.html')
    else:
        base_form = CharacterForm()
        surviving_form = SurvivingForm()

    context = {
        'race': race,
        'class': character_class,
        'title': 'Создание персонажа',
        'base_form': base_form,
        'surviving_form': surviving_form,
        'menu': menu,
    }
    return render(request, 'character/create_character.html', context=context)


def choose_race_for_features(request):
    races = Race.objects.all()

    context = {
        'menu': menu,
        'races': races
    }
    return render(request, "character/choose_race.html", context=context)


def purchase_features(request, race_slug):
    race_instance = get_object_or_404(Race, slug=race_slug)
    abil_score_inc_dict = race_instance.abil_score_inc

    strength = abil_score_inc_dict.get('Сила', 0)
    dexterity = abil_score_inc_dict.get('Ловкость', 0)
    physique = abil_score_inc_dict.get('Телосложение', 0)
    intelligence = abil_score_inc_dict.get('Интеллект', 0)
    wisdom = abil_score_inc_dict.get('Мудрость', 0)
    charisma = abil_score_inc_dict.get('Харизма', 0)

    if request.method == "POST":
        form = PurchaseForm(request.POST, prefix='form')
        if form.is_valid():
            total_strength = form.cleaned_data.get('strength', 8) + strength
            total_dexterity = form.cleaned_data.get('dexterity', 8) + dexterity
            total_physique = form.cleaned_data.get('physique', 8) + physique
            total_intelligence = form.cleaned_data.get('intelligence', 8) + intelligence
            total_wisdom = form.cleaned_data.get('wisdom', 8) + wisdom
            total_charisma = form.cleaned_data.get('charisma', 8) + charisma

            strength_mod = math.floor((total_strength - 10) / 2)
            dexterity_mod = math.floor((total_dexterity - 10) / 2)
            physique_mod = math.floor((total_physique - 10) / 2)
            intelligence_mod = math.floor((total_intelligence - 10) / 2)
            wisdom_mod = math.floor((total_wisdom - 10) / 2)
            charisma_mod = math.floor((total_charisma - 10) / 2)

            context = {
                'form': form,
                'total_strength': total_strength,
                'total_dexterity': total_dexterity,
                'total_physique': total_physique,
                'total_intelligence': total_intelligence,
                'total_wisdom': total_wisdom,
                'total_charisma': total_charisma,
                'strength_mod': strength_mod,
                'dexterity_mod': dexterity_mod,
                'physique_mod': physique_mod,
                'intelligence_mod': intelligence_mod,
                'wisdom_mod': wisdom_mod,
                'charisma_mod': charisma_mod,
                'strength': strength,
                'dexterity': dexterity,
                'physique': physique,
                'intelligence': intelligence,
                'wisdom': wisdom,
                'charisma': charisma,
            }

            return render(request, 'character/purchase_features.html', context=context)
    else:
        form = PurchaseForm(prefix='form')

    context = {
        'form': form,
        'total_strength': 8 + strength,
        'total_dexterity': 8 + dexterity,
        'total_physique': 8 + physique,
        'total_intelligence': 8 + intelligence,
        'total_wisdom': 8 + wisdom,
        'total_charisma': 8 + charisma,
        'strength_mod': math.floor(((8 + strength) - 10) / 2),
        'dexterity_mod': math.floor(((8 + dexterity) - 10) / 2),
        'physique_mod': math.floor(((8 + physique) - 10) / 2),
        'intelligence_mod': math.floor(((8 + intelligence) - 10) / 2),
        'wisdom_mod': math.floor(((8 + wisdom) - 10) / 2),
        'charisma_mod': math.floor(((8 + charisma) - 10) / 2),
        'strength': strength,
        'dexterity': dexterity,
        'physique': physique,
        'intelligence': intelligence,
        'wisdom': wisdom,
        'charisma': charisma,
    }

    return render(request, 'character/purchase_features.html', context=context)


def get_characteristics(request, class_slug):
    character_class = CharacterClass.objects.get(slug=class_slug)
    characteristics = character_class.characteristics  # Предполагается, что это JSON

    return JsonResponse(characteristics)
