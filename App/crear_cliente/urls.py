from django.urls import path
from App.crear_cliente import views

urlpatterns = [
    path('', views.crear_cliente, name="inicio_crear_cliente"),
    path('insertar_cliente/', views.insertar_cliente, name="insertar_cliente"),
    path('existe_usuario/<str:nombre_usuario>', views.existe_usuario, name="existe_usuario"),
]