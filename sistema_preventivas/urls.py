"""
URL configuration for sistema_preventivas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from App.inicial import views
from App.inicial.views import exit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', exit, name='exit'),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('agendar/', include("App.agendar_hora.urls")),
    path('crear_paquete/', include("App.crear_paquete.urls")),
    path('crear_cliente/', include("App.crear_cliente.urls")),
    path('crear_empresa/', include("App.crear_empresa.urls")),
    path('lista_horas/', include("App.lista_hora_agendada.urls")),
    path('recepcion_examen/', include("App.recepcion_examen.urls")),
]
