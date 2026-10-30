from django.test import TestCase
from core.models import Libro
import json

class PruebasLibros(TestCase):

    def test_crear_libro(self):
        
        cantidad = Libro.objects.count()
        self.assertEqual(cantidad, 0)
        
        libro_creado = Libro.objects.create(
            titulo = "Tokio Blues",
            autor = "Haruki Murakami"
        )

        cantidad = Libro.objects.count()
        self.assertEqual(cantidad, 1)

        libro = Libro.objects.get(id=libro_creado.id)
       
        self.assertEqual(libro.titulo, "Tokio Blues")

    def test_listar_libros(self):
        libro1 = Libro(
            titulo = "Un mundo feliz",
            autor = "Aldous Huxley"
        )

        libro2 = Libro(
            titulo = "Los detectives salvajes",
            autor = "Roberto Bolaño"
        )

        libro1.save()
        libro2.save()

        r = self.client.get("/api/libros/")

        self.assertEqual(r.status_code, 200)

        datos = r.json()

        self.assertEqual(len(datos), 2)

        titulos = [libro["titulo"] for libro in datos]

        self.assertIn("Un mundo feliz", titulos)
        self.assertIn("Los detectives salvajes", titulos)

    def test_post_libros(self):
        self.assertEqual(Libro.objects.count(), 0)

        libro_enviar = {"titulo": "Rayuela", "autor": "Julio Cortázar"}

        respuesta = self.client.post(
            "/api/libros/",
            data=json.dumps(libro_enviar),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 201)

        self.assertEqual(Libro.objects.count(), 1)

        libro = Libro.objects.all().first()

        self.assertEqual(libro.titulo, "Rayuela")

    def test_post_titulo_vacio(self):

        libro_enviar = {"titulo": "", "autor": "Truman Capote"}

        respuesta = self.client.post(
            "/api/libros/",
            data=json.dumps(libro_enviar),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 400)

        self.assertEqual(Libro.objects.count(), 0)

        datos = respuesta.json()
        self.assertIn("error", datos)

    def test_post_datos_invalidos(self):
        casos = [
            {"titulo": "", "autor": "Albert Camus"},
            {"titulo": "La peste", "autor": ""},
            {"titulo": 123, "autor": "Albert Camus"},
            {"titulo": "La peste", "autor": 456},
            {"titulo": "A" * 201, "autor": "Albert Camus"},
            {"titulo": "La peste", "autor": "A" * 101},
        ]

        for caso in casos:
            with self.subTest(datos=caso):
                respuesta = self.client.post(
                    "/api/libros/",
                    data=json.dumps(caso),
                    content_type="application/json"
                )

                self.assertEqual(respuesta.status_code, 400)
                self.assertIn("error", respuesta.json())
                self.assertEqual(Libro.objects.count(), 0)

    def test_obtener_libro(self):
        libro_nuevo = Libro.objects.create(
            titulo="Los detectives salvajes",
            autor="Roberto Bolaño"
        )

        url = f"/api/libros/{libro_nuevo.id}/"

        respuesta = self.client.get(
            url
        )

        datos = respuesta.json()

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(datos["titulo"], "Los detectives salvajes")
        self.assertEqual(datos["autor"], "Roberto Bolaño")


    def test_obtener_libro_inexistente(self):

        respuesta = self.client.get(
            "/api/libros/999/"
        )

        self.assertEqual(respuesta.status_code, 404)
        self.assertIn("error", respuesta.json())

    def test_patch_libro(self):
        libro_nuevo = Libro.objects.create(
            titulo="El cuento de la criada",
            autor="Margaret Atwood"
        )

        url = f"/api/libros/{libro_nuevo.id}/"

        respuesta = self.client.patch(
            url,
            data=json.dumps({"titulo": "El cuento de la criada (edición revisada)"}),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.json()

        libro_nuevo.refresh_from_db()

        self.assertEqual(
            libro_nuevo.titulo,
            "El cuento de la criada (edición revisada)"
            )
        self.assertEqual(libro_nuevo.autor, "Margaret Atwood")

        self.assertEqual(
            datos["titulo"],
            "El cuento de la criada (edición revisada)"
            )

        self.assertEqual(datos["autor"], "Margaret Atwood")

    def test_put_libro(self):
        libro_nuevo = Libro.objects.create(
            titulo="Nieve de primavera",
            autor="Yukio Mishima"
        )

        url = f"/api/libros/{libro_nuevo.id}/"

        respuesta = self.client.put(
            url,
            data=json.dumps({
                "titulo":"Sputnik, mi amor",
                "autor": "Haruki Murakami"
            }),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 200)

        libro_nuevo.refresh_from_db()

        datos = respuesta.json()

        self.assertEqual(libro_nuevo.titulo, "Sputnik, mi amor")
        self.assertEqual(libro_nuevo.autor, "Haruki Murakami")
        self.assertEqual(datos["titulo"], "Sputnik, mi amor")
        self.assertEqual(datos["autor"], "Haruki Murakami")

    def test_put_incompleto(self):

        libro_nuevo = Libro.objects.create(
            titulo="Nieve de primavera",
            autor="Yukio Mishima"
        )

        url = f"/api/libros/{libro_nuevo.id}/"

        respuesta = self.client.put(
            url,
            data=json.dumps({"titulo": "Caballos desbocados"}),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 400)

        libro_nuevo.refresh_from_db()

        self.assertEqual(libro_nuevo.titulo, "Nieve de primavera")
        self.assertEqual(libro_nuevo.autor, "Yukio Mishima")

    def test_delete_libro(self):
        libro_nuevo = Libro.objects.create(
            titulo="Nieve de primavera",
            autor="Yukio Mishima"
        )

        url = f"/api/libros/{libro_nuevo.id}/"

        respuesta = self.client.delete(url)

        self.assertEqual(respuesta.status_code, 204)
        self.assertFalse(Libro.objects.filter(id=libro_nuevo.id).exists())

    def test_delete_libro_inexistente(self):

        respuesta = self.client.delete("/api/libros/999/")

        self.assertEqual(respuesta.status_code, 404)
        self.assertIn("error", respuesta.json())