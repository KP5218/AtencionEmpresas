from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.http import HttpRequest
from django.shortcuts import render, reverse
from App.agendar_hora.models import solicitudes
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Max
from django.db.models import Q
import urllib
from urllib.error import HTTPError, URLError

@login_required
def agenda_hora(request):
    assert isinstance(request,HttpRequest)
    return render(
        request,
        'agenda_hora/agenda_hora.html',
        {
            'title':'Agendar Hora',
            'year':datetime.now().year,
        }
    )

@csrf_exempt
def filtroRut(request):
    if request.method == 'POST':
        rut_busqueda = request.POST.get('busquedaRut')
        print(rut_busqueda)

        datos_filtrados_rut = solicitudes.objects.filter(rut=rut_busqueda)

        solicitudes_agendadas = solicitudes.objects.filter(agendado__isnull=True)

        grupos_usuario = request.user.groups.all()
        filters = Q()
        for grupo in grupos_usuario:
            if grupo.name == 'Urgencia':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='02')
            elif grupo.name == 'Preventivo':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='01')
            elif grupo.name == 'Hospitalario':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='03')
            elif grupo.name == 'Consultas':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='04')
            elif grupo.name == 'Examenes':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='05')

        if filters:
            datos_filtrados = datos_filtrados_rut.filter(filters) & solicitudes_agendadas
        else:
            datos_filtrados = datos_filtrados_rut & solicitudes_agendadas

        if datos_filtrados.exists():
            datos_json = []
            for solicitud in datos_filtrados:
                nombre_solicitante = solicitud.nombre_solicitante or "—"
                telefono = solicitud.telefono or "—"
                rut = solicitud.rut or "—"
                responsable = solicitud.usuario.nombre or "—"

                empresa = solicitud.usuario.empresa.nombre_empresa if solicitud.usuario and solicitud.usuario.empresa else "—"
                mutualidad = solicitud.usuario.mutualidad.nombre_mutual if solicitud.usuario and solicitud.usuario.mutualidad else "—"

                paquete = solicitud.paquete.nombre_paquete if solicitud.paquete and solicitud.paquete.nombre_paquete else "—"
                id_solicitud = solicitud.id
                tipo_solicitud_nombre = solicitud.tipo_solicitud.tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.tipo_solicitud else "—"
                tipo_solicitud_cod = solicitud.tipo_solicitud.cod_tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.cod_tipo_solicitud else "—"

                solicitud_dict = {
                    "id": id_solicitud,
                    "nombre_solicitante": nombre_solicitante,
                    "telefono": telefono,
                    "rut": rut,
                    "responsable": responsable,
                    "empresa": empresa,
                    "mutualidad": mutualidad,
                    "paquete": paquete,
                    "tipo_solicitud": {
                        "cod_tipo_solicitud": tipo_solicitud_cod,
                        "tipo_solicitud": tipo_solicitud_nombre
                    }
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
            return render(request, 'agenda_hora/agenda_hora.html', {'title': 'solicitud', 'year': datetime.now().year})

    context = {
        'title': 'solicitud',
        'year': datetime.now().year,
    }
    return render(request, 'agenda_hora/agenda_hora.html', context)

@csrf_exempt
def filtroPreventiva(request):
    if request.method == 'POST':
        paquete = request.POST.get('busquedaPreventivo')

        datos_filtrados_paquete = solicitudes.objects.filter(paquete__nombre_paquete=paquete)

        solicitudes_agendadas = solicitudes.objects.filter(agendado__isnull=True)

        datos_filtrados = datos_filtrados_paquete & solicitudes_agendadas

        grupos_usuario = request.user.groups.all()

        filters = Q()
        for grupo in grupos_usuario:
            if grupo.name == 'Urgencia':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='02')
            elif grupo.name == 'Preventivo':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='01')
            elif grupo.name == 'Hospitalario':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='03')
            elif grupo.name == 'Consultas':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='04')
            elif grupo.name == 'Examenes':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='05')

        if filters:
            datos_filtrados = datos_filtrados.filter(filters)

        if datos_filtrados.exists():
            datos_json = []
            for solicitud in datos_filtrados:
                nombre_solicitante = solicitud.nombre_solicitante or "—"
                telefono = solicitud.telefono or "—"
                rut = solicitud.rut or "—"
                responsable = solicitud.usuario.nombre or "—"

                empresa = solicitud.usuario.empresa.nombre_empresa if solicitud.usuario and solicitud.usuario.empresa else "—"
                mutualidad = solicitud.usuario.mutualidad.nombre_mutual if solicitud.usuario and solicitud.usuario.mutualidad else "—"

                paquete = solicitud.paquete.nombre_paquete if solicitud.paquete and solicitud.paquete.nombre_paquete else "—"
                id_solicitud = solicitud.id
                tipo_solicitud_nombre = solicitud.tipo_solicitud.tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.tipo_solicitud else "—"
                tipo_solicitud_cod = solicitud.tipo_solicitud.cod_tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.cod_tipo_solicitud else "—"

                solicitud_dict = {
                    "id": id_solicitud,
                    "nombre_solicitante": nombre_solicitante,
                    "telefono": telefono,
                    "rut": rut,
                    "responsable": responsable,
                    "empresa": empresa,
                    "mutualidad": mutualidad,
                    "paquete": paquete,
                    "tipo_solicitud": {
                        "cod_tipo_solicitud": tipo_solicitud_cod,
                        "tipo_solicitud": tipo_solicitud_nombre
                    }
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
            return render(request, 'agenda_hora/agenda_hora.html', {'title': 'solicitud', 'year': datetime.now().year})

    context = {
        'title': 'solicitud',
        'year': datetime.now().year,
    }
    return render(request, 'agenda_hora/agenda_hora.html', context)

@csrf_exempt
def filtroEmpresa(request):
    if request.method == 'POST':
        empresa = request.POST.get('busquedaEmpresa')

        datos_filtrados_empresa = solicitudes.objects.filter(usuario__empresa__nombre_empresa=empresa) | solicitudes.objects.filter(usuario__mutualidad__nombre_mutual=empresa)

        solicitudes_agendadas = datos_filtrados_empresa.filter(agendado__isnull=True)

        grupos_usuario = request.user.groups.all()

        # Filtros para cada tipo de usuario
        filters = Q()
        for grupo in grupos_usuario:
            if grupo.name == 'Urgencia':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='02')
            elif grupo.name == 'Preventivo':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='01')
            elif grupo.name == 'Hospitalario':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='03')
            elif grupo.name == 'Consultas':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='04')
            elif grupo.name == 'Examenes':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='05')

        # Aplicar los filtros de usuario
        if filters:
            solicitudes_agendadas = solicitudes_agendadas.filter(filters)

        if solicitudes_agendadas.exists():
            datos_json = []
            for solicitud in solicitudes_agendadas:
                # Obtener datos de la solicitud
                nombre_solicitante = solicitud.nombre_solicitante or "—"
                telefono = solicitud.telefono or "—"
                rut = solicitud.rut or "—"
                responsable = solicitud.usuario.nombre or "—"

                empresa = solicitud.usuario.empresa.nombre_empresa if solicitud.usuario and solicitud.usuario.empresa else "—"
                mutualidad = solicitud.usuario.mutualidad.nombre_mutual if solicitud.usuario and solicitud.usuario.mutualidad else "—"

                paquete = solicitud.paquete.nombre_paquete if solicitud.paquete and solicitud.paquete.nombre_paquete else "—"
                id_solicitud = solicitud.id
                tipo_solicitud_nombre = solicitud.tipo_solicitud.tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.tipo_solicitud else "—"
                tipo_solicitud_cod = solicitud.tipo_solicitud.cod_tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.cod_tipo_solicitud else "—"

                solicitud_dict = {
                    "id": id_solicitud,
                    "nombre_solicitante": nombre_solicitante,
                    "telefono": telefono,
                    "rut": rut,
                    "responsable": responsable,
                    "empresa": empresa,
                    "mutualidad": mutualidad,
                    "paquete": paquete,
                    "tipo_solicitud": {
                        "cod_tipo_solicitud": tipo_solicitud_cod,
                        "tipo_solicitud": tipo_solicitud_nombre
                    }
                }

                datos_json.append(solicitud_dict)

            solicitudes_data = json.dumps(datos_json)

            return JsonResponse({'data': datos_json})
        else:
            return JsonResponse({'data': []})
    else:
        context = {
            'title': 'solicitud',
            'year': datetime.now().year,
        }
        return render(request, 'agenda_hora/agenda_hora.html', context)

