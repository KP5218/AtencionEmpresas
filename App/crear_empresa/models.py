from django.db import models

# Create your models here.
class mutualidades(models.Model):
    class Meta:
        db_table = 'mutualidades'
    cod_mutual = models.CharField(max_length=50, unique=True, null=True, blank=True,verbose_name="Codigo mutual")
    nombre_mutual = models.TextField(max_length=100, null=True, blank=True, verbose_name="Nombre mutual")
    rut = models.TextField(max_length=100, null=True, blank=True, verbose_name="Rut")
    direccion = models.TextField(max_length=100, null=True, blank=True, verbose_name="Direccion")
    telefono = models.TextField(max_length=100, null=True, blank=True, verbose_name="Telefono")

class empresa(models.Model):
    class Meta:
        db_table = 'empresa'
    cod_empresa = models.CharField(max_length=50, unique=True, null=True, blank=True,verbose_name="Codigo empresa")
    nombre_empresa = models.TextField(max_length=100, null=True, blank=True, verbose_name="Nombre empresa")
    mutualidad = models.ForeignKey(mutualidades, on_delete=models.RESTRICT, blank=True, null=True,verbose_name="mutual", to_field='cod_mutual')
    rut = models.TextField(max_length=100, null=True, blank=True, verbose_name="Rut")
    direccion = models.TextField(max_length=100, null=True, blank=True, verbose_name="Direccion")
    telefono = models.TextField(max_length=100, null=True, blank=True, verbose_name="Telefono")

class utms(models.Model):
    class Meta:
        db_table = 'utms'
    cod_utms = models.CharField(max_length=50, unique=True, null=True, blank=True,verbose_name="Codigo utms")
    nombre_utms = models.TextField(max_length=100, null=True, blank=True, verbose_name="Nombre utms")
    rut = models.TextField(max_length=100, null=True, blank=True, verbose_name="Rut")
    direccion = models.TextField(max_length=100, null=True, blank=True, verbose_name="Direccion")
    telefono = models.TextField(max_length=100, null=True, blank=True, verbose_name="Telefono")

class tipo_organizacion(models.Model):
    class Meta:
        db_table = 'tipo_organizacion'
    cod_tipo = models.CharField(max_length=50, unique=True, null=True, blank=True,verbose_name="Codigo tipo")
    nombre_tipo = models.TextField(max_length=250, null=True, blank=True, verbose_name="Nombre tipo")


