from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from apps import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('apps/',include('apps.urls')),
]
