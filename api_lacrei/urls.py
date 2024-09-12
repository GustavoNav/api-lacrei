from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('<str:model_name>/', views.handle_request, name='handle_request'),
] 