@csrf_exempt
def filtroFecha(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fechaInicio')
        fecha_fin = request.POST.get('fechaFin')

        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

        datos_filtrados_por_fecha = solicitudes.objects.filter(fecha_ingreso__range=[fecha_inicio, fecha_fin])

        solicitudes_agendadas = datos_filtrados_por_fecha.filter(agendado__isnull=True)

        grupos_usuario = request.user.groups.all()
        filters = Q()
        for grupo in grupos_usuario:
            if grupo.name == 'Urgencia':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='02')
            elif grupo.name == 'Preventivo':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='01')
            elif grupo.name == 'Hospitalario':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='03')
            elif grupo.name == 'Consultas':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='04')
            elif grupo.name == 'Examenes':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='05')

        if filters:
            solicitudes_agendadas = solicitudes_agendadas.filter(filters)

        if solicitudes_agendadas.exists():
            datos_json = []
            for solicitud in solicitudes_agendadas:
                nombre_solicitante = solicitud.nombre_solicitante or "—"
                telefono = solicitud.telefono or "—"
                rut = solicitud.rut or "—"
                responsable = solicitud.usuario.nombre or "—"
                fecha = solicitud.fecha_ingreso.strftime('%Y-%m-%d %H:%M:%S')

                empresa = solicitud.usuario.empresa.nombre_empresa if solicitud.usuario and solicitud.usuario.empresa else "—"
                mutualidad = solicitud.usuario.mutualidad.nombre_mutual if solicitud.usuario and solicitud.usuario.mutualidad else "—"

                paquete = solicitud.paquete.nombre_paquete if solicitud.paquete and solicitud.paquete.nombre_paquete else "—"
                id_solicitud = solicitud.id
                tipo_solicitud_nombre = solicitud.tipo_solicitud.tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.tipo_solicitud else "—"
                tipo_solicitud_cod = solicitud.tipo_solicitud.cod_tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.cod_tipo_solicitud else "—"

                solicitud_dict = {
                    "id": id_solicitud,
                    "nombre_solicitante": nombre_solicitante,
                    "telefono": telefono,
                    "rut": rut,
                    "responsable": responsable,
                    "empresa": empresa,
                    "mutualidad": mutualidad,
                    "paquete": paquete,
                    "fecha": fecha,
                    "tipo_solicitud": {
                        "cod_tipo_solicitud": tipo_solicitud_cod,
                        "tipo_solicitud": tipo_solicitud_nombre
                    }
                }

                datos_json.append(solicitud_dict)

            return JsonResponse({'data': datos_json})
        else:
            return JsonResponse({'error': 'No se encontraron solicitudes para este rango de fechas.'})

    return JsonResponse({'error': 'Método no permitido'})

