from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormAhorro
from .models import Ahorro
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def ahorro(request):
    todos = Ahorro.objects.filter(usuario=request.user)
    context = {
        'todos': todos  # Usa el mismo nombre de variable en el contexto y en la plantilla
    }
    return render(request, 'ahorro/ahorro.html', context=context)


@login_required
def agregar(request):
    if request.method == 'GET':
        form = FormAhorro()
        context = {'form': form}
        return render(request, 'ahorro/crear.html', context=context)
    
    if request.method == 'POST':
        try:
            form = FormAhorro(request.POST)
            if form.is_valid():
                ahorro = form.save(commit=False)
                ahorro.usuario = request.user  # Asignar el usuario actual
                ahorro.save()
                messages.success(request, 'Hecho!.')
                return redirect('ahorro')
            else:
                messages.error(request, 'Hubo un error. Vuelva a intentar.')
                context = {'form': form}
                return render(request, 'ahorro/crear.html', context=context)
        
        except Exception as e:
            messages.error(request, f'Hubo un error al guardar los datos: {e}')
            return redirect('ahorro')


@login_required
def detalles(request, id):
    detalle = get_object_or_404(Ahorro, id=id, usuario=request.user)
    context = {'detalles': detalle}
    return render(request, 'ahorro/detalles.html', context=context)


@login_required
def actualizar(request, id):
    ahorro = get_object_or_404(Ahorro, id=id, usuario=request.user)
    if request.method == 'GET':
        form = FormAhorro(instance=ahorro)
        context = {'form': form}
        return render(request, 'ahorro/actualizar.html', context=context)
    
    if request.method == 'POST':
        try:
            form = FormAhorro(request.POST, instance=ahorro)
            if form.is_valid():
                form.save()
                messages.success(request, 'Hecho!.')
                return redirect('ahorro')
            else:
                messages.error(request, 'Hubo un error en los datos ingresados. Reintente.')
                context = {'form': form}
                return render(request, 'ahorro/actualizar.html', context=context)
        
        except Exception as e:
            messages.error(request, f'Hubo un error al guardar los datos: {e}')
            return redirect('ahorro')


@login_required
def eliminar(request, id):
    ahorro = get_object_or_404(Ahorro, id=id, usuario=request.user)
    try:
        ahorro.delete()
        messages.success(request, 'Hecho!.')
    except Exception as e:
        messages.error(request, f'Hubo un error al eliminar el registro: {e}')
    return redirect('ahorro')
