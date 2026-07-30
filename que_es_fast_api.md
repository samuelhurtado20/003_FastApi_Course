# Que es FastApi?
FastApi es un framework de Python que nos permite crear APIs de manera rápida y sencilla.

Qué es FastAPI y por qué usarlo

FastAPI es un framework moderno y rápido para desarrollar aplicaciones web y APIs en Python. Fue diseñado para proporcionar una combinación única de velocidad, seguridad, facilidad de uso y escalabilidad.

Características principales de FastAPI

Alta Velocidad:
FastAPI utiliza esquemas de tipo y validaciones asincrónicas para asegurar un rendimiento superior.
Aprovecha el motor Starlette y Pydantic, lo que permite manejar grandes volúmenes de tráfico con eficiencia.
Tipado y Validación de Datos:
Usa pydantic para definir modelos de datos, lo que asegura que los datos sean validados correctamente antes de ser procesados, garantizando la calidad de los datos.
Automatización de Documentación:
Genera documentación automática utilizando Swagger y Redoc. Esto mejora la experiencia del desarrollador y facilita la comprensión de la API por parte de los usuarios.
Soporte Asincrónico:
Permite crear APIs asíncronas para manejar múltiples solicitudes simultáneamente, mejorando la eficiencia de aplicaciones con cargas pesadas.
Seguridad:
Integra soporte para autenticación y autorización, incluyendo OAuth2, JWT y otros mecanismos de seguridad.
Es fácil de aprender y usar:
Su sintaxis es simple y concisa, lo que facilita la creación de APIs funcionales en poco tiempo.
Razones para usar FastAPI

Rendimiento:
FastAPI está diseñado para ser muy rápido gracias a su soporte nativo para métodos asíncronos y su uso eficiente de recursos.
Seguridad:
Ofrece una gestión segura de datos, validación automática, y soporte para estándares modernos de seguridad como HTTPS, autenticación y validación de token.
Facilidad de Uso:
Su sintaxis es muy intuitiva y limpia, ideal para desarrolladores que buscan escribir código claro y fácil de mantener.
Comunidad Activa y Documentación:
Gran comunidad de desarrolladores, con documentación completa, ejemplos y soporte continuo para resolver problemas o dudas.
Flexibilidad y Extensibilidad:
Soporte para integraciones avanzadas como Middlewares, dependencias y uso extensivo de bibliotecas externas.
Compatibilidad:
Es altamente compatible con bibliotecas modernas de Python como asyncio, pydantic y otras populares.
Ejemplo Básico de FastAPI

from fastapi import FastAPI

app = FastAPI()

@app.get("/") def read_root(): return {"message": "Hello, World!"}

Este pequeño ejemplo muestra cómo comenzar con una simple ruta que devuelve un mensaje básico. La capacidad de manejar rutas dinámicas, validar datos y generar documentación automática hacen de FastAPI una opción ideal para proyectos de alta demanda.










Quick setup — if you’ve done this kind of thing before
or	
https://github.com/samuelhurtado20/003-FastApi_Course.git
Get started by creating a new file or uploading an existing file. We recommend every repository include a README, LICENSE, and .gitignore.

…or create a new repository on the command line
echo "# 003-FastApi_Course" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M master
git remote add origin https://github.com/samuelhurtado20/003-FastApi_Course.git
git push -u origin master
…or push an existing repository from the command line
git remote add origin https://github.com/samuelhurtado20/003-FastApi_Course.git
git branch -M master
git push -u origin master