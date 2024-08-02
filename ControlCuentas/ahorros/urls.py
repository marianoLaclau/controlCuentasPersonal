
from django.urls import path 
from .views import ahorro  ,agregar , detalles , eliminar

urlpatterns = [
    path('',ahorro,name='ahorro'),
    path('agregar/',agregar,name='agregarahorro'),
    path('detalles/<int:id>',detalles,name='detalleahorro'),
    path('actualizar/',agregar,name='actualizarahorro'),
    path('eliminar/<int:id>',eliminar,name='eliminar')
   
]
