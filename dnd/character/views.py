import math
from django.shortcuts import render, get_object_or_404, redirect
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
            character = affiliation_form.save(commit=False)
            character.save()

            context = {
                'affiliation_form': affiliation_form,
                'menu': menu,
            }
            return redirect('choose_information', character_id=character.id)
    else:
        affiliation_form = AffiliationForm()

    context = {
        'affiliation_form': affiliation_form,
        'menu': menu,
    }
    return render(request, 'character/choose_affiliation.html', context=context)


def choose_information(request, character_id):
    character = get_object_or_404(Character, id=character_id)
    if request.method == "POST":
        information_form = InformationForm(request.POST, instance=character)

        if information_form.is_valid():
            character.experience = calculate_experience(information_form.cleaned_data['level'])
            character.proficiency_bonus = calculate_proficiency_bonus(information_form.cleaned_data['level'])
            information_form.save()
            context = {
                'information_form': information_form,
                'menu': menu
            }
            return redirect('choose_features', character_id=character.id)
    else:
        information_form = InformationForm(instance=character)
    context = {
        'information_form': information_form,
        'menu': menu
    }
    return render(request, 'character/choose_information.html', context=context)


def choose_features(request, character_id):
    character = get_object_or_404(Character, id=character_id)
    race = Race.objects.get(name=character.race)
    abil_score_inc_dict = race.abil_score_inc
    character_class = CharacterClass.objects.get(name=character.character_class)

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

            characteristics = {'Сила': total_strength, 'Ловкость': total_dexterity,
                               'Телосложение': total_physique, 'Интеллект': total_intelligence,
                               'Мудрость': total_wisdom, 'Харизма': total_charisma}

            modifiers = {'Сила': strength_mod, 'Ловкость': dexterity_mod,
                         'Телосложение': physique_mod, 'Интеллект': intelligence_mod,
                         'Мудрость': wisdom_mod, 'Харизма': charisma_mod}

            saving_throws = calculate_saving_throws(modifiers, character_class.saving_throws,
                                                    character.proficiency_bonus)

            character.characteristics = characteristics
            character.modifiers = modifiers
            character.saving_throws = saving_throws
            character.save()

            return redirect('spell', spell_slug='geroizm')
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

    return render(request, 'character/choose_features.html', context=context)


def characters(request):
    characters_list = Character.objects.all()

    context = {
        "menu": menu,
        "characters": characters_list,
    }

    return render(request, 'character/characters.html', context=context)


def show_character(request, character_id):
    character = get_object_or_404(Character, pk=character_id)

    context = {
        'menu': menu,
        'character': character
    }

    return render(request, 'character/character.html', context=context)
