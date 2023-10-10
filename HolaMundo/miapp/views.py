from django.shortcuts import render, HttpResponse, redirect
from miapp.models import Article
from django.db.models import Q
from miapp.forms import FormArticle
from django.contrib import messages

# Create your views here.

#Que es MVC? = Modelo Vista Controlador --> Acciones(Methods)
#Ques es MVT? = Modelo Vista Template --> Acciones (Methods)

layout = """
    <h1>Mi sitio WEB con Django | Anton Ibarra</h1>
    <hr />
    <ul>
    <li> <a href="/">Inicio</a> </li>
    <li> <a href="/hola-mundo">Hola Mundo</a> </li>
    <li> <a href="/pagina-pruebas">Pagina de pruebas</a> </li>
    <li> <a href="/contacto">Contacto</a> </li>
    </ul>
    <hr />
"""

def index (request):
    """html = 
        <h1>Inicio de mi Web</h1>
        <p>Creado por Antonio Ibarra!!!</p>
        <br />
        <p>Años del actual al 2100</p>
        <ul>
    ""
    year = 2023

    while year <= 2060:
        if year % 2 == 0:
            html += f"<li>{str(year)}</li>"
        year += 1

    html += "</ul>"""

    nombre = 'Anton Ibarra'
    lenguajes = ['Java','Pyhton','C++','JavaScript','Ruby']
    
    year = 2023
    hasta = range(year, 2061)

    #return HttpResponse(layout + html)
    return render(request, 'index.html', {
        'title' : 'Inicio de mi Web',
        'mi_variable': 'Soy un dato que aparecera en las vistas',
        'nombre' : nombre,
        'lenguajes' : lenguajes,
        'years' : hasta
        })

def pagina(request, redirigir=0):
    
    if redirigir == 1:
        return redirect('contacto', nombre="Anton", apellido="Ibarra")

    return render(request, 'pagina.html',{
        'texto': 'Este es un texto para probar los filtros',
        'lista' : [1,2,3,4,5]
    })

def hola_mundo (request):
    return render(request, 'hola_mundo.html')


def contacto(request, nombre="", apellido=""):
    html = ""

    if nombre and apellido:
        html += """ <p>El nombre completo es: </p>"""
        html += f"<h3>{nombre} {apellido}</h3>"

    return HttpResponse(layout + f""" <h2>Pagina de Contacto.</h2> """ + html)

def crear_articulo(request,title,content,public):
    
    articulo = Article(
        title = title,
        content = content,
        public = public
    )
    
    articulo.save()
    
    return HttpResponse(f"Articulo creado: {articulo.title} - {articulo.content}")

def articulo(request):
    
    #articulo = Article.objects.get(pk=6)
    #articulo = Article.objects.get(id=6)
    
    try:
        articulo = Article.objects.get(title="Super man", public ='False')
        response = f"<h1>Articulo: {articulo.id}. {articulo.title}</h1>"
    except:
        response = "<h1>Articulo no encontrado</h1>"
    
    return HttpResponse(response)
    
def editar_articulo(request, id):
    
    articulo = Article.objects.get(pk=id)
    
    articulo.title = 'Batman'
    articulo.content = 'Pelicula del 2017'
    articulo.public =  True
    
    articulo.save()
    
    return HttpResponse (f"<h1>Articulo {articulo.id} editado: {articulo.title} - {articulo.content}</h1>")

def articulos(request):
    
    articulos = Article.objects.all()
    #articulos = Article.objects.order_by('id') #poner - antes invierte la lista ejem: '-id'
    #articulos = Article.objects.order_by('id')[:3] #Limit a la consulta [:3] 0 [2:4] 
    
    """articulos = Article.objects.filter(
        Q(title__contains = "2") | Q(public=False)
    )
    
    articulos = Article.objects.filter(
        title = 'Articulo',
        ).exclude(public=False)           #Buscar documentacion de filtros Lookup
    
    articulos = Article.objects.raw("SELECT * FROM miapp_article ") #WHERE title='Articulo 2' AND public=1"""
    
    return render(request, 'articulos.html', {
        'articulos' : articulos 
    })
    
def borrar_articulo(request, id):
    articulo = Article.objects.get(pk=id)
    articulo.delete()
    
    return redirect('articulos')

def save_article(request):
    
    if request.method == 'POST':
        
        title = request.POST['title']
        if len(title) <= 5:
            return HttpResponse("<script>alert('El nombre del articulo es demasiado corto')</script>")
        
        content = request.POST['content']
        if len(content) <= 10:
            return HttpResponse("<script>alert('El contenido del articulo es demasiado corto')</script>")
        
        public = request.POST['public']
    
        articulo = Article(
            title = title,
            content = content,
            public = public
        )
        
        articulo.save()
    
        return HttpResponse(f'Articulo creado: {articulo.title} - {articulo.content}')
    else:
        return HttpResponse("<h1>No se ha podido crear el articulo</h1>")

def create_article(request):
    
    return render(request, 'create_article.html')

def create_full_article(request):
    
    if request.method == 'POST':
        formulario = FormArticle(request.POST)
        
        if formulario.is_valid():
            data_form = formulario.cleaned_data
            
            title = data_form['title']
            content = data_form['content']
            public =  data_form['public']
            
            articulo = Article(
            title = title,
            content = content,
            public = public
            )
        
            articulo.save()
            
            #crear mansaje falsh(sesion que solo se usa una ves)
            messages.success(request, f'Has creado correctamente el articulo {articulo.id}')
            
            
            return redirect('articulos')
            #return HttpResponse(articulo.title + ' - ' + articulo.content + ' - ' + articulo.public)
    else:
        formulario = FormArticle()
    
    return render(request, 'create_full_article.html', {
        'form' : formulario
    })