import json
from datetime import datetime
from django.contrib import messages
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect,reverse
from django.utils import timezone
from django.db import transaction
from App.crear_paquete.models import tipo_prestacion, prestacion, paquete, paquete_prestacion, Anulado
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index_paquete(request):
    assert isinstance(request, HttpRequest)

    return render(request, 'crear_paquete/index.html')
def prestaciones_nuevas(request):
    assert isinstance(request, HttpRequest)
    tipo_p = tipo_prestacion.objects.all().order_by('tipo_prestacion')
    return render(
        request,
        'crear_paquete/prestaciones_nuevas.html',
        {
            'title': 'Crear Paquete',
            'year': datetime.now().year,
            'tipo_prestacion': tipo_p
        }
    )
@csrf_exempt
def crear_paquete(request):
    assert isinstance(request,HttpRequest)
    tipo_p = tipo_prestacion.objects.all().order_by('tipo_prestacion')
    return render(
        request,
        'crear_paquete/crear_paquete.html',
        {
            'title':'Crear Paquete',
            'year':datetime.now().year,
            'tipo_prestacion':tipo_p
        }
    )
@csrf_exempt
def filtro_tipo_prestacion(request, cod_tipo_prestacion):
    prestaciones = prestacion.objects.filter(cod_tipo_prestacion=cod_tipo_prestacion, ingresado=True).order_by('cod_prestacion')
    data_prestacion = list(prestaciones.values())
    return JsonResponse(data_prestacion, safe=False)
