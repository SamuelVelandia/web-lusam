from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# creamos el router para manejar las rutas
router = APIRouter()
# configuramos las plantillas para renderizar las vistas
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/acerca", response_class=HTMLResponse)
async def mostrar_pagina_verstream(request: Request):
    # renderizamos la página de acerca con los datos del usuario
    return templates.TemplateResponse(
        "Acerca.html",
        {
            "request": request,
            "title": "Panel de Manejo",
            "usuario": request.cookies.get("current_user")
        }
    )