@csrf_exempt
def filtroUrgencia(request):
    if request.method == 'POST':
        cod_tipo_solicitud = '02'

        datos_filtrados_urgencias = solicitudes.objects.filter(tipo_solicitud__cod_tipo_solicitud=cod_tipo_solicitud)

        solicitudes_agendadas = datos_filtrados_urgencias.filter(agendado__isnull=True)

        grupos_usuario = request.user.groups.all()

        filters = Q()
        for grupo in grupos_usuario:
            if grupo.name == 'Urgencia':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='02')
            elif grupo.name == 'Preventivo':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='01')
            elif grupo.name == 'Hospitalario':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='03')
            elif grupo.name == 'Consultas':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='04')
            elif grupo.name == 'Examenes':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='05')

        if filters:
            solicitudes_agendadas = solicitudes_agendadas.filter(filters)

        if solicitudes_agendadas.exists():
            datos_json = []
            for solicitud in solicitudes_agendadas:
                nombre_solicitante = solicitud.nombre_solicitante or "—"
                telefono = solicitud.telefono or "—"
                rut = solicitud.rut or "—"
                responsable = solicitud.usuario.nombre or "—"
                fecha = solicitud.fecha_ingreso.strftime('%Y-%m-%d %H:%M:%S')

                empresa = solicitud.usuario.empresa.nombre_empresa if solicitud.usuario and solicitud.usuario.empresa else "—"
                mutualidad = solicitud.usuario.mutualidad.nombre_mutual if solicitud.usuario and solicitud.usuario.mutualidad else "—"

                paquete = solicitud.paquete.nombre_paquete if solicitud.paquete and solicitud.paquete.nombre_paquete else "—"
                id_solicitud = solicitud.id
                tipo_solicitud_nombre = solicitud.tipo_solicitud.tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.tipo_solicitud else "—"
                tipo_solicitud_cod = solicitud.tipo_solicitud.cod_tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.cod_tipo_solicitud else "—"

                solicitud_dict = {
                    "id": id_solicitud,
                    "nombre_solicitante": nombre_solicitante,
                    "telefono": telefono,
                    "rut": rut,
                    "responsable": responsable,
                    "empresa": empresa,
                    "mutualidad": mutualidad,
                    "paquete": paquete,
                    "fecha": fecha,
                    "tipo_solicitud": {
                        "cod_tipo_solicitud": tipo_solicitud_cod,
                        "tipo_solicitud": tipo_solicitud_nombre
                    }
                }

                datos_json.append(solicitud_dict)

            return JsonResponse({'data': datos_json})
        else:
            return JsonResponse({'error': 'No se encontraron solicitudes de urgencias agendadas'})

    return JsonResponse({'error': 'Método no permitido'})

