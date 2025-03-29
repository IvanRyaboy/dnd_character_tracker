# Импорт моделей из текущего пакета
from .models import *
import random


# Функция возвращает список классов персонажей в формате (английское название, русское название)
def get_classes_list():
    classes_list = [('bard', 'Бард'), ("barbarian", "Варвар"),
                    ('warrior', "Воин"), ('wizard', "Волшебник"),
                    ('druid', "Друид"), ('cleric', "Жрец"),
                    ('artificer', "Изобретатель"), ('warlock', "Колдун"),
                    ('monk', "Монах"), ('paladin', "Паладин"),
                    ('rogue', "Плут"), ('ranger', "Следопыт"),
                    ('sorcerer', "Чародей")]
    return classes_list


# Функция возвращает список рас персонажей в формате (английское название, русское название)
def get_races_list():
    races_list = [('dwarf', 'Дварф'), ('dragonborn', 'Драконорждённый'),
                  ('half-orc', 'Полуорк'), ('halfling', 'Полурослик'),
                  ('half-elf', 'Полуэльф'), ('tiefling', 'Тифлинг'),
                  ('human', 'Человек'), ('elf', 'Эльф')]
    return races_list


# Функция возвращает список предысторий персонажей в формате (английское название, русское название)
def get_backgrounds_list():
    backgrounds_list = [('artist', 'Артист'), ('homeless', 'Безпризорник'),
                        ('noble', 'Благородный'), ('guild craftsman', 'Гидьдейский ремесленник'),
                        ('sailor', 'Моряк'), ('sage', 'Мудрец'),
                        ('folk hero', 'Народный герой'), ('hermit', 'Отшельник'),
                        ('pirate', 'Пират'), ('criminal', 'Преступник'),
                        ('soldier', 'Солдат'), ('foreigner', 'Чужеземец'),
                        ('charlatan', 'Шарлатан')]
    return backgrounds_list


# Функция возвращает список мировоззрений персонажей в формате (английское название, русское название)
def get_alignment_list():
    alignment_list = [('lawful good', 'Упорядоченно добрый'), ('neutral good', 'Добрый'),
                      ('chaotic good', 'Хаотично добрый'), ('lawful neutral', 'Упорядоченный'),
                      ('true neutral', 'Истинно нейтральный'), ('chaotic neutral', 'Хаотичный'),
                      ('lawful evil', 'Упорядоченно злой'), ('neutral evil', 'Злой'),
                      ('chaotic evil', 'Хаотично злой'), ('unaligned', 'Вне мировоззрения')]
    return alignment_list


# Функция извлекает значения характеристик из словаря и возвращает их
def get_characteristics_from_dict(characteristics):
    strength = characteristics.get('Сила', 0)
    dexterity = characteristics.get('Ловкость', 0)
    physique = characteristics.get('Телосложение', 0)
    intelligence = characteristics.get('Интеллект', 0)
    wisdom = characteristics.get('Мудрость', 0)
    charisma = characteristics.get('Харизма', 0)
    return strength, dexterity, physique, intelligence, wisdom, charisma


# Функция переводит предысторию с английского на русский язык
def translate_background(background):
    backgrounds = get_backgrounds_list()
    for background_en, background_ru in backgrounds:
        if background_en == background:
            return background_ru
    return 'Отшельник'  # Возвращает значение по умолчанию, если перевод не найден


# Функция переводит мировоззрение с английского на русский язык
def translate_alignment(alignment):
    alignments = get_alignment_list()
    for alignment_en, alignment_ru in alignments:
        if alignment_en == alignment:
            return alignment_ru
    return 'Истинно нейтрильный'  # Возвращает значение по умолчанию, если перевод не найден


# Функция возвращает количество опыта, необходимое для достижения определённого уровня
def calculate_experience(level):
    level_to_exp = {
        1: 0,
        2: 300,
        3: 900,
        4: 2700,
        5: 6500,
        6: 14000,
        7: 23000,
        8: 34000,
        9: 48000,
        10: 64000,
        11: 85000,
        12: 100000,
        13: 120000,
        14: 140000,
        15: 165000,
        16: 195000,
        17: 225000,
        18: 265000,
        19: 305000,
        20: 355000,
    }
    return level_to_exp.get(level)


