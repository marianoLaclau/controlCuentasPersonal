
from django.urls import path 
from .views import egreso ,detalles ,crear, egreso_mes

urlpatterns = [
    path('',egreso,name='egreso'),
    path('<int:categoria>',egreso,name='egreso_cat'),
    path('mes/<int:mes>',egreso_mes,name='egreso_mes'),
    path('crear/',crear,name='crearegreso'),
    path('detalles/<int:id>',detalles,name='detallesegreso'),
]
