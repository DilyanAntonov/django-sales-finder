from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('clothes/', views.clothes, name='clothes'),
    path('clothes_search/', views.clothes_search, name='clothes_search'),
    path('shoes/', views.shoes, name='shoes'),
    path('shoes_search/', views.shoes_search, name='shoes_search'),
]