@csrf_exempt
def filtroHospitalario(request):
    if request.method == 'POST':
        cod_tipo_solicitud = '03'

        datos_filtrados_hospitalario = solicitudes.objects.filter(tipo_solicitud__cod_tipo_solicitud=cod_tipo_solicitud)

        solicitudes_agendadas = datos_filtrados_hospitalario.filter(agendado__isnull=True)

        grupos_usuario = request.user.groups.all()

        filters = Q()
        for grupo in grupos_usuario:
            if grupo.name == 'Urgencia':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='02')
            elif grupo.name == 'Preventivo':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='01')
            elif grupo.name == 'Hospitalario':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='03')
            elif grupo.name == 'Consultas':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='04')
            elif grupo.name == 'Examenes':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='05')

        if filters:
            solicitudes_agendadas = solicitudes_agendadas.filter(filters)

        if solicitudes_agendadas.exists():
            datos_json = []
            for solicitud in solicitudes_agendadas:
                nombre_solicitante = solicitud.nombre_solicitante or "—"
                telefono = solicitud.telefono or "—"
                rut = solicitud.rut or "—"
                responsable = solicitud.usuario.nombre or "—"
                fecha = solicitud.fecha_ingreso.strftime('%Y-%m-%d %H:%M:%S')

                empresa = solicitud.usuario.empresa.nombre_empresa if solicitud.usuario and solicitud.usuario.empresa else "—"
                mutualidad = solicitud.usuario.mutualidad.nombre_mutual if solicitud.usuario and solicitud.usuario.mutualidad else "—"

                paquete = solicitud.paquete.nombre_paquete if solicitud.paquete and solicitud.paquete.nombre_paquete else "—"
                id_solicitud = solicitud.id
                tipo_solicitud_nombre = solicitud.tipo_solicitud.tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.tipo_solicitud else "—"
                tipo_solicitud_cod = solicitud.tipo_solicitud.cod_tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.cod_tipo_solicitud else "—"

                solicitud_dict = {
                    "id": id_solicitud,
                    "nombre_solicitante": nombre_solicitante,
                    "telefono": telefono,
                    "rut": rut,
                    "responsable": responsable,
                    "empresa": empresa,
                    "mutualidad": mutualidad,
                    "paquete": paquete,
                    "fecha": fecha,
                    "tipo_solicitud": {
                        "cod_tipo_solicitud": tipo_solicitud_cod,
                        "tipo_solicitud": tipo_solicitud_nombre
                    }
                }

                datos_json.append(solicitud_dict)

            return JsonResponse({'data': datos_json})
        else:
            return JsonResponse({'error': 'No se encontraron solicitudes hospitalarias agendadas'})

    return JsonResponse({'error': 'Método no permitido'})

