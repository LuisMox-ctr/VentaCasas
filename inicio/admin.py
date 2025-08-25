from django.contrib import admin
from .models import Casas, Opiniones, Contacto

# Register your models here.
@admin.register(Casas)
class CasaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'clave', 'costo', 'precio_promocional', 'numhabitaciones', 'destacada', 'en_promocion', 'fecha_fin_promocion')
    search_fields = ('nombre', 'direccion')
    list_filter = ('destacada', 'en_promocion', 'numhabitaciones', 'fecha_fin_promocion')
    list_editable = ('destacada', 'en_promocion', 'precio_promocional')
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'clave', 'costo', 'numhabitaciones', 'direccion', 'servicios', 'imagen')
        }),
        ('Destacada', {
            'fields': ('destacada',)
        }),
        ('Promoción', {
            'fields': ('en_promocion', 'precio_promocional', 'fecha_fin_promocion'),
            'classes': ('collapse',) 
        }),
    )

@admin.register(Opiniones)
class OpinionesAdmin(admin.ModelAdmin):
    list_display = ('casa', 'usuario', 'fecha_creacion', 'tiene_imagen')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'casa__nombre', 'comentario')
    list_filter = ('fecha_creacion', 'casa')
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    
    fieldsets = (
        ('Información básica', {
            'fields': ('casa', 'usuario', 'comentario', 'imagen')
        }),
        ('Información del sistema', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    def tiene_imagen(self, obj):
        return bool(obj.imagen)
    tiene_imagen.boolean = True
    tiene_imagen.short_description = 'Tiene imagen'

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'numero_telefono', 'get_casa_info')
    search_fields = ('nombre', 'email', 'mensaje')
    list_filter = ('email',)
    readonly_fields = ('nombre', 'email', 'numero_telefono', 'mensaje')
    
    def get_casa_info(self, obj):
        # Extrae información de la casa del mensaje si está disponible
        if "Consulta sobre la propiedad:" in obj.mensaje:
            lineas = obj.mensaje.split('\n')
            if lineas:
                return lineas[0].replace("Consulta sobre la propiedad:", "").strip()
        return "Consulta general"
    get_casa_info.short_description = "Propiedad consultada"
    
    def has_add_permission(self, request):
        # No permitir agregar contactos desde el admin (solo desde el formulario web)
        return False
    
    def has_change_permission(self, request, obj=None):
        # Solo permitir ver, no editar
        return False