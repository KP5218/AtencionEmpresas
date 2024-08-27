from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.http import HttpRequest
from django.shortcuts import render, reverse
import json
from django.views.decorators.csrf import csrf_exempt
from App.recepcion_examen.models import examenes
from django.contrib import messages
@login_required
def recepcion_examen(request):
    assert isinstance(request,HttpRequest)
    return render(
        request,
        'recepcion_examen/recepcion_examen.html',
        {
            'title':'Agendar Hora',
            'year':datetime.now().year,
        }
    )

@csrf_exempt
def filtroCodigo(request):
    if request.method == 'POST':
        codigo_busqueda = request.POST.get('busquedaCodigo')

        datos_filtrados_codigo = examenes.objects.filter(cod_examen=codigo_busqueda)

        solicitudes = examenes.objects.filter(recepcionado=False)

        datos_filtrados = datos_filtrados_codigo & solicitudes

        if datos_filtrados.exists():
            datos_json = []
            for examen in datos_filtrados:
                codigo = examen.cod_examen or "_"
                rut = examen.rut or "—"
                nombre_solicitante = examen.nombre_paciente or "—"
                telefono = examen.telefono or "—"
                tipo_examen = examen.tipo_examen.descripcion or "—"
                fecha = examen.fecha_ingreso.strftime('%Y-%m-%d %H:%M:%S')
                solicitante = examen.usuario.nombre or "—"

                solicitud_dict = {
                    "codigo": codigo,
                    "rut": rut,
                    "nombre_solicitante": nombre_solicitante,
                    "telefono": telefono,
                    "tipo_examen": tipo_examen,
                    "fecha": fecha,
                    "solicitante": solicitante,

                }

                datos_json.append(solicitud_dict)

            solicitudes_data = json.dumps(datos_json)

            context = {
                'title': 'solicitud',
                'year': datetime.now().year,
                'list_datos': datos_json,
                'solicitudes_data': solicitudes_data,
            }

            return JsonResponse({'data': datos_json})
        else:
            return JsonResponse({'error': 'No se encontraron datos'})

    return JsonResponse({'error': 'La solicitud debe ser de tipo POST'})

