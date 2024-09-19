from django import forms
from django.core.exceptions import ValidationError
from .models import *
from .functions import *


class AffiliationForm(forms.ModelForm):
    classes_list = get_classes_list()
    races_list = get_races_list()

    class Meta:
        model = Character
        fields = ['race', 'character_class']


class InformationForm(forms.ModelForm):

    class Meta:
        model = Character
        fields = ['character_name', 'background', 'alignment', 'player_name', 'level', 'skills']


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
            raise ValidationError("Вы не можете использовать больше 27 очков для закупки характеристик.")

        elif used_points < 75:
            raise ValidationError("Пожалуйста, используйте все 27 очков характеристик.")

        return cleaned_data
