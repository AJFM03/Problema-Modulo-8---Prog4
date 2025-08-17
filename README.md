# Problema-Modulo-8---Prog4

🎯 Objetivo
Extender la aplicación web de biblioteca personal para incluir la funcionalidad de envío de correos electrónicos gestionados de forma asíncrona utilizando Celery como gestor de tareas y KeyDB como broker de mensajes.

📝 Contexto
En esta fase del proyecto, los estudiantes integrarán capacidades de comunicación por correo electrónico en su aplicación Flask. Las acciones importantes, como agregar o eliminar libros, deben generar un correo de confirmación. Para evitar que estas operaciones ralenticen la app, se deben ejecutar como tareas asíncronas mediante Celery y KeyDB.

📌 Requisitos funcionales
Envío de correos electrónicos

Enviar un correo al usuario al agregar o eliminar un libro.

El contenido del correo debe incluir datos dinámicos (por ejemplo, título del libro).

Tareas asíncronas con Celery

El envío de correos debe gestionarse fuera del hilo principal de Flask mediante Celery.

Utilizar KeyDB como broker de mensajes (usando la interfaz Redis compatible).

🔄 Cambios y objetivos clave
Integrar Celery con Flask para ejecutar tareas asíncronas.

Configurar KeyDB como broker en .env.

Usar una biblioteca como Flask-Mail o similar para el envío de correos.

Verificar que la funcionalidad sea compatible con Gunicorn y Nginx (para entorno de producción).

💡 Consideraciones técnicas
Crear una instancia de Celery dentro del proyecto Flask (celery_app.py o similar).

Configurar las variables de entorno para SMTP y KeyDB en .env:

MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=usuario
MAIL_PASSWORD=contraseña
MAIL_USE_TLS=True
CELERY_BROKER_URL=redis://localhost:6379/0
Agregar dependencias al archivo requirements.txt: Flask-Mail, Celery, redis, python-dotenv.

Separar claramente la lógica de Flask y las tareas de Celery.

Asegurar buen manejo de errores y validaciones (por ejemplo, fallos de conexión SMTP).

🚀 Entrega
El proyecto debe subirse a un repositorio público o privado en GitHub o GitLab.

El enlace del repositorio debe compartirse en el espacio de entrega habilitado.