@csrf_exempt
def guardar_paquete(request):
    if request.method == 'POST':
        datos = json.loads(request.body)
        nombre_paquete = datos.get('nombrePaquete')
        datos_tabla = datos.get('datosTabla')

        try:
            ultimo_paquete = paquete.objects.last()
            if ultimo_paquete:
                nuevo_cod_paquete = str(int(ultimo_paquete.cod_paquete) + 1).zfill(2)
            else:
                nuevo_cod_paquete = '01'

            nuevo_paquete = paquete(
                cod_paquete = nuevo_cod_paquete,
                nombre_paquete = nombre_paquete
            )
            nuevo_paquete.save()

            for fila in datos_tabla:
                campo_tipo_prestacion = fila.get('campo_0')
                cod_prestacion = fila.get('campo_1')

                codigo_tipo_prestacion = tipo_prestacion.objects.get(tipo_prestacion=campo_tipo_prestacion)
                codigo_prestacion = prestacion.objects.get(cod_prestacion=cod_prestacion)

                datos_paquete_prestacion = paquete_prestacion(
                    cod_paquete=nuevo_paquete,
                    cod_tipo_prestacion=codigo_tipo_prestacion,
                    cod_prestacion=codigo_prestacion)
                datos_paquete_prestacion.save()

            return JsonResponse({'mensaje': 'El paquete se creó correctamente.'})
        except Exception as e:
            return JsonResponse({'error': f'Ocurrió un error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'La solicitud debe ser de tipo POST.'}, status=400)
@csrf_exempt
def paquete_existe(request,nombre_paquete_modal):
    try:
        paquete_existente = paquete.objects.filter(nombre_paquete__icontains=nombre_paquete_modal)
        data = list(paquete_existente.values())
        return JsonResponse(data, safe=False)
    except Exception as e:
        messages.error(request, f'Ocurrio un error, no se pudo validar si el paquete existe: {str(e)}')
        return JsonResponse({'success': False, 'error_message': str(e)})
@csrf_exempt
def nuevaPrestacion(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.POST.get('datosJson', '{}'))
            nombre_prestacion = datos.get('nombrePrestacion', '').upper()
            tipo_prestacion_id = datos.get('tipoPrestacion', '')
            cod_interno = datos.get('cod_interno', '').upper()
            cod_fonasa = datos.get('cod_fonasa', '').upper()

            with transaction.atomic():
                ultima_prestacion = prestacion.objects.order_by('-id').first()
                nuevo_id = ultima_prestacion.id + 1 if ultima_prestacion else 1

                nueva_prestacion = prestacion(
                    cod_prestacion=nuevo_id,
                    prestacion=nombre_prestacion,
                    cod_tipo_prestacion_id=tipo_prestacion_id,
                    codigo_interno=cod_interno,
                    cod_fonasa=cod_fonasa
                )
                nueva_prestacion.save()

            messages.success(request, 'Prestación ha sido agregada correctamente.')
        except Exception as e:
            messages.error(request, str(e))

    return HttpResponseRedirect(reverse("prestaciones_nuevas"))
@csrf_exempt
def editar(request):
    if request.method == 'POST':
        datos = request.POST.get('datosEditar', '{}')
        datos_antes = request.POST.get('datosAntes', '{}')

        datos_antes_dict = json.loads(datos_antes)
        print(datos_antes_dict)
        prestacion_nombre_antes = datos_antes_dict.get('nombre', '')
        interno_cod_antes = datos_antes_dict.get('cod_interno', '')
        fonasa_cod_antes = datos_antes_dict.get('cod_fonasa', '')

        datos_dict = json.loads(datos)
        print(datos_dict)
        nombre_prestacion = datos_dict.get('nombrePrestacion', '').upper()
        cod_interno = datos_dict.get('cod_interno', '').upper()
        cod_fonasa = datos_dict.get('cod_fonasa', '').upper()
        print(cod_fonasa)

        mensaje_error = mensaje_exito = None

        prestacion.objects.filter(cod_fonasa=fonasa_cod_antes).update(cod_fonasa=cod_fonasa)
        prestacion.objects.filter(prestacion=prestacion_nombre_antes).update(prestacion=nombre_prestacion)
        prestacion.objects.filter(codigo_interno=interno_cod_antes).update(codigo_interno=cod_interno)

        mensaje_exito = 'Los datos han sido cambiados correctamente.'

        if mensaje_error:
            messages.error(request, mensaje_error)
        elif mensaje_exito:
            messages.success(request, mensaje_exito)

        return HttpResponseRedirect(reverse("crear_paquete"))
@csrf_exempt
def anulado(request):
    if request.method == 'POST':
        try:
            motivo = request.POST.get('motivo_anulacion', '')
            anulado_data = request.POST.get('anular', '')

            codigo_dict = json.loads(anulado_data)
            codigo = codigo_dict.get('codigo_prestacion', '')

            prestacion_obj = prestacion.objects.get(cod_prestacion=codigo)

            prestacion_obj.ingresado = False
            prestacion_obj.save()

            registro_anulado = Anulado.objects.create(
                motivo_anulacion=motivo,
                fecha_anulacion=timezone.now(),
                responsable=request.user.username if request.user.is_authenticated else None,
                ingresar_prestacion=prestacion_obj,
            )
            registro_anulado.save()

            messages.success(request, 'La prestación se ha anulado correctamente.')

            return HttpResponseRedirect(reverse("crear_paquete"))

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return HttpResponseRedirect(reverse("crear_paquete"))
@csrf_exempt
def filtrocod_interno(request, codigo_interno ):
    datos_codigo_interno = prestacion.objects.filter(codigo_interno__iexact=codigo_interno)
    data = list(datos_codigo_interno.values())
    return JsonResponse(data, safe=False)


@csrf_exempt
def filtronombPrestacion(request, nombre_prestacion):
    datos_prestacion = prestacion.objects.filter(prestacion__iexact=nombre_prestacion)
    data = list(datos_prestacion.values())
    return JsonResponse(data, safe=False)

@csrf_exempt
def filtrocod_fonasa(request, cod_fonasa):
    datos_codigo_fonasa = prestacion.objects.filter(cod_fonasa__iexact=cod_fonasa)
    data = list(datos_codigo_fonasa.values())
    return JsonResponse(data, safe=False)


