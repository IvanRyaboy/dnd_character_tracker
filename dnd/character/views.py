# Импорт необходимых модулей
import math
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Импорт форм из текущего пакета
from .forms import *

# Меню для навигации по сайту
menu = [{'title': 'Классы', 'url_name': 'classes'},
        {'title': 'Рассы', 'url_name': 'races'},
        {'title': 'Заклинания', 'url_name': 'spells'}, ]


# Функция для отображения главного меню
def main_menu(request):
    return render(request, 'character/index.html', {'menu': menu})


# Функция для отображения списка классов персонажей
def classes(request):
    all_classes = CharacterClass.objects.all().order_by('name')  # Получение всех классов и сортировка по имени
    return render(request, 'character/classes.html', {'classes': all_classes, 'menu': menu})


# Функция для отображения списка рас персонажей
def races(request):
    all_races = Race.objects.all().order_by('name')  # Получение всех рас и сортировка по имени
    return render(request, "character/races.html", {'races': all_races, 'menu': menu})


# Функция для отображения списка заклинаний
def spells(request):
    all_spells = Spells.objects.all().order_by('id')  # Получение всех заклинаний и сортировка по ID
    return render(request, 'character/spells.html', {'spells': all_spells, 'menu': menu})


# Функция для отображения детальной информации о классе персонажа
def show_class(request, class_slug):
    character_class = get_object_or_404(CharacterClass, slug=class_slug)  # Получение класса по slug
    info = get_object_or_404(ClassInformation, character_class=character_class)  # Получение информации о классе

    context = {
        'class': character_class,
        'info': info,
        'title': character_class.name,
        'menu': menu,
    }
    return render(request, 'character/class.html', context=context)


# Функция для отображения детальной информации о расе персонажа
def show_race(request, race_slug):
    race = get_object_or_404(Race, slug=race_slug)  # Получение расы по slug
    info = get_object_or_404(RaceInformation, race=race)  # Получение информации о расе

    context = {
        'race': race,
        'info': info,
        'title': race.name,
        'menu': menu
    }
    return render(request, 'character/race.html', context=context)


# Функция для отображения детальной информации о заклинании
def show_spell(request, spell_slug):
    spell = get_object_or_404(Spells, slug=spell_slug)  # Получение заклинания по slug

    context = {
        'spell': spell,
        'title': spell.name,
        'menu': menu,
    }
    return render(request, 'character/spell.html', context=context)


# Функция для отображения списка оружия
def weapons(request):
    all_weapons = Weapons.objects.all()  # Получение всего оружия

    context = {
        'menu': menu,
        'weapons': all_weapons
    }
    return render(request, 'character/weapons.html', context=context)


# Функция для отображения списка доспехов
def armor(request):
    all_armor = Armor.objects.all()  # Получение всех доспехов

    context = {
        'menu': menu,
        'armor': all_armor
    }

    return render(request, 'character/armor.html', context=context)


# Функция для выбора принадлежности персонажа (например, игрока)
def choose_affiliation(request):
    if request.method == "POST":
        affiliation_form = AffiliationForm(request.POST)  # Обработка POST-запроса

        if affiliation_form.is_valid():
            character = affiliation_form.save(commit=False)  # Сохранение формы без коммита в БД
            if request.user in User.objects.all():
                character.player = get_object_or_404(Player, user=request.user)  # Привязка персонажа к игроку
            character.save()  # Сохранение персонажа

            context = {
                'affiliation_form': affiliation_form,
                'menu': menu,
            }
            return redirect('choose_information', character_id=character.id)  # Перенаправление на следующую страницу
    else:
        affiliation_form = AffiliationForm()  # Создание пустой формы для GET-запроса

    context = {
        'affiliation_form': affiliation_form,
        'menu': menu,
    }
    return render(request, 'character/choose_affiliation.html', context=context)


