from django.urls import path
from App.crear_paquete import views

urlpatterns = [
    path('', views.index_paquete, name="index_paquete"),
    path('crear_paquete/', views.crear_paquete, name="crear_paquete"),
    path('prestaciones_nuevas/', views.prestaciones_nuevas, name = "prestaciones_nuevas"),
    path('filtro_tipo_prestacion/<str:cod_tipo_prestacion>', views.filtro_tipo_prestacion, name = "filtrar_prestacion" ),
    path('existe_paquete/<str:nombre_paquete_modal>', views.paquete_existe, name="existe_paquete"),
    path('guardar_paquete/', views.guardar_paquete, name = "guardar_paquete"),
    path('nuevaPrestacion/', views.nuevaPrestacion, name = "nuevaPrestacion"),
    path('editar/', views.editar, name = "editar"),
    path('anulado/', views.anulado, name = "anulado"),
    path('filtrocod_interno/<str:codigo_interno>', views.filtrocod_interno, name="filtrocod_interno"),
    path('filtronombPrestacion/<str:nombre_prestacion>/', views.filtronombPrestacion, name="filtronombPrestacion"),
    path('filtrocod_fonasa/<str:cod_fonasa>', views.filtrocod_fonasa, name="filtrocod_fonasa"),
]