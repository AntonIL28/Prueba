from django import forms
from django.core import validators

#Se pueden personalizar los formularios con clases, revisar docuemntacion

class FormArticle(forms.Form):
    
    title = forms.CharField(
        label= "Titulo",
        max_length = 20,
        widget = forms.TextInput(
            attrs={
                'placeholder':'Escribe el titulo',
                'class' : 'titulo_form_article'
            }
        ),
        validators=[
            validators.MinLengthValidator(10, 'El titulo es demasiado corto'),
            validators.RegexValidator('^[A-Za-z0-9ñ ]*$', 'El titulo esta mal formado', 'invalid_title')
        ]
    )
    
    content = forms.CharField(
        label= "Contenido",
        widget= forms.Textarea,
        validators=[
            validators.MaxLengthValidator(40, 'Te has pasado, has puesto mucho texto')
        ]
    )
    
    content.widget.attrs.update({
        'placeholder':'Escribe el contenido del articulo YAA',
        'class' : 'contenido_form_article'
    })
    
    public_options = [
        (1, "Publico"),
        (0, "Privado")
    ]
    public = forms.TypedChoiceField(
        label = "Estado",
        choices = public_options
    )