# Функция для выбора информации о персонаже (например, уровня и навыков)
def choose_information(request, character_id):
    character = get_object_or_404(Character, id=character_id)  # Получение персонажа по ID
    if request.method == "POST":
        information_form = InformationForm(request.POST, instance=character)  # Обработка POST-запроса
        selected_skills = information_form.data.getlist('skills')  # Получение выбранных навыков
        max_skills = get_max_skills(character)  # Получение максимального количества навыков

        try:
            if len(selected_skills) > max_skills:
                raise ValidationError(
                    f"Вы не можете выбрать более {max_skills} навыков")  # Проверка на превышение лимита
            if len(selected_skills) < max_skills:
                raise ValidationError(f"Выберите {max_skills} навыка")  # Проверка на минимальное количество навыков

            if information_form.is_valid():
                character.experience = calculate_experience(information_form.cleaned_data['level'])  # Расчет опыта
                character.proficiency_bonus = calculate_proficiency_bonus(
                    information_form.cleaned_data['level'])  # Расчет бонуса мастерства
                if character.player:
                    character.player_name = character.player.user.username  # Установка имени игрока
                else:
                    character.player_name = ""
                information_form.save()  # Сохранение формы
                return redirect('choose_features', character_id=character.id)  # Перенаправление на следующую страницу
        except ValidationError as e:
            information_form.add_error('skills', e)  # Добавление ошибки в форму
    else:
        information_form = InformationForm(instance=character)  # Создание формы для GET-запроса
    context = {
        'information_form': information_form,
        'menu': menu
    }
    return render(request, 'character/choose_information.html', context=context)


# Функция для выбора характеристик персонажа
def choose_features(request, character_id):
    character = get_object_or_404(Character, id=character_id)  # Получение персонажа по ID
    race = Race.objects.get(name=character.race)  # Получение расы персонажа
    abil_score_inc_dict = race.abil_score_inc  # Получение бонусов к характеристикам от расы
    character_class = CharacterClass.objects.get(name=character.character_class)  # Получение класса персонажа

    strength, dexterity, physique, intelligence, wisdom, charisma = get_characteristics_from_dict(
        abil_score_inc_dict)  # Получение характеристик

    if request.method == "POST":
        form = PurchaseForm(request.POST, prefix='form')  # Обработка POST-запроса
        if form.is_valid():
            # Расчет итоговых характеристик с учетом бонусов
            total_strength = form.cleaned_data.get('strength', 8) + strength
            total_dexterity = form.cleaned_data.get('dexterity', 8) + dexterity
            total_physique = form.cleaned_data.get('physique', 8) + physique
            total_intelligence = form.cleaned_data.get('intelligence', 8) + intelligence
            total_wisdom = form.cleaned_data.get('wisdom', 8) + wisdom
            total_charisma = form.cleaned_data.get('charisma', 8) + charisma

            # Расчет модификаторов характеристик
            strength_mod = math.floor((total_strength - 10) / 2)
            dexterity_mod = math.floor((total_dexterity - 10) / 2)
            physique_mod = math.floor((total_physique - 10) / 2)
            intelligence_mod = math.floor((total_intelligence - 10) / 2)
            wisdom_mod = math.floor((total_wisdom - 10) / 2)
            charisma_mod = math.floor((total_charisma - 10) / 2)

            # Создание словарей характеристик и модификаторов
            characteristics = {'Сила': total_strength, 'Ловкость': total_dexterity,
                               'Телосложение': total_physique, 'Интеллект': total_intelligence,
                               'Мудрость': total_wisdom, 'Харизма': total_charisma}

            modifiers = {'Сила': strength_mod, 'Ловкость': dexterity_mod,
                         'Телосложение': physique_mod, 'Интеллект': intelligence_mod,
                         'Мудрость': wisdom_mod, 'Харизма': charisma_mod}

            # Расчет спасбросков
            saving_throws = calculate_saving_throws(modifiers, character_class.saving_throws,
                                                    character.proficiency_bonus)

            # Сохранение характеристик, модификаторов и спасбросков
            character.characteristics = characteristics
            character.modifiers = modifiers
            character.saving_throws = saving_throws
            character.save()

            return redirect('choose_items', character_id=character.id)  # Перенаправление на следующую страницу
    else:
        form = PurchaseForm(prefix='form')  # Создание формы для GET-запроса

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


