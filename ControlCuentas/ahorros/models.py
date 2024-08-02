from django.db import models
from django.contrib.auth.models import User


class TipoAhorro(models.Model):
    tipo = models.CharField(max_length=50,null=False,blank=False)

    def __str__(self):
        return self.tipo
    

class Ahorro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoAhorro,on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False)
    fecha = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.tipo.tipo
    