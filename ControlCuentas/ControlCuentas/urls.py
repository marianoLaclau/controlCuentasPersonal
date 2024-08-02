
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('autenticacion.urls')),
    path('home/', include('home.urls')),
    path('ingreso/',include('ingreso.urls')),
    path('egreso/', include('egreso.urls')),
    path('ahorro/',include('ahorros.urls')),
    path('metricas/', include('metricas.urls')),
]
