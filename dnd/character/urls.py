from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [
    path('', main_menu, name='home'),
    path('classes/', classes, name='classes'),
    path('classes/<slug:class_slug>/', show_class, name='class'),
]
