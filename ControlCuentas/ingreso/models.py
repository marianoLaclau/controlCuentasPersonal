from django.db import models
from django.contrib.auth.models import User




class Categoria(models.Model):
    nombre = models.CharField(max_length = 50, null = False, blank = False)

    def __str__(self):
        return self.nombre
    


class Ingreso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False)
    fecha = models.DateField(auto_now_add = True)
    
    def __str__(self):
        return self.categoria.nombre
    