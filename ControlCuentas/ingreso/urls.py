
from django.urls import path 
from .views import ingreso ,crear

urlpatterns = [
    path('',ingreso,name='ingreso'),
    path('crear/',crear,name='crear'),
]
