"""Urls patterns for roster app"""
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'roster'

urlpatterns = [
    path('', TemplateView.as_view(template_name='roster/home.html'), name='home'),
]
