"""Urls patterns for roster app"""
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'roster'

urlpatterns = [
    path('', TemplateView.as_view(template_name='roster/home.html'), name='home'),
    path('staffs/', views.StaffListView.as_view(), name='staffsList'),
    path('staffs/new/', views.CreateStaffView.as_view(), name='newStaff'),
    path('staffs/<int:id>/', views.StaffActionsView.as_view(), name='staffActions')
]
