from django.urls import path
from App.agendar_hora import views
urlpatterns = [
    path('', views.agenda_hora, name="inicio_agendar_hora"),
    path('filtroRut/',views.filtroRut, name="filtroRut"),
    path('filtroPreventiva/',views.filtroPreventiva, name="filtroPreventiva"),
    path('filtroEmpresa/',views.filtroEmpresa, name="filtroEmpresa"),
    path('filtroFecha/',views.filtroFecha, name="filtroFecha"),
    path('filtroUrgencia/',views.filtroUrgencia, name="filtroUrgencia"),
    path('filtroHospitalario/',views.filtroHospitalario, name="filtroHospitalario"),
    path('agendar/',views.agendar, name="agendar"),
    path('filtroConsultas/',views.filtroConsultas, name="filtroConsultas"),
    path('filtroExamen/',views.filtroExamen, name="filtroExamen"),
]