
from django.urls import path 
from .views import home,vaciar

urlpatterns = [
    path('',home,name='home'),
    path('vaciar/',vaciar,name='vaciar')
]
