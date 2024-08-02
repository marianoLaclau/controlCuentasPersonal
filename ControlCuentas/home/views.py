from django.shortcuts import render,redirect
from egreso.models import Egreso ,Servicios,Deudas,GastosVarios
from ingreso.models import Ingreso
from ahorros.models import Ahorro
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request,'home/home.html',{})


@login_required
def vaciar(request):
    try:
        Egreso.objects.all().delete()
        Ingreso.objects.all().delete()
        Ahorro.objects.all().delete()
        Servicios.objects.all().delete()
        Deudas.objects.all().delete()
        GastosVarios.objects.all().delete()
        messages.success(request,'Se ha vaciado la base de datos correctamente')
    
    except Exception as e:
        messages.error(request,f'Error al vaciar la base de datos: {str(e)}')
    
    return redirect ('home')