from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.http import JsonResponse
from core.models import Libro
import json

def hola(request):
    edad = request.GET.get("edad")
    anios = request.GET.get("anios")

    if edad is None:
        return HttpResponse("No proporcionaste tu edad.")

    if anios is None:
        return HttpResponse("No indicaste cuántos años quieres avanzar.")

    try:
        anios = int(anios)
        edad = int(edad)
    except ValueError:
        return HttpResponse("Los datos tienen que ser números enteros.")

    if not (1 <= edad <= 120):
        return HttpResponse("La edad debe estar entre 1 y 120")

    if anios < 0:
        return HttpResponse("Los años no pueden ser menor que 0")

    return HttpResponse(f"Dentro de {anios} tendrás {edad + anios} años.")

def formulario(request):
    if request.method == "GET":
        return render(request, "core/formulario.html", {"mensaje" : "Hola desde Python"})

    if request.method == "POST":
        edad = request.POST.get("edad")
        if not edad:
            return HttpResponse("No proporcionaste tu edad.")

        try:
            edad = int(edad)
        except ValueError:
            return HttpResponse("La edad debe ser un número entero.")

        if not 1 <= edad <= 120:
            return HttpResponse("Edad fuera del rango permitido")

        resultado = edad + 1
        return render(request, "core/formulario.html", {"resultado" : resultado, "mensaje" : "Hola desde Python", "edad" : edad})

    return HttpResponseNotAllowed(["GET", "POST"])


def datos(request):
    nombre = request.GET.get("nombre", "Anónimo")
    edad = request.GET.get("edad", 0)

    try:
        edad = int(edad)
    except ValueError:
        return JsonResponse({"error": "La edad debe ser un entero."}, status = 400)

    return JsonResponse({
        "nombre": nombre,
        "edad": edad
    })

def calcular_edad(request):
    if request.method == "POST":

        try:
            datos = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        if not isinstance(datos, dict):
            return JsonResponse({"error": "Se esperaba un objeto JSON"}, status=400)
        
        edad_recibida = datos.get("edad")

        if type(edad_recibida) is not int:
            return JsonResponse({"error": "La edad debe ser un número entero"}, status=400)

        if not 1 <= edad_recibida <= 120:
            return JsonResponse({"error": "La edad debe ser un entero entre 1 y 120"}, status=400)

        return JsonResponse({"edad": edad_recibida})

    return HttpResponseNotAllowed(["POST"])


def listar_libros(request):
    if request.method == "GET":
        libros_db = Libro.objects.all()
        libros_db_list = []

        for i in libros_db:
            libros_db_list.append(
                {
                    "id": i.id,
                    "titulo": i.titulo,
                    "autor": i.autor
                }
            )

        return JsonResponse(libros_db_list, safe = False)

    if request.method == "POST":

        try:
            libro = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        if not isinstance(libro, dict):
            return JsonResponse({"error": "Tipo de dato equivocado, se espera un diccionario"}, status=400)

        if "titulo" not in libro:
            return JsonResponse({"error": "Clave título inexistente"}, status=400)

        if "autor" not in libro:
            return JsonResponse({"error": "Clave autor inexistente"}, status=400)

        titulo = libro["titulo"]
        autor = libro["autor"]

        if not isinstance(titulo, str):
            return JsonResponse({"error": "El título tiene que ser un str"}, status=400)

        if not isinstance(autor, str):
            return JsonResponse({"error": "El autor tiene que ser un str"}, status=400)

        titulo = titulo.strip()
        autor = autor.strip()

        if not titulo:
            return JsonResponse({"error": "El campo de título está vacío."}, status=400)

        if not autor:
            return JsonResponse({"error": "El campo de autor está vacío."}, status=400)

        if len(titulo) > 200:
            return JsonResponse({"error": "El título no puede tener más de 200 caracteres"}, status=400)

        if len(autor) > 100:
            return JsonResponse({"error": "El autor no puede tener más de 100 caracteres"}, status=400)

        nuevo_libro = Libro.objects.create(
            titulo=titulo,
            autor=autor
        )

        nuevo_libro_dict = {"id": nuevo_libro.id, "titulo": titulo, "autor": autor}

        return JsonResponse(nuevo_libro_dict, status=201)

    return HttpResponseNotAllowed(["GET", "POST"])

def detalle_libro(request, id):

    if request.method not in ["GET", "PATCH", "PUT", "DELETE"]:
        return HttpResponseNotAllowed(["GET", "PATCH", "PUT", "DELETE"])

    libro = Libro.objects.filter(id=id).first()

    if libro is None:
        return JsonResponse({"error": "Libro no encontrado"}, status=404)

    libro_dict = {"id": libro.id, "titulo": libro.titulo, "autor": libro.autor}

    if request.method == "DELETE":
        libro.delete()
        return HttpResponse(status=204)

    if request.method == "GET":
        return JsonResponse(libro_dict)

    if request.method in ["PATCH", "PUT"]:

        try:
            libro_nuevo = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        if not isinstance(libro_nuevo, dict):
            return JsonResponse({"error": "Tipo de dato equivocado, se espera un diccionario"}, status=400)

        if not libro_nuevo:
            return JsonResponse({"error": "El diccionario está vacío"}, status=400)

        campos_permitidos = {"titulo", "autor"}
        campos_recibidos = set(libro_nuevo.keys())

        campos_no_permitidos = campos_recibidos - campos_permitidos

        if campos_no_permitidos:
            return JsonResponse({"error": "Campos no permitidos"}, status=400)

        if request.method == "PUT" and campos_recibidos != campos_permitidos:
            return JsonResponse({"error": "Campos incompletos"}, status=400)

        if "titulo" in libro_nuevo:
            titulo_nuevo = libro_nuevo["titulo"]

            if not isinstance(titulo_nuevo, str):
                return JsonResponse({"error": "El título tiene que ser un str"}, status=400)

            titulo_nuevo = titulo_nuevo.strip()

            if not titulo_nuevo:
                return JsonResponse({"error": "El campo de título está vacío"}, status=400)

            if len(titulo_nuevo) > 200:
                return JsonResponse({"error": "El título no puede tener más de 200 caracteres"}, status=400)

        if "autor" in libro_nuevo:
            autor_nuevo = libro_nuevo["autor"]

            if not isinstance(autor_nuevo, str):
                return JsonResponse({"error": "El autor tiene que ser un str"}, status=400)

            autor_nuevo = autor_nuevo.strip()

            if not autor_nuevo:
                return JsonResponse({"error": "El campo de autor está vacío"}, status=400)

            if len(autor_nuevo) > 100:
                return JsonResponse({"error": "El autor no puede tener más de 100 caracteres"}, status=400)

        if "titulo" in libro_nuevo:
            libro.titulo = titulo_nuevo

        if "autor" in libro_nuevo:
            libro.autor = autor_nuevo

        libro.save()

        libro_dict = {"id": libro.id, "titulo": libro.titulo, "autor": libro.autor}

        return JsonResponse(libro_dict)                    