@csrf_exempt
def filtroConsultas(request):
    if request.method == 'POST':
        cod_tipo_solicitud = '04'

        datos_filtrados_consultas = solicitudes.objects.filter(tipo_solicitud__cod_tipo_solicitud=cod_tipo_solicitud)

        solicitudes_agendadas = datos_filtrados_consultas.filter(agendado__isnull=True)

        grupos_usuario = request.user.groups.all()

        filters = Q()
        for grupo in grupos_usuario:
            if grupo.name == 'Urgencia':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='02')
            elif grupo.name == 'Preventivo':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='01')
            elif grupo.name == 'Hospitalario':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='03')
            elif grupo.name == 'Consultas':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='04')
            elif grupo.name == 'Examenes':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='05')

        if filters:
            solicitudes_agendadas = solicitudes_agendadas.filter(filters)

        if solicitudes_agendadas.exists():
            datos_json = []
            for solicitud in solicitudes_agendadas:
                nombre_solicitante = solicitud.nombre_solicitante or "—"
                telefono = solicitud.telefono or "—"
                rut = solicitud.rut or "—"
                responsable = solicitud.usuario.nombre or "—"
                fecha = solicitud.fecha_ingreso.strftime('%Y-%m-%d %H:%M:%S')

                empresa = solicitud.usuario.empresa.nombre_empresa if solicitud.usuario and solicitud.usuario.empresa else "—"
                mutualidad = solicitud.usuario.mutualidad.nombre_mutual if solicitud.usuario and solicitud.usuario.mutualidad else "—"

                paquete = solicitud.paquete.nombre_paquete if solicitud.paquete and solicitud.paquete.nombre_paquete else "—"
                id_solicitud = solicitud.id
                tipo_solicitud_nombre = solicitud.tipo_solicitud.tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.tipo_solicitud else "—"
                tipo_solicitud_cod = solicitud.tipo_solicitud.cod_tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.cod_tipo_solicitud else "—"

                solicitud_dict = {
                    "id": id_solicitud,
                    "nombre_solicitante": nombre_solicitante,
                    "telefono": telefono,
                    "rut": rut,
                    "responsable": responsable,
                    "empresa": empresa,
                    "mutualidad": mutualidad,
                    "paquete": paquete,
                    "fecha": fecha,
                    "tipo_solicitud": {
                        "cod_tipo_solicitud": tipo_solicitud_cod,
                        "tipo_solicitud": tipo_solicitud_nombre
                    }
                }

                datos_json.append(solicitud_dict)

            return JsonResponse({'data': datos_json})
        else:
            return JsonResponse({'error': 'No se encontraron solicitudes de consultas agendadas'})

    return JsonResponse({'error': 'Método no permitido'})

@csrf_exempt
def filtroExamen(request):
    if request.method == 'POST':
        examen = request.POST.get('busquedaExamen')

        datos_filtrados_examen = solicitudes.objects.filter(tipo_examen__descripcion__icontains=examen)

        solicitudes_agendadas = datos_filtrados_examen.filter(agendado__isnull=True)

        grupos_usuario = request.user.groups.all()

        filters = Q()
        for grupo in grupos_usuario:
            if grupo.name == 'Urgencia':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='02')
            elif grupo.name == 'Preventivo':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='01')
            elif grupo.name == 'Hospitalario':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='03')
            elif grupo.name == 'Consultas':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='04')
            elif grupo.name == 'Examenes':
                filters |= Q(tipo_solicitud__cod_tipo_solicitud='05')

        if filters:
            solicitudes_agendadas = solicitudes_agendadas.filter(filters)

        if solicitudes_agendadas.exists():
            datos_json = []
            for solicitud in solicitudes_agendadas:
                nombre_solicitante = solicitud.nombre_solicitante or "—"
                telefono = solicitud.telefono or "—"
                rut = solicitud.rut or "—"
                responsable = solicitud.usuario.nombre or "—"

                empresa = solicitud.usuario.empresa.nombre_empresa if solicitud.usuario and solicitud.usuario.empresa else "—"
                mutualidad = solicitud.usuario.mutualidad.nombre_mutual if solicitud.usuario and solicitud.usuario.mutualidad else "—"

                paquete = solicitud.paquete.nombre_paquete if solicitud.paquete and solicitud.paquete.nombre_paquete else "—"
                id_solicitud = solicitud.id
                tipo_solicitud_nombre = solicitud.tipo_solicitud.tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.tipo_solicitud else "—"
                tipo_solicitud_cod = solicitud.tipo_solicitud.cod_tipo_solicitud if solicitud.tipo_solicitud and solicitud.tipo_solicitud.cod_tipo_solicitud else "—"

                solicitud_dict = {
                    "id": id_solicitud,
                    "nombre_solicitante": nombre_solicitante,
                    "telefono": telefono,
                    "rut": rut,
                    "responsable": responsable,
                    "empresa": empresa,
                    "mutualidad": mutualidad,
                    "paquete": paquete,
                    "tipo_solicitud": {
                        "cod_tipo_solicitud": tipo_solicitud_cod,
                        "tipo_solicitud": tipo_solicitud_nombre
                    }
                }
                datos_json.append(solicitud_dict)

            solicitudes_data = json.dumps(datos_json)

            return JsonResponse({'data': datos_json})
        else:
            return JsonResponse({'data': []})

    else:
        context = {
            'title': 'solicitud',
            'year': datetime.now().year,
        }
        return render(request, 'agenda_hora/agenda_hora.html', context)