# Функция для выбора предметов (оружия и доспехов)
def choose_items(request, character_id):
    character = get_object_or_404(Character, id=character_id)  # Получение персонажа по ID
    money = convert_money(character.money)  # Конвертация денег персонажа

    all_armor = Armor.objects.all()  # Получение всех доспехов
    all_weapons = Weapons.objects.all()  # Получение всего оружия

    if request.method == 'POST':
        selected_armors = request.POST.getlist('armor')  # Получение выбранных доспехов
        selected_weapons = request.POST.getlist('weapons')  # Получение выбранного оружия

        total_cost = 0

        # Расчет общей стоимости выбранных предметов
        for armor_id in selected_armors:
            chosen_armor = Armor.objects.get(pk=armor_id)
            total_cost += chosen_armor.price
        for weapon_id in selected_weapons:
            chosen_weapon = Weapons.objects.get(pk=weapon_id)
            total_cost += chosen_weapon.price

        total_price = convert_money(total_cost)  # Конвертация общей стоимости

        if total_cost > character.money:
            return HttpResponseNotFound(
                'Слишком большая стоимость. Попробуйте закупть другие предметы')  # Проверка на превышение бюджета
        else:
            character.money = character.money - total_cost  # Вычитание стоимости из бюджета
            character.armor.set(selected_armors)  # Установка выбранных доспехов
            character.weapons.set(selected_weapons)  # Установка выбранного оружия
            character.save()  # Сохранение персонажа

            context = {
                'menu': menu,
                'character': character,
                'total_cost': total_price,
                'character_id': character_id,
                'armors': all_armor,
                'weapons': all_weapons,
                'gold': money.get('gold'),
                'silver': money.get('silver'),
                'copper': money.get('copper')
            }
            return HttpResponseRedirect(reverse('home'))  # Перенаправление на главную страницу
    else:
        form = ItemsForm()  # Создание формы для GET-запроса

    context = {
        'menu': menu,
        'form': form,
        'character': character,
        'armors': all_armor,
        'weapons': all_weapons,
        'gold': money.get('gold'),
        'silver': money.get('silver'),
        'copper': money.get('copper')
    }

    return render(request, 'character/choose_items.html', context=context)


# Функция для отображения списка персонажей
def characters(request):
    characters_list = Character.objects.all()  # Получение всех персонажей

    context = {
        "menu": menu,
        "characters": characters_list,
    }

    return render(request, 'character/characters.html', context=context)


# Функция для отображения детальной информации о персонаже
def show_character(request, character_id):
    character = get_object_or_404(Character, pk=character_id)  # Получение персонажа по ID

    context = {
        'menu': menu,
        'character': character
    }

    return render(request, 'character/character.html', context=context)


# Функция для отображения пустого листа персонажа с возможностью выбора существующих персонажей для зарегистрированного пользователя
def show_character_list(request):
    if request.user.is_authenticated:
        players_characters = Character.objects.filter(player=request.user.player)  # Получение персонажей пользователя
        context = {
            'players_characters': players_characters,
        }
        return render(request, 'character/character_list.html', context=context)
    return render(request, 'character/character_list.html')


# Функция для отображения листа персонажа зарегистрированного пользователя
def show_users_character_list(request, character_id):
    character = get_object_or_404(Character, pk=character_id)  # Получение персонажа по ID
    strength, dexterity, physique, intelligence, wisdom, charisma = get_characteristics_from_dict(
        character.characteristics)  # Получение характеристик

    context = {
        'character': character,
        'strength': strength,
        'dexterity': dexterity,
        'physique': physique,
        'intelligence': intelligence,
        'wisdom': wisdom,
        'charisma': charisma,
    }
    return render(request, 'character/character_list.html', context=context)


# Функция для авторизации пользователя
def login_user(request):
    if request.method == "POST":
        form = LoginUserForm(request.POST)  # Обработка POST-запроса

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],
                                password=cd['password'])  # Аутентификация пользователя

            if user and user.is_active:
                login(request, user)  # Вход пользователя
                return HttpResponseRedirect(reverse('home'))  # Перенаправление на главную страницу

    else:
        form = LoginUserForm()  # Создание формы для GET-запроса
    return render(request, 'character/login.html', {'form': form})


# Функция для выхода пользователя
def logout_user(request):
    logout(request)  # Выход пользователя
    return HttpResponseRedirect(reverse('login_user'))  # Перенаправление на страницу авторизации


