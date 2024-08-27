from django.db import models
from App.crear_cliente.models import usuario
from App.crear_paquete.models import tipo_solicitud, paquete
from datetime import date, datetime
# Create your models here.

class tipo_examen(models.Model):
    class Meta:
        db_table = 'tipo_examen'
    cod_examen = models.CharField(max_length=50, unique=True, null=True, blank=True)
    descripcion = models.CharField(max_length=100, unique=True, null=True, blank=True)

class tipo_formulario(models.Model):
    class Meta:
        db_table = 'tipo_formulario'
    cod_formulario = models.CharField(max_length=50, unique=True, null=True, blank=True)
    descripcion = models.CharField(max_length=100, unique=True, null=True, blank=True)

class tipo_genero(models.Model):
    class Meta:
        db_table = 'tipo_genero'
    cod_genero = models.CharField(max_length=50, unique=True, null=True, blank=True)
    descripcion = models.CharField(max_length=100, unique=True, null=True, blank=True)


class solicitudes(models.Model):
    class Meta:
        db_table = 'solicitudes'

    cod_solicitud = models.IntegerField(blank=True, null=True, verbose_name="Cod solicitud",unique=True)
    n_solicitud = models.IntegerField(blank=True, null=True, verbose_name="Numero solicitud")
    usuario = models.ForeignKey(usuario, on_delete=models.RESTRICT, blank=True, null=True,verbose_name="Usuario", to_field='usuario')
    rut = models.CharField(max_length=12, blank=True, null=True,verbose_name="Rut solicitante")
    fecha_ingreso = models.DateField(null=True, blank=True, verbose_name="Fecha ingreso")
    nombre_solicitante = models.CharField(max_length=255, blank=True, null=True,verbose_name="Nombre solicitante")
    paquete = models.ForeignKey(paquete, on_delete=models.RESTRICT, blank=True, null=True,verbose_name="Paquete", to_field='cod_paquete')
    valido = models.BooleanField(default=True, blank=True, null=True,verbose_name="Aprobado")
    fecha_atencion = models.DateField(null=True, blank=True, verbose_name="Fecha atencion")
    hora_atencion = models.TimeField(null=True, blank=True, verbose_name="Hora atencion")
    responsable = models.CharField(max_length=100, blank=True, null=True,verbose_name="Responsable")
    telefono = models.IntegerField(null=True, blank=True,verbose_name="Telefono solicitante")
    tipo_solicitud = models.ForeignKey(tipo_solicitud, on_delete=models.RESTRICT, blank=True, null=True,verbose_name="Tipo solicitud", to_field='cod_tipo_solicitud')
    comentario = models.TextField(blank=True, null=True, verbose_name="Comentario", max_length=160)
    ingresado = models.BooleanField(default=True, blank=True, null=True, verbose_name="Ingreso")
    agendado = models.BooleanField(default=False, blank=True, null=True, verbose_name="Agendado")
    nombre_medico = models.CharField(max_length=50, blank=True, null=True,verbose_name="nombre_medico")
    direccion = models.TextField(blank=True, null=True, verbose_name="Direccion", max_length=100)
    edad = models.IntegerField(blank=True, null=True, verbose_name="Edad")
    tipo_formulario = models.TextField(blank=True, null=True, verbose_name="Formulario", max_length=100)
    tipo_examen = models.ForeignKey(tipo_examen, on_delete=models.RESTRICT, blank=True, null=True,verbose_name="Tipo examen", to_field='cod_examen')
    tipo_genero = models.ForeignKey(tipo_genero, on_delete=models.RESTRICT, blank=True, null=True,
                                    verbose_name="Tipo genero", to_field='cod_genero')

class qr_solicitudes(models.Model):
    class Meta:
        db_table = 'qr_solicitudes'
    cod_encrip = models.TextField(blank=True, null=True, verbose_name="Encriptado", max_length=100)
    valido = models.BooleanField(default=None, blank=True, null=True, verbose_name="Valido")
    n_solicitud = models.IntegerField(blank=True, null=True, verbose_name="Numero solicitud")


class RegistroAnulado(models.Model):
    class Meta:
        db_table = "RegistroAnulado"
    motivo_anulacion = models.TextField(max_length=255, verbose_name="Motivo de Anulación")
    fecha_anulacion = models.DateTimeField(default=datetime.today, verbose_name="Fecha de Anulación")
    responsable = models.TextField(null=True, blank=True, max_length=50, verbose_name="Nombre responsable")
    cod_id = models.ForeignKey('solicitudes', verbose_name="cod_id", null=True, blank=True, on_delete=models.CASCADE, to_field="id")

