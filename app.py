from flask import Flask, render_template, request, redirect, url_for, flash
import redis, json, uuid, os
from dotenv import load_dotenv
from celery_app import celery, send_email_async

load_dotenv()
app = Flask(__name__)
app.secret_key = "supersecret"

# Conexión KeyDB
r = redis.Redis(
    host=os.getenv("KEYDB_HOST", "localhost"),
    port=int(os.getenv("KEYDB_PORT", 6379)),
    password=os.getenv("KEYDB_PASSWORD", None),
    decode_responses=True
)

USER_EMAIL = os.getenv("MAIL_USERNAME")  # Destino de prueba

# Función auxiliar para obtener todos los libros
def get_all_books():
    keys = r.keys("libro:*")
    books = []
    for key in keys:
        book = json.loads(r.get(key))
        books.append({"id": key.split(":")[1], **book})
    return books

# Agregar libro
@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        genre = request.form["genre"]
        status = request.form["status"]

        if not title or not author:
            flash("Título y Autor son obligatorios", "error")
            return redirect(url_for("add_book"))

        book_id = str(uuid.uuid4())
        r.set(f"libro:{book_id}", json.dumps({
            "title": title,
            "author": author,
            "genre": genre,
            "status": status
        }))

        # Enviar correo asíncrono
        body = f"Se ha agregado el libro: {title} de {author}"
        send_email_async.delay("Libro agregado 📚", USER_EMAIL, body)

        flash("Libro agregado correctamente ✅", "success")
        return redirect(url_for("index"))
    return render_template("add_book.html")

# Eliminar libro
@app.route("/delete/<id>", methods=["GET", "POST"])
def delete_book(id):
    key = f"libro:{id}"
    if not r.exists(key):
        flash("El libro no existe", "error")
        return redirect(url_for("index"))

    book = json.loads(r.get(key))
    if request.method == "POST":
        r.delete(key)

        # Enviar correo asíncrono
        body = f"Se ha eliminado el libro: {book['title']} de {book['author']}"
        send_email_async.delay("Libro eliminado 🗑️", USER_EMAIL, body)

        flash("Libro eliminado correctamente 🗑️", "success")
        return redirect(url_for("index"))

    return render_template("delete_book.html", book=book, id=id)