# Функция для регистрации пользователя
def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)  # Обработка POST-запроса

        if form.is_valid():
            user = form.save()  # Сохранение пользователя
            player = Player(user=user)  # Создание игрока
            player.save()

            login(request, user)  # Автоматический вход после регистрации

            return HttpResponseRedirect(reverse('home'))  # Перенаправление на главную страницу

    else:
        form = RegistrationForm()  # Создание формы для GET-запроса

    context = {
        "menu": menu,
        'form': form,
    }
    return render(request, 'character/registration.html', context=context)


# Функция для отображения интерактивного листа персонажа
@require_http_methods(["GET", "POST"])
def show_users_interactive_list(request, character_id):
    # Получение персонажа по ID или возврат 404, если персонаж не найден
    character = get_object_or_404(Character, pk=character_id)

    # Получение скорости персонажа из его расы
    speed = character.race.speed

    # Получение инициативы персонажа
    initiative = character.get_initiative()

    # Если максимальное количество хитов персонажа равно 0, рассчитываем его
    if character.max_hp == 0:
        character.max_hp = max_hp(character)
        character.save()

    # Обработка AJAX-запроса для добавления снаряжения
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = EquipmentForm(request.POST)
        spell_form = SpellForm(request.POST)
        if form.is_valid() and spell_form.is_valid():
            equipment_type = form.cleaned_data['equipment_type']
            response_data = {'success': True}

            try:
                if equipment_type == 'weapon':
                    weapon = form.cleaned_data['weapon']
                    character.weapons.add(weapon)
                    character.money -= weapon.price
                    response_data['added_item'] = f"{weapon.name} (оружие) - {weapon.price} мм, {weapon.weight} фунтов"
                elif equipment_type == 'armor':
                    armor = form.cleaned_data['armor']
                    character.armor.add(armor)
                    character.money -= armor.price
                    response_data['added_item'] = f"{armor.name} (доспехи) - {armor.price} мм, {armor.weight} фунтов"
                elif equipment_type == 'other':
                    item = {
                        'name': form.cleaned_data['item_name'],
                        'price': form.cleaned_data['item_price'],
                        'weight': form.cleaned_data['item_weight']
                    }
                    equipment = character.equipment or []
                    equipment.append(item)
                    character.equipment = equipment
                    character.money -= item['price']
                    response_data['added_item'] = f"{item['name']} - {item['price']} мм, {item['weight']} фунтов"

                character.save()
                response_data['coins'] = character.get_coins()
                return JsonResponse(response_data)

            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)

        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    # Получение количества монет персонажа
    coins = character.get_coins()

    # Получаем список снаряжения для отображения
    character_equipment = []
    for weapon in character.weapons.all():
        character_equipment.append(f"{weapon.name} (оружие) - {weapon.price} мм, {weapon.weight} фунтов")
    for armor in character.armor.all():
        character_equipment.append(f"{armor.name} (доспехи) - {armor.price} мм, {armor.weight} фунтов")
    if character.equipment:
        for item in character.equipment:
            character_equipment.append(f"{item['name']} - {item['price']} мм, {item['weight']} фунтов")

    # Создание контекста для передачи в шаблон
    context = {
        'character': character,
        'character_max_hp': character.max_hp,
        'initiative': initiative,
        'speed': speed,
        'coins': coins,
        'equipment_form': EquipmentForm(),
        'character_equipment': character_equipment,
        'spell_form': SpellForm()
    }

    # Рендеринг шаблона с переданным контекстом
    return render(request, 'character/interactive_list.html', context=context)


# Декоратор для отключения CSRF-защиты (для разработки, в продакшене удалить)
@csrf_exempt
def calculate_initiative(request):
    # Обработка POST-запроса
    if request.method == 'POST':
        # Парсинг JSON-данных из тела запроса
        data = json.loads(request.body)

        # Получение ID персонажа из данных
        character_id = data.get('character_id')

        # Получение персонажа по ID или возврат 404, если персонаж не найден
        character = get_object_or_404(Character, pk=character_id)

        # Получение инициативы персонажа
        initiative = character.get_initiative()  # Используется метод get_initiative()

        # Возврат JSON-ответа с инициативой
        return JsonResponse({'initiative': initiative})

    # Возврат ошибки, если запрос не POST
    return JsonResponse({'error': 'Invalid request'}, status=400)
