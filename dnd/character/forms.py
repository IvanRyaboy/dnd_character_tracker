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
    skills = forms.ModelMultipleChoiceField(queryset=Skills.objects.none(),
                                            required=False)
    spells = forms.ModelMultipleChoiceField(queryset=Spells.objects.none(),
                                            required=False)

    def __init__(self, *args, **kwargs):
        character = kwargs.pop('instance', None)
        super(InformationForm, self).__init__(*args, **kwargs)

        if character is not None:
            self.fields['skills'].queryset = Skills.objects.filter(character_class=character.character_class)
            self.fields['spells'].queryset = Spells.objects.filter(character_class=character.character_class)

    class Meta:
        model = Character
        fields = ['character_name', 'background', 'alignment', 'player_name', 'level', 'skills', 'spells']


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


class ItemsForm(forms.ModelForm):
    armor = forms.ModelMultipleChoiceField(queryset=Armor.objects.all(),
                                           required=False, widget=forms.CheckboxSelectMultiple)
    weapons = forms.ModelMultipleChoiceField(queryset=Weapons.objects.all(),
                                             required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Character
        fields = ['armor', 'weapons']

