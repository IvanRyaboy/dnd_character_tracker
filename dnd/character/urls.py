from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [
    path('', main_menu, name='home'),
    path('classes/', classes, name='classes'),
    path('classes/<slug:class_slug>/', show_class, name='class'),
    path('races/', races, name='races'),
    path('races/<slug:race_slug>/', show_race, name='race'),
    path('spells/', spells, name="spells"),
    path('spells/<slug:spell_slug>/', show_spell, name="spell"),
    path('create_character/', create_character, name='create_character'),
    path('choose_race/', choose_race_for_features, name='choose_race'),
    path('purchase_features/<slug:race_slug>/', purchase_features, name='purchase_features'),
    path('get_characteristics/<slug:class_slug>/', get_characteristics, name='get_characteristics')
]
