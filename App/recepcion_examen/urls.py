from django.urls import path
from App.recepcion_examen import views
urlpatterns = [
    path('', views.recepcion_examen, name="inicio_recepcion_examen"),
    path('filtroCodigo/',views.filtroCodigo, name="filtroCodigo"),
    path('filtroRut/',views.filtroRut, name="filtroRut"),
    path('filtro_n_examen/',views.filtro_n_examen, name="filtro_n_examen"),
    path('filtroFecha/',views.filtroFecha, name="filtroFecha"),
    path('filtro_nombre_Utm/',views.filtro_nombre_Utm, name="filtro_nombre_Utm"),
    path('Enviar/', views.Enviar, name="Enviar"),
]