@csrf_exempt
def filtroFecha(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fechaInicio')
        fecha_fin = request.POST.get('fechaFin')

        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

        datos_filtrados_por_fecha = examenes.objects.filter(fecha_ingreso__range=[fecha_inicio, fecha_fin])

        solicitudes = datos_filtrados_por_fecha.filter(recepcionado=False)

        if solicitudes.exists():
            datos_json = []
            for examen in solicitudes:
                codigo = examen.cod_examen or "_"
                rut = examen.rut or "—"
                nombre_solicitante = examen.nombre_paciente or "—"
                telefono = examen.telefono or "—"
                tipo_examen = examen.tipo_examen.descripcion or "—"
                fecha = examen.fecha_ingreso.strftime('%Y-%m-%d %H:%M:%S')
                solicitante = examen.usuario.nombre or "—"

                solicitud_dict = {
                    "codigo": codigo,
                    "rut": rut,
                    "nombre_solicitante": nombre_solicitante,
                    "telefono": telefono,
                    "tipo_examen": tipo_examen,
                    "fecha": fecha,
                    "solicitante": solicitante,

                }

                datos_json.append(solicitud_dict)

            return JsonResponse({'data': datos_json})
        else:
            return JsonResponse({'error': 'No se encontraron solicitudes para este rango de fechas.'})

    return JsonResponse({'error': 'Método no permitido'})

@csrf_exempt
def filtroRut(request):
    if request.method == 'POST':
        rut_busqueda = request.POST.get('busquedaRut')

        datos_filtrados_rut = examenes.objects.filter(rut=rut_busqueda)

        solicitudes = examenes.objects.filter(recepcionado=False)

        datos_filtrados = datos_filtrados_rut & solicitudes

        if datos_filtrados.exists():
            datos_json = []
            for examen in datos_filtrados:
                codigo = examen.cod_examen or "_"
                rut = examen.rut or "—"
                nombre_solicitante = examen.nombre_paciente or "—"
                telefono = examen.telefono or "—"
                tipo_examen = examen.tipo_examen.descripcion or "—"
                fecha = examen.fecha_ingreso.strftime('%Y-%m-%d %H:%M:%S')
                solicitante = examen.usuario.nombre or "—"

                solicitud_dict = {
                    "codigo": codigo,
                    "rut": rut,
                    "nombre_solicitante": nombre_solicitante,
                    "telefono": telefono,
                    "tipo_examen": tipo_examen,
                    "fecha": fecha,
                    "solicitante": solicitante,

                }

                datos_json.append(solicitud_dict)

            solicitudes_data = json.dumps(datos_json)

            context = {
                'title': 'solicitud',
                'year': datetime.now().year,
                'list_datos': datos_json,
                'solicitudes_data': solicitudes_data,
            }

            return JsonResponse({'data': datos_json})
        else:
            return JsonResponse({'error': 'No se encontraron datos'})

    return JsonResponse({'error': 'La solicitud debe ser de tipo POST'})

@csrf_exempt
def filtro_n_examen(request):
    if request.method == 'POST':
        nExamen_busqueda = request.POST.get('busquedaNexamen')

        datos_filtrados_numero = examenes.objects.filter(n_examen=nExamen_busqueda)

        solicitudes = examenes.objects.filter(recepcionado=False)

        datos_filtrados = datos_filtrados_numero & solicitudes

        if datos_filtrados.exists():
            datos_json = []
            for examen in datos_filtrados:
                codigo = examen.cod_examen or "_"
                rut = examen.rut or "—"
                nombre_solicitante = examen.nombre_paciente or "—"
                telefono = examen.telefono or "—"
                tipo_examen = examen.tipo_examen.descripcion or "—"
                fecha = examen.fecha_ingreso.strftime('%Y-%m-%d %H:%M:%S')
                solicitante = examen.usuario.nombre or "—"

                solicitud_dict = {
                    "codigo": codigo,
                    "rut": rut,
                    "nombre_solicitante": nombre_solicitante,
                    "telefono": telefono,
                    "tipo_examen": tipo_examen,
                    "fecha": fecha,
                    "solicitante": solicitante,

                }

                datos_json.append(solicitud_dict)

            solicitudes_data = json.dumps(datos_json)

            context = {
                'title': 'solicitud',
                'year': datetime.now().year,
                'list_datos': datos_json,
                'solicitudes_data': solicitudes_data,
            }

            return JsonResponse({'data': datos_json})
        else:
            return JsonResponse({'error': 'No se encontraron datos'})

    return JsonResponse({'error': 'La solicitud debe ser de tipo POST'})

@csrf_exempt
def filtro_nombre_Utm(request):
    if request.method == 'POST':
        Nombre_busqueda = request.POST.get('busquedaNomUtm')

        datos_filtrados_nombre = examenes.objects.filter(usuario__utm_id__nombre_utms=Nombre_busqueda)

        solicitudes_agendadas = examenes.objects.filter(recepcionado=False)

        datos_filtrados = datos_filtrados_nombre & solicitudes_agendadas

        if datos_filtrados.exists():
            datos_json = []
            for examen in datos_filtrados:
                codigo = examen.cod_examen or "_"
                rut = examen.rut or "—"
                nombre_solicitante = examen.nombre_paciente or "—"
                telefono = examen.telefono or "—"
                tipo_examen = examen.tipo_examen.descripcion or "—"
                fecha = examen.fecha_ingreso.strftime('%Y-%m-%d %H:%M:%S')
                solicitante = examen.usuario.nombre or "—"

                solicitud_dict = {
                    "codigo": codigo,
                    "rut": rut,
                    "nombre_solicitante": nombre_solicitante,
                    "telefono": telefono,
                    "tipo_examen": tipo_examen,
                    "fecha": fecha,
                    "solicitante": solicitante,

                }

                datos_json.append(solicitud_dict)

            solicitudes_data = json.dumps(datos_json)

            context = {
                'title': 'solicitud',
                'year': datetime.now().year,
                'list_datos': datos_json,
                'solicitudes_data': solicitudes_data,
            }

            return JsonResponse({'data': datos_json})
        else:
            return JsonResponse({'error': 'No se encontraron datos'})

    return JsonResponse({'error': 'La solicitud debe ser de tipo POST'})

def Enviar(request):
    if request.method == 'POST':
        checkboxJson = request.POST.get('checkbox')
        fecha_actual = datetime.now()

        checkboxJson = json.loads(checkboxJson) if checkboxJson else []

        for datos in checkboxJson:
            codigo = datos.get('examenCodigo')
            ischecked = datos.get('isChecked')
            if ischecked:
                try:
                    examen = examenes.objects.get(cod_examen=codigo)
                    examen.recepcionado = True
                    examen.fecha_recepcion = fecha_actual
                    examen.save()
                except examenes.DoesNotExist:
                    messages.warning(request, f'El examen con código {codigo} no existe.')
            else:
                messages.info(request, f'El examen con código {codigo} no fue recepcionado correctamente".')

        messages.success(request, 'Exámenes recepcionados correctamente.')
        return HttpResponseRedirect(reverse("inicio_recepcion_examen"))
    else:
        return HttpResponse('Error: Esta vista solo acepta peticiones POST.')