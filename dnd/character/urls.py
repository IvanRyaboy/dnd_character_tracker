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
    path('choose_affiliation/', choose_affiliation, name='choose_affiliation'),
    path('choose_information/<int:character_id>/', choose_information, name='choose_information'),
    path('choose_features/<int:character_id>/', choose_features, name='choose_features'),
    path('choose_items/<int:character_id>/', choose_items, name='choose_items'),
    path('characters/', characters, name='characters'),
    path('characters/<int:character_id>/', show_character, name='show_character'),
]
