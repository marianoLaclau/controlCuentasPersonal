from django.forms import ModelForm
from .models import Ingreso


class IngresoForm(ModelForm):
    class Meta:
        model = Ingreso
        exclude = ['usuario']

    