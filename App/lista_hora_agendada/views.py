from django.http import JsonResponse, HttpResponseRedirect
from datetime import datetime
from django.http import HttpRequest
from django.shortcuts import render, reverse
from App.agendar_hora.models import solicitudes, RegistroAnulado
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

def lista_agenda(request):
    assert isinstance(request,HttpRequest)
    return render(
        request,
        'lista_hora_agendada/lista_hora_agendada.html',
        {
            'title':'Lista de horas',
            'year':datetime.now().year,
        }
    )

@csrf_exempt
def filtroRut(request):
    if request.method == 'POST':
        rut_busqueda = request.POST.get('busquedaRut')

        datos_filtrados_rut = solicitudes.objects.filter(rut=rut_busqueda)

        solicitudes_agendadas = solicitudes.objects.filter(agendado=True)

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

        solicitudes_agendadas = solicitudes.objects.filter(agendado=True)

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

        solicitudes_agendadas = datos_filtrados_empresa.filter(agendado=True)

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

        datos_filtrados_por_fecha = solicitudes.objects.filter(fecha_atencion__range=[fecha_inicio, fecha_fin])

        solicitudes_agendadas = datos_filtrados_por_fecha.filter(agendado=True)

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

        solicitudes_agendadas = datos_filtrados_urgencias.filter(agendado=True)

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

        solicitudes_agendadas = datos_filtrados_hospitalario.filter(agendado=True)

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

        solicitudes_agendadas = datos_filtrados_consultas.filter(agendado=True)

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

        solicitudes_agendadas = datos_filtrados_examen.filter(agendado=True)

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
def obtener_datos(request):
    if request.method == 'POST':
        persona_id = request.POST.get('personaId')
        try:
            solicitud = solicitudes.objects.select_related('usuario__empresa', 'usuario__mutualidad').get(id=persona_id)
            datos_vinculados = {
                'id': solicitud.id,
                'rut': solicitud.rut,
                'fecha_agendada': solicitud.fecha_atencion.strftime("%Y-%m-%d"),
                'hora_agendada': solicitud.hora_atencion,
                'nombre_solicitante': solicitud.nombre_solicitante,
                'telefono': solicitud.telefono,
                'empresa': solicitud.usuario.empresa.nombre_empresa if solicitud.usuario and solicitud.usuario.empresa else solicitud.usuario.mutualidad.nombre_mutual if solicitud.usuario and solicitud.usuario.mutualidad else None,
                'ejecutivo': solicitud.responsable,
                'comentario': solicitud.comentario,
                'paquete': solicitud.paquete.nombre_paquete if solicitud.paquete else None,
                'nombre_medico': solicitud.nombre_medico
            }
            return JsonResponse({'success': True, 'data': datos_vinculados})
        except solicitudes.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'La solicitud no existe'})
    return JsonResponse({'success': False, 'error': 'Método de solicitud no válido'})

@csrf_exempt
def guardar_anulacion(request):
    if request.method == 'POST':
        try:
            motivo = request.POST.get('motivo_anulacion', '')
            id_persona = request.POST.get('id_persona')

            id_solicitudes = [int(id_str.strip('"')) for id_str in id_persona.split(',')]

            solicitudes_anuladas = solicitudes.objects.filter(id__in=id_solicitudes)

            if solicitudes_anuladas.exists():
                id_procesado = solicitudes_anuladas.first()

            registro_anulado = RegistroAnulado.objects.create(
                motivo_anulacion=motivo,
                fecha_anulacion=timezone.now(),
                responsable=request.user.username if request.user.is_authenticated else None,
                cod_id=id_procesado
            )

            registro_anulado.save()

            solicitudes_anuladas.update(agendado=False)

            messages.success(request, 'El registro se ha anulado correctamente.')
            return HttpResponseRedirect(reverse("inicio_lista_hora_agendada"))

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'lista_hora_agendada/lista_hora_agendada.html')