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
]
