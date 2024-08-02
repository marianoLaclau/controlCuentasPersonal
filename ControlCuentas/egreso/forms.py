from django.forms import ModelForm
from .models import Egreso


class EgresoForm(ModelForm):
    class Meta:
        model = Egreso
        exclude = ['usuario']

    #Normalizar los datos antes de almacenarlos
    def clean_concepto(self):
        concepto = self.cleaned_data['concepto']
        concepto = concepto.title()
        concepto = concepto.replace(' ', '')
        return concepto