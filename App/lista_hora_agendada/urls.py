from django.urls import path
from App.lista_hora_agendada import views

urlpatterns = [
    path('', views.lista_agenda, name="inicio_lista_hora_agendada"),
    path('filtroRut/', views.filtroRut, name="filtroRut"),
    path('filtroPreventiva/', views.filtroPreventiva, name="filtroPreventiva"),
    path('filtroEmpresa/', views.filtroEmpresa, name="filtroEmpresa"),
    path('filtroFecha/', views.filtroFecha, name="filtroFecha"),
    path('filtroUrgencia/', views.filtroUrgencia, name="filtroUrgencia"),
    path('filtroHospitalario/', views.filtroHospitalario, name="filtroHospitalario"),
    path('obtener_datos/', views.obtener_datos, name="obtener_datos"),
    path('guardar_anulacion/', views.guardar_anulacion, name="guardar_anulacion"),
    path('filtroConsultas/',views.filtroConsultas, name="filtroConsultas"),
    path('filtroExamen/',views.filtroExamen, name="filtroExamen"),
]