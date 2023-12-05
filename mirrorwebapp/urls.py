# mirrorwebapp/urls.py
from django.urls import path

from mirrorwebapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('espejo/', views.espejo, name='espejo'),
    path('procesar_formulario/', views.procesar_formulario,name='procesar_formulario'),
    path('entrar/', views.entrar, name='entrar'),
    path('añadirusuario/', views.añadirusuario, name='añadirusuario'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('habitacion/', views.habitacion, name='habitacion'),
    path('transcribir_audio/', views.transcribir_audio, name='transcribir_audio'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
