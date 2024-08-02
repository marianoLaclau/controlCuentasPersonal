from django.shortcuts import render, redirect
from .forms import IngresoForm
from .models import Ingreso
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def ingreso(request):
    todos = Ingreso.objects.filter(usuario=request.user)
    context = {
        'todos': todos  # Asegúrate de usar el mismo nombre de variable en el contexto y en la plantilla
    }
    return render(request, 'ingreso/ingresos.html', context=context)


@login_required
def crear(request):
    if request.method == 'GET':
        form = IngresoForm()
        context = {
            'form': form
        }
        return render(request, 'ingreso/crear.html', context=context)

    if request.method == 'POST':
        try:
            form = IngresoForm(request.POST)
            if form.is_valid():
                ingreso = form.save(commit=False)
                ingreso.usuario = request.user  # Asignar el usuario actual
                ingreso.save()
                messages.success(request, 'Hecho!.')
                return redirect('ingreso')
            else:
                messages.error(request, 'Hubo un error en los datos ingresados. Reintente.')
                context = {'form': form}
                return render(request, 'ingreso/crear.html', context=context)

        except Exception as e:
            messages.error(request, f'Hubo un error al guardar los datos: {e}')
            return redirect('ingreso')
