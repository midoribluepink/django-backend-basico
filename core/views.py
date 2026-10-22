from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.http import JsonResponse
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
        return JsonResponse({"edad": edad_recibida})

    return HttpResponseNotAllowed(["POST"])