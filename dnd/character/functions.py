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


def characteristic_distribution():
    pass
