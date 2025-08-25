from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, Http404
from .models import Casas, Opiniones
from .forms import OpinionesForm, ContactoForm, EditarOpinionForm
from django.utils import timezone
import json

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada exitosamente para {username}. Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Create your views here.
def principal(request):
    casas = Casas.objects.all()
    # Obtener casas destacadas para el carousel
    casas_destacadas = Casas.objects.filter(destacada=True)[:3]
    # Obtener casas en promoción (promociones vigentes)
    casas_promocion = Casas.objects.filter(
        en_promocion=True,
        fecha_fin_promocion__gte=timezone.now().date()
    )[:4]  # Mostrar máximo 4 promociones
    
    context = {
        'casas': casas,
        'casas_destacadas': casas_destacadas,
        'casas_promocion': casas_promocion
    }
    return render(request, 'inicio/principal.html', context)

def encabezado(request):
    return render(request, 'inicio/encabezado.html')

def opiniones(request):
    return render(request, 'inicio/opiniones.html')

def vercasa(request, casa_id):
    casa = get_object_or_404(Casas, id=casa_id)
    opiniones = Opiniones.objects.filter(casa=casa).order_by('-fecha_creacion')
    
    # Inicializar formularios
    opinion_form = OpinionesForm()
    contacto_form = ContactoForm()
    
    # Manejar formularios POST
    if request.method == 'POST':
        # Verificar qué formulario se envió
        if 'opinion_form' in request.POST:
            # Verificar si el usuario está autenticado para agregar opiniones
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para agregar una opinión.')
                return redirect('login')
            
            # Procesar formulario de opiniones
            opinion_form = OpinionesForm(request.POST, request.FILES)
            if opinion_form.is_valid():
                opinion = opinion_form.save(commit=False)
                opinion.casa = casa  
                opinion.usuario = request.user  # Asignar el usuario autenticado
                opinion.save()
                
                messages.success(request, 'Tu opinión ha sido enviada correctamente.')
                return redirect('vercasa', casa_id=casa.id)
        
        elif 'contacto_form' in request.POST:
            # Procesar formulario de contacto
            contacto_form = ContactoForm(request.POST)
            if contacto_form.is_valid():
                # Agregar información de la casa al mensaje
                contacto = contacto_form.save(commit=False)
                mensaje_original = contacto.mensaje
                contacto.mensaje = f"Consulta sobre la propiedad: {casa.nombre} (Clave: {casa.clave})\n\n{mensaje_original}"
                contacto.save()
                messages.success(request, 'Tu mensaje de contacto ha sido enviado correctamente. Nos pondremos en contacto contigo pronto.')
                return redirect('vercasa', casa_id=casa.id)
    
    context = {
        'casa': casa,
        'opiniones': opiniones,
        'opinion_form': opinion_form,
        'contacto_form': contacto_form
    }
    
    return render(request, 'inicio/VistaCasa.html', context)

@login_required
def editar_opinion(request, opinion_id):
    opinion = get_object_or_404(Opiniones, id=opinion_id)
    
    # Verificar que el usuario sea el propietario de la opinión
    if opinion.usuario != request.user:
        messages.error(request, 'No tienes permisos para editar esta opinión.')
        return redirect('vercasa', casa_id=opinion.casa.id)
    
    if request.method == 'POST':
        form = EditarOpinionForm(request.POST, request.FILES, instance=opinion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu opinión ha sido actualizada correctamente.')
            return redirect('vercasa', casa_id=opinion.casa.id)
    else:
        form = EditarOpinionForm(instance=opinion)
    
    context = {
        'form': form,
        'opinion': opinion,
        'casa': opinion.casa
    }
    
    return render(request, 'inicio/editar_opinion.html', context)

@login_required
def eliminar_opinion(request, opinion_id):
    opinion = get_object_or_404(Opiniones, id=opinion_id)
    
    # Verificar que el usuario sea el propietario de la opinión
    if opinion.usuario != request.user:
        messages.error(request, 'No tienes permisos para eliminar esta opinión.')
        return redirect('vercasa', casa_id=opinion.casa.id)
    
    casa_id = opinion.casa.id
    
    if request.method == 'POST':
        opinion.delete()
        messages.success(request, 'Tu opinión ha sido eliminada correctamente.')
        return redirect('vercasa', casa_id=casa_id)
    
    context = {
        'opinion': opinion,
        'casa': opinion.casa
    }
    
    return render(request, 'inicio/confirmar_eliminar_opinion.html', context)

def casas_destacadas(request):
    casas_destacadas = Casas.objects.filter(destacada=True)[:6]
    return render(request, 'inicio/casas_destacadas.html', {'casas': casas_destacadas})

def casas_promocion(request):
    # Obtener casas en promoción vigentes
    casas_promocion = Casas.objects.filter(
        en_promocion=True,
        fecha_fin_promocion__gte=timezone.now().date()
    ).order_by('fecha_fin_promocion')  # Ordenar por fecha de vencimiento
    
    return render(request, 'inicio/casas_promocion.html', {'casas': casas_promocion})