# Coded with <3 Razuvitto
# location : Test/apps/urls.py
# April 2018

from django.urls import path
from apps import views

app_name = 'apps'
urlpatterns = [
    path('', views.form_index),
    path('test/', views.classification),
]