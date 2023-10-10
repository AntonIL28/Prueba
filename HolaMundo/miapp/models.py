from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name = "Titulo")
    content = models.TextField(verbose_name = "Contenido")
    image = models.ImageField(default='null', verbose_name = "Miniatura")
    public = models.BooleanField(verbose_name = "Publico")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name = "Fecha de creacion")
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Articulo"
        verbose_name_plural = "Articulos"
        ordering = ['id']
    
class Category(models.Model):
    name = models.CharField(max_length=110)
    description = models.CharField(max_length=250)
    create_at = models.DateField()
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"