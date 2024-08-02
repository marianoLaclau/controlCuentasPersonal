from django.forms import ModelForm
from .models import  Ahorro


class FormAhorro(ModelForm):
    class Meta:
        model = Ahorro
        exclude = ['usuario']

    