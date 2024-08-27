from django.db import models
from datetime import date, datetime
# Create your models here.

class tipo_solicitud(models.Model):
    class Meta:
        db_table="tipo_solicitud"
    cod_tipo_solicitud = models.CharField(blank=False, null=False, max_length=5, verbose_name="Codigo tipo solicitud", unique=True)
    tipo_solicitud = models.TextField(blank=False, null=False, verbose_name="tipo de solicitud", max_length=100)
    empresa= models.BooleanField(default=False, blank=True, null=True, verbose_name="Empresa")
    mutual = models.BooleanField(default=False, blank=True, null=True, verbose_name="Mutual")

class tipo_prestacion(models.Model):
    class Meta:
        db_table = "tipo_prestacion"
    cod_tipo_prestacion = models.CharField(blank=False, null=False, max_length=5, verbose_name="Codigo tipo prestacion", unique=True)
    tipo_prestacion = models.TextField(blank=False, null=False, verbose_name="tipo de prestacion", max_length=100)
    cod_tipo_solicitud = models.ForeignKey(tipo_solicitud, on_delete=models.RESTRICT, blank=True, null=True, to_field='cod_tipo_solicitud')

class prestacion(models.Model):
    class Meta:
        db_table = "prestacion"
    cod_prestacion = models.CharField(blank=False, null=False, max_length=20, verbose_name="Codigo prestacion", unique=True)
    cod_fonasa = models.CharField(blank=True, null=True, max_length=20, verbose_name="Codigo fonasa")
    prestacion = models.TextField(blank=False, null=False, verbose_name="prestacion", max_length=100)
    cod_tipo_prestacion = models.ForeignKey(tipo_prestacion, on_delete=models.RESTRICT, blank=True, null=True, to_field='cod_tipo_prestacion')
    codigo_interno = models.CharField(max_length=12, blank=True, null=True, verbose_name="cod_interno")
    ingresado = models.BooleanField(null=True, blank=True, default=True, verbose_name="ingresado")


class paquete(models.Model):
    class Meta:
        db_table = "paquete"
    cod_paquete = models.CharField(blank=False, null=False, verbose_name="Codigo paquete", unique=True,max_length=100)
    nombre_paquete = models.TextField(blank=False, null=False, verbose_name="nombre_paquete", max_length=100)

class paquete_prestacion(models.Model):
    class Meta:
        db_table = "paquete_prestacion"
    cod_paquete = models.ForeignKey(paquete, on_delete=models.RESTRICT, blank=True, null=True, to_field='cod_paquete')
    cod_tipo_prestacion = models.ForeignKey(tipo_prestacion, on_delete=models.RESTRICT, blank=True, null=True, to_field='cod_tipo_prestacion')
    cod_prestacion = models.ForeignKey(prestacion, on_delete=models.RESTRICT, blank=True, null=True, to_field='cod_prestacion')


class Anulado(models.Model):
    class Meta:
        db_table = "Anulado"
    motivo_anulacion = models.TextField(max_length=255, verbose_name="Motivo de Anulación")
    fecha_anulacion = models.DateTimeField(default=datetime.today, verbose_name="Fecha de Anulación")
    responsable = models.TextField(null=True, blank=True, max_length=50, verbose_name="Nombre responsable")
    ingresar_prestacion = models.ForeignKey('prestacion', verbose_name="cod_prestacion", null=True, blank=True, on_delete=models.CASCADE, to_field="cod_prestacion")


