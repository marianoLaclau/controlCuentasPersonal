from django.shortcuts import render, redirect, get_object_or_404
from .models import Egreso
from django.contrib import messages
from .forms import EgresoForm
from django.contrib.auth.decorators import login_required


@login_required
def egreso(request, categoria=None):
    if categoria:
        todos = Egreso.objects.filter(usuario=request.user, categoria=categoria)
    else:
        todos = Egreso.objects.filter(usuario=request.user)
    
    context = {
        'todos': todos  # Usa el mismo nombre de variable en el contexto y en la plantilla
    }
    return render(request, 'egreso/egreso.html', context=context)


@login_required
def egreso_mes(request, mes=None):
    if mes:
        todos = Egreso.objects.filter(usuario=request.user, fecha__month=mes)
        if not todos:
            messages.error(request, 'Sin registros')
    else:
        todos = Egreso.objects.filter(usuario=request.user)
    
    context = {
        'todos': todos  # Usa el mismo nombre de variable en el contexto y en la plantilla
    }
    return render(request, 'egreso/egreso.html', context=context)


@login_required
def detalles(request, id):
    todo = get_object_or_404(Egreso, id=id, usuario=request.user)
    context = {
        'detalles': todo,
    }
    return render(request, 'egreso/detalles.html', context=context)


@login_required
def crear(request):
    if request.method == 'GET':
        form = EgresoForm()
        context = {
            'form': form
        }
        return render(request, 'egreso/crear.html', context=context)
    
    if request.method == 'POST':
        try:
            form = EgresoForm(request.POST)
            if form.is_valid():
                egreso = form.save(commit=False)
                egreso.usuario = request.user  # Asignar el usuario actual
                egreso.save()
                messages.success(request, 'Registrado con éxito!')
                return redirect('egreso')
            else:
                messages.error(request, 'Hubo un error en los datos ingresados. Reintente.')
                context = {'form': form}
                return render(request, 'egreso/crear.html', context=context)
        
        except Exception as e:
            messages.error(request, f'Hubo un error al guardar los datos: {e}')
            return redirect('egreso')