@csrf_exempt
def agendar(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        medico = request.POST.get('medico')
        comentario = request.POST.get('comentario')
        id_solicitud = request.POST.get('id_solicitud')
        envio = request.POST.get('envio')

        solicitud = get_object_or_404(solicitudes, id=id_solicitud)

        telefono = str(solicitud.telefono)
        telefono_validado = validar_telefono(telefono)


        fecha_form = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_formateada = fecha_form.strftime("%d-%m-%y")

        mensaje = f"Su cita ha sido agendada para el {fecha_formateada} a las {hora} en Clinica Alemana Temuco."

        responsable_username = request.user.username

        solicitud.fecha_atencion = fecha
        solicitud.hora_atencion = hora
        solicitud.comentario = comentario
        solicitud.responsable = responsable_username
        solicitud.nombre_medico = medico
        solicitud.agendado = True

        ultimo_codigo = solicitudes.objects.aggregate(Max('cod_solicitud'))['cod_solicitud__max']
        if ultimo_codigo is None:
            nuevo_codigo_solicitud = 1
        else:
            nuevo_codigo_solicitud = ultimo_codigo + 1

        solicitud.cod_solicitud = nuevo_codigo_solicitud


        if envio == 'on' and telefono_validado is None:

            messages.error(request, 'Número de teléfono inválido. La Hora no fue agendada')
            return HttpResponseRedirect(reverse("inicio_agendar_hora"))

        elif envio == 'on' and telefono_validado is not None:

            solicitud.save()
            if enviar_sms(mensaje, telefono_validado):

                print(f"SMS enviado a {telefono_validado} con éxito")
                messages.success(request, 'La cita ha sido agendada correctamente y la notificacion fue enviada')

            else:

                print(f"Fallo al enviar SMS a {telefono_validado}")
                messages.success(request, 'La cita ha sido agendada correctamente. Pero la notificacion no fue enviada')
        else:

            solicitud.save()
            messages.success(request, 'La cita ha sido agendada correctamente.')

        return HttpResponseRedirect(reverse("inicio_agendar_hora"))
    else:
        return HttpResponse('Error: Esta vista solo acepta peticiones POST.')


def enviar_sms(mensaje, telefono):
    username = urllib.parse.quote_plus("jruizt")
    password = urllib.parse.quote_plus("Kic1905$")
    token = urllib.parse.quote_plus("89d5b5cd-8655-473b-96bd-858a485995e1")
    mensaje_salida = urllib.parse.quote_plus(mensaje)

    url = (
        f"https://ida.itdchile.cl/publicSms/sendSms.html?"
        f"username={username}&password={password}&phone={telefono}&message={mensaje_salida}&use_short_links=1&companyCode={token}"
    )

    try:
        response = urllib.request.urlopen(url)

        if response.getcode() == 200:

            return True
        else:
            print(f"Fallo al enviar SMS. Código de respuesta: {response.getcode()}")
            return False

    except HTTPError as e:
        print(f"Error HTTP al enviar SMS: {e}")
        return False

    except URLError as e:
        print(f"Error de URL al enviar SMS: {e}")
        return False

    except Exception as e:
        print(f"Error inesperado al enviar SMS: {e}")
        return False


def validar_telefono(telefono):
    """
    Valida el número de teléfono chileno y devuelve el número formateado o None
    si no es válido. No genera error si el valor es None o incorrecto.
    """
    if telefono is None:
        return None

    telefono = telefono.replace("+", "").replace("-", "").replace(" ", "")

    try:
        int(telefono)
    except ValueError:
        return None

    if len(telefono) == 8:
        return "569" + telefono
    elif len(telefono) == 9:
        if telefono.startswith("9"):
            telefono = "569" + telefono[1:]
        elif not telefono.startswith("569"):
            return None
        return telefono
    elif len(telefono) == 10:
        if telefono.startswith("69"):
            telefono = "569" + telefono[2:]
        elif telefono.startswith("9"):
            telefono = "569" + telefono[1:]
        elif not telefono.startswith("569"):
            return None
        return telefono
    elif len(telefono) == 11:
        if telefono.startswith("569"):
            return telefono
        elif not telefono.startswith("569"):
            return None
        return telefono

    if not telefono.startswith("56"):
        return None


    return None
