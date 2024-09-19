import math
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
import json
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView
from .models import *
from .forms import *

menu = [{'title': 'Классы', 'url_name': 'classes'},
        {'title': 'Рассы', 'url_name': 'races'},
        {'title': 'Заклинания', 'url_name': 'spells'},]


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


def choose_affiliation(request):
    if request.method == "POST":
        affiliation_form = AffiliationForm(request.POST)

        if affiliation_form.is_valid():
            character = affiliation_form.save()

            context = {
                'affiliation_form': affiliation_form,
                'menu': menu,
            }
            return render(request, 'character/choose_affiliation.html', context=context)
    else:
        affiliation_form = AffiliationForm()

    context = {
        'affiliation_form': affiliation_form,
        'menu': menu,
    }
    return render(request, 'character/choose_affiliation.html', context=context)


def choose_information(request, race, character_class):
    form_race = Race.objects.get(name=race)
    if request.method == "POST":
        information_form = InformationForm(request.POST, prefix='information')

        if information_form.is_valid():
            form_name = information_form.cleaned_data.get('name', 'Дуэргар')
            form_background = translate_background(information_form.cleaned_data.get('background', 'noble'))
            form_alignment = translate_alignment(information_form.cleaned_data.get('alignment', 'chaotic evil'))
            form_player_name = information_form.cleaned_data.get('player_name', 'Иван')
            form_level = information_form.cleaned_data.get('level', 1)
            form_experience = calculate_experience(form_level)

            context = {
                'race': form_race,
                'class': character_class,
                'form_name': form_name,
                'form_background': form_background,
                'form_alignment': form_alignment,
                'form_player_name': form_player_name,
                'form_experience': form_experience,
                'form_level': form_level,
            }
            return redirect('choose_features', prev_context=context)
    else:
        information_form = InformationForm(prefix='information')
    context = {
        'information_form': information_form,
        'menu': menu
    }
    return render(request, 'character/choose_information.html', context=context)


def choose_features(request, prev_context):
    race = Race.objects.get(name=prev_context.get('race'))
    abil_score_inc_dict = race.abil_score_inc

    strength = abil_score_inc_dict.get('Сила', 0)
    dexterity = abil_score_inc_dict.get('Ловкость', 0)
    physique = abil_score_inc_dict.get('Телосложение', 0)
    intelligence = abil_score_inc_dict.get('Интеллект', 0)
    wisdom = abil_score_inc_dict.get('Мудрость', 0)
    charisma = abil_score_inc_dict.get('Харизма', 0)

    form_name = prev_context.get('form_name')
    form_background = prev_context.get('form_background')
    form_alignment = prev_context.get('form_alignment')
    form_player_name = prev_context.get('form_player_name')
    form_level = prev_context.get('form_level')
    form_experience = prev_context.get('form_experience')
    form_character_class = prev_context.get('form_character_class')

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
            'form_name': form_name,
            'form_background': form_background,
            'form_alignment': form_alignment,
            'form_player_name': form_player_name,
            'form_experience': form_experience,
            'form_level': form_level,
            'race': race,
            'form_character_class': form_character_class
        }
        return render(request, 'character/purchase_features.html', context=context)