# Функция возвращает бонус мастерства для определённого уровня
def calculate_proficiency_bonus(level):
    proficiency_bonus = {
        1: 2,
        2: 2,
        3: 2,
        4: 2,
        5: 3,
        6: 3,
        7: 3,
        8: 3,
        9: 4,
        10: 4,
        11: 4,
        12: 4,
        13: 5,
        14: 5,
        15: 5,
        16: 5,
        17: 6,
        18: 6,
        19: 6,
        20: 6,
    }
    return proficiency_bonus.get(level)


# Функция рассчитывает спасброски на основе модификаторов, спасбросков класса и бонуса мастерства
def calculate_saving_throws(modifiers, classes_saving_throws, proficiency_bonus):
    if 'Сила' in classes_saving_throws:
        strength = modifiers.get('Сила') + proficiency_bonus
    else:
        strength = modifiers.get('Сила')
    if 'Ловкость' in classes_saving_throws:
        dexterity = modifiers.get('Ловкость') + proficiency_bonus
    else:
        dexterity = modifiers.get('Ловкость')
    if 'Телосложение' in classes_saving_throws:
        physique = modifiers.get('Телосложение') + proficiency_bonus
    else:
        physique = modifiers.get('Телосложение')
    if 'Интеллект' in classes_saving_throws:
        intelligence = modifiers.get('Интеллект') + proficiency_bonus
    else:
        intelligence = modifiers.get('Интеллект')
    if 'Мудрость' in classes_saving_throws:
        wisdom = modifiers.get('Мудрость') + proficiency_bonus
    else:
        wisdom = modifiers.get('Мудрость')
    if 'Харизма' in classes_saving_throws:
        charisma = modifiers.get('Харизма') + proficiency_bonus
    else:
        charisma = modifiers.get('Харизма')

    saving_throws = {'Сила': strength, 'Ловкость': dexterity,
                     'Телосложение': physique, 'Интеллект': intelligence,
                     'Мудрость': wisdom, 'Харизма': charisma}

    return saving_throws


# Функция возвращает максимальное количество навыков, которые может выбрать персонаж в зависимости от класса
def get_max_skills(character):
    if character.character_class.name in ['Бард', 'Следопыт']:
        return 3
    if character.character_class.name == 'Плут':
        return 4
    else:
        return 2


# Функция конвертирует количество медяков в платину, золото, серебро и медяки
def convert_money(copper):
    platinum = copper // 1000
    copper %= 1000
    gold = copper // 100
    copper %= 100
    silver = copper // 10
    copper = copper % 10
    return {'platinum': platinum, 'gold': gold, 'silver': silver, 'copper': copper}


# Функция рассчитывает класс брони (AC) в зависимости от типа доспеха и модификаторов
def calculate_armor_class(armor, modifiers) -> int:
    if armor is None:
        return 10 + modifiers.get('Ловкость', 0)
    if armor.type == 'Лёгкий доспех':
        return armor.armor_class + modifiers.get('Ловкость', 0)
    if armor.type == 'Средний доспех':
        return armor.armor_class + min(modifiers.get('Ловкость', 0), 2)
    if armor.type == 'Тяжелый доспех':
        return armor.armor_class


# Функция рассчитывает максимальное количество хитов персонажа на основе его уровня, класса и модификаторов
def max_hp(character) -> int:
    character_max_hp = character.character_class.hp_dice + character.modifiers.get('Телосложение', 0)
    for _ in range(2, character.level + 1):
        character_max_hp += (random.randint(1, character.character_class.hp_dice) +
                             character.modifiers.get('Телосложение', 0))
    return character_max_hp


# Функция проверяет, превышает ли вес инвентаря максимальную грузоподъёмность персонажа
def is_max_capacity_exceed(character) -> bool:
    is_exceed = False
    max_capacity = character.characteristics.get('Сила', 0) * 15
    if character.inventory_capacity > max_capacity:
        is_exceed = True
    return is_exceed


# Функция рассчитывает инициативу персонажа на основе модификатора ловкости и случайного броска кубика
def calculate_initiative(modifiers) -> int:
    dexterity_modifier = modifiers.get('Ловкость', 0)
    roll = random.randint(1, 20)
    initiative = roll + dexterity_modifier
    return initiative


# Функция рассчитывает текущий вес инвентаря персонажа, учитывая оружие, доспехи и остальной инвентарь
def count_current_capacity(weapon, armor, inventory_capacity) -> int:
    current_capacity = weapon.weight + armor.weight + inventory_capacity
    return current_capacity



