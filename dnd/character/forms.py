from django import forms
from .functions import *


class CharacterForm(forms.Form):
    classes_list = get_classes_list()
    races_list = get_races_list()
    backgrounds_list = get_backgrounds_list()
    alignment_list = get_alignment_list()

    name = forms.CharField(label="Имя персонажа")
    character_class = forms.ChoiceField(label="Класс персонажа", choices=classes_list)
    race = forms.ChoiceField(label='Раса персонажа', choices=races_list)
    background = forms.ChoiceField(label='Предыстория', choices=backgrounds_list)
    alignment = forms.ChoiceField(label='Мировоззрение', choices=alignment_list)
    player_name = forms.CharField(label="Имя игрока")
    experience = forms.IntegerField(label='Опыт')
    level = forms.IntegerField(label='Уровень')


class SurvivingForm(forms.Form):
    armor_class = forms.IntegerField(label='Класс защиты')
    initiative = forms.IntegerField(label='Инициатива')
    speed = forms.IntegerField(label='Скорость')
    max_hp = forms.IntegerField(label='Максимум хитов')
    current_hp = forms.IntegerField(label='Текущие хиты')
    temporary_hp = forms.IntegerField(label='Временные хиты')
    quantity_hp_dice = forms.IntegerField(label='Количестов дайсов')
    hp_dice = forms.CharField(label='Кость хитов')


class PurchaseForm(forms.Form):
    strength = forms.IntegerField(min_value=8, max_value=15, initial=8)
    dexterity = forms.IntegerField(min_value=8, max_value=15, initial=8)
    physique = forms.IntegerField(min_value=8, max_value=15, initial=8)
    intelligence = forms.IntegerField(min_value=8, max_value=15, initial=8)
    wisdom = forms.IntegerField(min_value=8, max_value=15, initial=8)
    charisma = forms.IntegerField(min_value=8, max_value=15, initial=8)

    def clean(self):
        cleaned_data = super().clean()

        field_names = ['strength', 'dexterity', 'physique', 'intelligence', 'wisdom', 'charisma']

        used_points = sum(cleaned_data.get(field, 8) or 8 for field in field_names)

        if used_points > 75:
            raise ValidationError("Вы можете использовать только 27 очков для закупки характеристик.")

        return cleaned_data
