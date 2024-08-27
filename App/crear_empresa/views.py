from datetime import datetime

from django.contrib import messages
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect

from App.crear_empresa.models import empresa, tipo_organizacion, mutualidades, utms


# Create your views here.

def crear_empresa(request):
    assert isinstance(request,HttpRequest)
    tipo = tipo_organizacion.objects.all()
    mutual = mutualidades.objects.all()
    return render(
        request,
        'crear_empresa/crear_empresa.html',
        {
            'title':'Crear Empresa',
            'year':datetime.now().year,
            'tipos': tipo,
            'mutualidades': mutual
        }
    )

def insertar_empresa(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        rut = request.POST.get('rut')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')

        try:
            if tipo == '01':
                existe_emp = empresa.objects.filter(cod_empresa=codigo).exists()

                if existe_emp:
                    messages.error(request, f'El codigo de empresa ya existe')
                    return redirect('inicio_crear_empresa')

                mutual = request.POST.get('mutual_cliente')
                existe_mutual = mutualidades.objects.get(cod_mutual=mutual)

                datos = empresa(
                    cod_empresa = codigo,
                    nombre_empresa = nombre,
                    mutualidad = existe_mutual,
                    rut = rut,
                    direccion = direccion,
                    telefono = telefono,
                )
                datos.save()
                messages.success(request, 'La empresa se ha creado correctamente.')
                return redirect('inicio_crear_empresa')
            elif tipo == '02':

                existe_mutual = mutualidades.objects.filter(cod_mutual=codigo).exists()

                if existe_mutual:
                    messages.error(request, f'El codigo de mutual ya existe')
                    return redirect('inicio_crear_empresa')

                datos = mutualidades(
                    cod_mutual=codigo,
                    nombre_mutual=nombre,
                    rut=rut,
                    direccion=direccion,
                    telefono=telefono,
                )
                datos.save()
                messages.success(request, 'La mutualidad se ha creado correctamente.')
                return redirect('inicio_crear_empresa')
            elif tipo == '03':

                existe_utms = utms.objects.filter(cod_utms=codigo).exists()

                if existe_utms:
                    messages.error(request, f'El codigo de UTMS ya existe')
                    return redirect('inicio_crear_empresa')

                datos = utms(
                    cod_utms=codigo,
                    nombre_utms=nombre,
                    rut=rut,
                    direccion=direccion,
                    telefono=telefono,
                )
                datos.save()
                messages.success(request, 'La UTMS se ha creado correctamente.')
                return redirect('inicio_crear_empresa')
            else:
                messages.error(request, 'No se han insertado datos.')
                return redirect('inicio_crear_empresa')

        except Exception as e:
            messages.error(request, f'Ocurrió un error (no se insertaron datos): {str(e)}')
            return redirect('inicio_crear_empresa')

    return redirect('inicio_crear_empresa')

def existe_empresa(request, cod_empresa):
    empresa_existente = empresa.objects.filter(cod_empresa=cod_empresa)
    data = list(empresa_existente.values())
    return JsonResponse(data, safe=False)

def existe_mutualidad(request, cod_mutual):
    mutual_existente = mutualidades.objects.filter(cod_mutual=cod_mutual)
    data = list(mutual_existente.values())
    return JsonResponse(data, safe=False)

def existe_utms(request, cod_utms):
    utms_existente = utms.objects.filter(cod_utms=cod_utms)
    data = list(utms_existente.values())
    return JsonResponse(data, safe=False)