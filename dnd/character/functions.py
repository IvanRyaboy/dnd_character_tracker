from .models import *


def get_classes_list():
    classes_list = [('bard', 'Бард'), ("barbarian", "Варвар"),
                    ('warrior', "Воин"), ('wizard', "Волшебник"),
                    ('druid', "Друид"), ('cleric', "Жрец"),
                    ('artificer', "Изобретатель"), ('warlock', "Колдун"),
                    ('monk', "Монах"), ('paladin', "Паладин"),
                    ('rogue', "Плут"), ('ranger', "Следопыт"),
                    ('sorcerer', "Чародей")]
    return classes_list


def get_races_list():
    races_list = [('dwarf', 'Дварф'), ('dragonborn', 'Драконорждённый'),
                  ('half-orc', 'Полуорк'), ('halfling', 'Полурослик'),
                  ('half-elf', 'Полуэльф'), ('tiefling', 'Тифлинг'),
                  ('human', 'Человек'), ('elf', 'Эльф')]
    return races_list


def get_backgrounds_list():
    backgrounds_list = [('artist', 'Артист'), ('homeless', 'Безпризорник'),
                        ('noble', 'Благородный'), ('guild craftsman', 'Гидьдейский ремесленник'),
                        ('sailor', 'Моряк'), ('sage', 'Мудрец'),
                        ('folk hero', 'Народный герой'), ('hermit', 'Отшельник'),
                        ('pirate', 'Пират'), ('criminal', 'Преступник'),
                        ('soldier', 'Солдат'), ('foreigner', 'Чужеземец'),
                        ('charlatan', 'Шарлатан')]
    return backgrounds_list


def get_alignment_list():
    alignment_list = [('lawful good', 'Упорядоченно добрый'), ('neutral good', 'Добрый'),
                      ('chaotic good', 'Хаотично добрый'), ('lawful neutral', 'Упорядоченный'),
                      ('true neutral', 'Истинно нейтральный'), ('chaotic neutral', 'Хаотичный'),
                      ('lawful evil', 'Упорядоченно злой'), ('neutral evil', 'Злой'),
                      ('chaotic evil', 'Хаотично злой'), ('unaligned', 'Вне мировоззрения')]
    return alignment_list


def translate_background(background):
    backgrounds = get_backgrounds_list()
    for background_en, background_ru in backgrounds:
        if background_en == background:
            return background_ru
    return 'Отшельник'


def translate_alignment(alignment):
    alignments = get_alignment_list()
    for alignment_en, alignment_ru in alignments:
        if alignment_en == alignment:
            return alignment_ru
    return 'Истинно нейтрильный'


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


def get_max_skills(character):
    if character.character_class.name in ['Бард', 'Следопыт']:
        return 3
    if character.character_class.name == 'Плут':
        return 4
    else:
        return 2


def convert_money(copper):
    gold = copper // 100
    silver = (copper % 100) // 10
    copper = copper % 10
    money = {'gold': gold, 'silver': silver, 'copper': copper}
    return money

def calculate_price():
    pass
