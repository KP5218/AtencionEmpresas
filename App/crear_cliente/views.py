from datetime import datetime

import bcrypt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect

from App.crear_empresa.models import empresa, tipo_organizacion, mutualidades, utms
from App.crear_cliente.models import usuario

@login_required
def crear_cliente(request):
    assert isinstance(request,HttpRequest)
    empresas = empresa.objects.all()
    tipo = tipo_organizacion.objects.all()
    mutual = mutualidades.objects.all()
    utm = utms.objects.all()
    return render(
        request,
        'crear_cliente/crear_cliente.html',
        {
            'title':'Crear Cliente',
            'year':datetime.now().year,
            'empresas':empresas,
            'tipos':tipo,
            'mutualidades':mutual,
            'utms':utm,
        }
    )


def insertar_cliente(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        nombre_cliente = request.POST.get('nombre_cliente')
        usuario_cliente = request.POST.get('usuario_cliente')
        contraseña_cliente = request.POST.get('contraseña_cliente')
        rut_cliente = request.POST.get('rut')


        try:
            if tipo == '01':
                empresa_cliente = request.POST.get('empresa_cliente')
                datos_empresa = empresa.objects.get(cod_empresa=empresa_cliente)

                existe_usuario = usuario.objects.filter(usuario=usuario_cliente).exists()

                if existe_usuario:
                    messages.error(request, f'El nombre de usuario ya existe')
                    return redirect('inicio_crear_cliente')

                hashed_password = bcrypt.hashpw(contraseña_cliente.encode('utf-8'), bcrypt.gensalt())

                datos_cliente = usuario(
                    usuario=usuario_cliente,
                    clave=hashed_password.decode('utf-8'),
                    empresa=datos_empresa,
                    nombre=nombre_cliente,
                    rut = rut_cliente,

                )
                datos_cliente.save()
                messages.success(request, 'El usuario se ha creado correctamente.')
                return redirect('inicio_crear_cliente')

            elif tipo == '02':
                mutual_cliente = request.POST.get('mutual_cliente')
                datos_mutual = mutualidades.objects.get(cod_mutual=mutual_cliente)

                existe_usuario = usuario.objects.filter(usuario=usuario_cliente).exists()

                if existe_usuario:
                    messages.error(request, f'El nombre de usuario ya existe')
                    return redirect('inicio_crear_cliente')

                hashed_password = bcrypt.hashpw(contraseña_cliente.encode('utf-8'), bcrypt.gensalt())

                datos_cliente = usuario(
                    usuario=usuario_cliente,
                    clave=hashed_password.decode('utf-8'),
                    mutualidad=datos_mutual,
                    nombre=nombre_cliente,
                    rut=rut_cliente,

                )
                datos_cliente.save()
                messages.success(request, 'El usuario se ha creado correctamente.')
                return redirect('inicio_crear_cliente')
            elif tipo == '03':
                utms_cliente = request.POST.get('utms_cliente')
                datos_utms = utms.objects.get(cod_utms=utms_cliente)

                existe_usuario = usuario.objects.filter(usuario=usuario_cliente).exists()

                if existe_usuario:
                    messages.error(request, f'El nombre de usuario ya existe')
                    return redirect('inicio_crear_cliente')

                hashed_password = bcrypt.hashpw(contraseña_cliente.encode('utf-8'), bcrypt.gensalt())

                datos_cliente = usuario(
                    usuario=usuario_cliente,
                    clave=hashed_password.decode('utf-8'),
                    utm=datos_utms,
                    nombre=nombre_cliente,
                    rut=rut_cliente,
                )
                datos_cliente.save()
                messages.success(request, 'El usuario se ha creado correctamente.')
                return redirect('inicio_crear_cliente')
            else:
                messages.error(request, f'El usuario no se insertó')
                return redirect('inicio_crear_cliente')

        except Exception as e:
            messages.error(request, f'Ocurrió un error (no se insertaron datos): {str(e)}')
            return redirect('inicio_crear_cliente')

    return redirect('inicio_crear_cliente')

def existe_usuario(request, nombre_usuario):
    usuario_existente = usuario.objects.filter(usuario=nombre_usuario)
    data = list(usuario_existente.values())
    return JsonResponse(data, safe=False)