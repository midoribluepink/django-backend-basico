"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path
from core.views import hola, formulario, datos, calcular_edad, listar_libros, detalle_libro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hola/', hola),
    path('formulario/', formulario),
    path('datos/', datos),
    path("api/edad/", calcular_edad),
    path("api/libros/", listar_libros),
    path('api/libros/<int:id>/', detalle_libro)
]