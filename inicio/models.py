from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Casas(models.Model):
    nombre = models.CharField(max_length=100)
    clave = models.IntegerField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    numhabitaciones = models.IntegerField()
    direccion = models.CharField(max_length=255)
    servicios = models.TextField()
    destacada = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='imagenes/')
    
    
    en_promocion = models.BooleanField(default=False, verbose_name="En promoción")
    precio_promocional = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio promocional")
    fecha_fin_promocion = models.DateField(blank=True, null=True, verbose_name="Fecha fin promoción")
    class Meta:
        verbose_name = "Casa"
        verbose_name_plural = "Casas"
    def __str__(self):
        return self.nombre
    
class Opiniones(models.Model):
    casa = models.ForeignKey(Casas, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario", blank=True, null=True)
    comentario = models.TextField()
    imagen = models.ImageField(upload_to='opiniones/', blank=True, null=True, verbose_name="Imagen")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Opinión"
        verbose_name_plural = "Opiniones"
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} - {self.casa.nombre}"
    
class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    numero_telefono = models.CharField(max_length=15, blank=True)
    mensaje = models.TextField()

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"

    def __str__(self):
        return self.nombre