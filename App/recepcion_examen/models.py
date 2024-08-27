from django.db import models

from App.agendar_hora.models import tipo_examen
from App.crear_cliente.models import usuario

# Create your models here.
class examenes (models.Model):
    class Meta:
        db_table = "examenes"
    cod_examen = models.IntegerField(blank=True, null=True, verbose_name="Cod examen", unique=True)
    n_examen = models.IntegerField(blank=True, null=True, verbose_name="Numero examen")
    usuario = models.ForeignKey(usuario, on_delete=models.RESTRICT, blank=True, null=True, verbose_name="Usuario",
                                to_field='usuario')
    rut = models.CharField(max_length=12, blank=True, null=True, verbose_name="Rut paciente")
    fecha_ingreso = models.DateField(null=True, blank=True, verbose_name="Fecha ingreso")
    nombre_paciente = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre paciente")
    valido = models.BooleanField(default=True, blank=True, null=True, verbose_name="Aprobado")
    responsable = models.CharField(max_length=100, blank=True, null=True, verbose_name="Responsable")
    telefono = models.IntegerField(null=True, blank=True, verbose_name="Telefono paciente")
    comentario = models.TextField(blank=True, null=True, verbose_name="Comentario", max_length=160)
    recepcionado = models.BooleanField(default=False, blank=True, null=True, verbose_name="Recepcionado")
    tipo_examen = models.ForeignKey(tipo_examen, on_delete=models.RESTRICT, blank=True, null=True,
                                        verbose_name="Tipo examen", to_field='cod_examen')
    fecha_recepcion = models.DateField(null=True, blank=True, verbose_name="Fecha recepcion")

class qr_examen(models.Model):
    class Meta:
        db_table = 'qr_examen'
    cod_encrip = models.TextField(blank=True, null=True, verbose_name="Encriptado", max_length=100)
    valido = models.BooleanField(default=None, blank=True, null=True, verbose_name="Valido")
    n_examen = models.IntegerField(blank=True, null=True, verbose_name="Numero examen")
    cod_examen = models.IntegerField(blank=True, null=True, verbose_name="Cod examen", unique=True)