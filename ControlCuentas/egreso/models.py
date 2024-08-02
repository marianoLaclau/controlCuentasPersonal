from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User



class GastosVarios(models.Model):
    concepto = models.CharField(max_length=50,null=False,blank=False)
    monto = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self) :
        return self.concepto
    
class Servicios(models.Model):
    concepto = models.CharField(max_length=50,null=False,blank=False)
    monto = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self) :
        return self.concepto
    
class Deudas(models.Model):
    concepto = models.CharField(max_length=50,null=False,blank=False)
    monto = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self) :
        return self.concepto
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=50,null=False,blank=False)

    def __str__(self):
        return self.nombre
    
class Egreso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    concepto = models.CharField(max_length=50,null=False,blank=False)
    monto = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False)
    fecha = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.concepto


# Triggers
@receiver(post_save, sender=Egreso)
def agregar_a_categorias(sender, instance, **kwargs):
    categoria_nombre = instance.categoria.nombre

    if categoria_nombre == 'Servicio':
        Servicios.objects.create(concepto=instance.concepto, monto=instance.monto)
    elif categoria_nombre == 'Varios':
        GastosVarios.objects.create(concepto=instance.concepto, monto=instance.monto)
    elif categoria_nombre == 'Deudas(Credito-Tarjetas)':
        Deudas.objects.create(concepto=instance.concepto, monto=instance.monto)