from django import forms
from .models import Opiniones
from .models import Contacto

class OpinionesForm(forms.ModelForm):
    class Meta:
        model = Opiniones
        fields = ['comentario', 'imagen']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tu opinión',
                'rows': 4
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'comentario': 'Tu opinión',
            'imagen': 'Imagen (opcional)'
        }

class EditarOpinionForm(forms.ModelForm):
    class Meta:
        model = Opiniones
        fields = ['comentario', 'imagen']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tu opinión',
                'rows': 4
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'comentario': 'Tu opinión',
            'imagen': 'Imagen (opcional)'
        }
        
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields =['nombre', 'email', 'numero_telefono', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
            }),
            'numero_telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de teléfono'
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'mensaje',
                'rows': 4
            })
        }
        labels = {
            'nombre': 'Nombre',
            'email': 'Correo electrónico',
            'numero_telefono': 'Número de teléfono',
            'mensaje': 'Mensaje'
        }