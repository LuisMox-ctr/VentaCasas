"""
URL configuration for VentaCasas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from inicio import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', (admin.site.urls)),
    path('', views.principal, name='principal'),
    path('Ver_casa/<int:casa_id>/', views.vercasa, name='vercasa'),
    path('encabezado/', views.encabezado, name='encabezado'),
    path('opiniones/', views.opiniones, name='opiniones'),
    path('promociones/', views.casas_promocion, name='promociones'),
    path('casas-destacadas/', views.casas_destacadas, name='casas_destacadas'),
    
    # Rutas para CRUD de opiniones
    path('opinion/editar/<int:opinion_id>/', views.editar_opinion, name='editar_opinion'),
    path('opinion/eliminar/<int:opinion_id>/', views.eliminar_opinion, name='eliminar_opinion'),
    
    # Rutas de autenticación
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)