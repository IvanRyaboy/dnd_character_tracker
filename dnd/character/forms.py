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
        character = kwargs.get('instance', None)
        super(InformationForm, self).__init__(*args, **kwargs)

        if character is not None:
            self.fields['skills'].queryset = Skills.objects.filter(character_class=character.character_class)
            self.fields['spells'].queryset = Spells.objects.filter(character_class=character.character_class)

    class Meta:
        model = Character
        fields = ['character_name', 'background', 'alignment', 'level', 'skills', 'spells']


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
    class Meta:
        model = Character
        fields = ['armor', 'weapons']
        widgets = {
            "armor": forms.CheckboxSelectMultiple,
            "weapons": forms.CheckboxSelectMultiple
        }


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class EquipmentForm(forms.Form):
    EQUIPMENT_TYPE_CHOICES = [
        ('weapon', 'Оружие'),
        ('armor', 'Доспехи'),
        ('other', 'Другое снаряжение'),
    ]

    equipment_type = forms.ChoiceField(
        choices=EQUIPMENT_TYPE_CHOICES,
        label='Тип снаряжения',
        widget=forms.Select(attrs={'class': 'equipment-type-selector'})
    )

    # Поля для оружия
    weapon = forms.ModelChoiceField(
        queryset=Weapons.objects.all(),
        label='Выберите оружие',
        required=False,
        widget=forms.Select(attrs={'class': 'weapon-selector'})
    )

    # Поля для доспехов
    armor = forms.ModelChoiceField(
        queryset=Armor.objects.all(),
        label='Выберите доспехи',
        required=False,
        widget=forms.Select(attrs={'class': 'armor-selector'})
    )

    # Поля для обычного снаряжения
    item_name = forms.CharField(
        max_length=100,
        label='Название предмета',
        required=False,
        widget=forms.TextInput(attrs={'class': 'item-name-input'})
    )
    item_price = forms.IntegerField(
        label='Цена (в медных монетах)',
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'item-price-input'})
    )
    item_weight = forms.IntegerField(
        label='Вес',
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'item-weight-input'})
    )

    def clean(self):
        cleaned_data = super().clean()
        equipment_type = cleaned_data.get('equipment_type')

        if equipment_type == 'weapon' and not cleaned_data.get('weapon'):
            self.add_error('weapon', 'Пожалуйста, выберите оружие')
        elif equipment_type == 'armor' and not cleaned_data.get('armor'):
            self.add_error('armor', 'Пожалуйста, выберите доспехи')
        elif equipment_type == 'other':
            if not cleaned_data.get('item_name'):
                self.add_error('item_name', 'Введите название предмета')
            if cleaned_data.get('item_price') is None:
                self.add_error('item_price', 'Введите цену предмета')
            if cleaned_data.get('item_weight') is None:
                self.add_error('item_weight', 'Введите вес предмета')

        return cleaned_data


class SpellForm(forms.Form):
    SPELL_TYPE_CHOICES = [
        ('abjuration', 'Ограждение'),
        ('conjuration', 'Вызов'),
        ('divination', 'Прорицание'),
        ('enchantment', 'Очарование'),
        ('evocation', 'Воплощение'),
        ('illusion', 'Иллюзия'),
        ('necromancy', 'Некромантия'),
        ('transmutation', 'Преобразование'),
        ('universal', 'Универсальное')
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        spell_type = self.data.get('spell_type') if not self.data else None
        self.fields['spell_type'] = forms.ChoiceField(
            choices=self.SPELL_TYPE_CHOICES,
            label='Тип заклинания',
            widget=forms.Select(attrs={
                'class': 'spell_type_selector',
            })
        )

        self.fields['spell'] = forms.ModelChoiceField(
            queryset=self.get_filtered_spells(spell_type),
            label='Выберите заклинание',
            required=False,
            widget=forms.Select(attrs={'id': 'spell_id'})
        )

    def get_filtered_spells(self, spell_type=None):
        """Возвращает отфильтрованный queryset заклинаний"""
        if spell_type and spell_type != '':
            return Spells.objects.filter(spell_type=spell_type)
        return Spells.objects.none()
