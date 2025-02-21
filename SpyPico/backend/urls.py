from django.urls import path
from backend.views import consultas, detalles_maquina, descargar_archivo
urlpatterns = [
    path('', consultas),
    path('consultas/<str:parametro>', detalles_maquina, name='consultas'),
    path('descargar_archivo/<int:archivo_id>/', descargar_archivo, name='descargar_archivo'),    

]
