from django.db import models
from App.crear_empresa.models import empresa, mutualidades, utms


# Create your models here.
class usuario(models.Model):
    class Meta:
        db_table = 'usuario'
    usuario = models.CharField(max_length=50, unique=True)
    clave = models.CharField(max_length=255)
    nombre = models.CharField(max_length=100)
    rut = models.TextField(max_length=100, null=True, blank=True, verbose_name="Rut")
    empresa = models.ForeignKey(empresa, on_delete=models.RESTRICT, blank=True, null=True,verbose_name="Empresa", to_field='cod_empresa')
    mutualidad = models.ForeignKey(mutualidades, on_delete=models.RESTRICT, blank=True, null=True, verbose_name="Mutualidad",to_field='cod_mutual')
    utm = models.ForeignKey(utms, on_delete=models.RESTRICT, blank=True, null=True,verbose_name="Utms", to_field='cod_utms')