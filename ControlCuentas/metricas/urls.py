
from django.urls import path 
from .views import metricas

urlpatterns = [
    path('',metricas,name='metricas')
]
