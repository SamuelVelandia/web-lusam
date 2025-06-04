# controlador para ver streams en vivo
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# configuración del router y plantillas
router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/verstream", response_class=HTMLResponse)
async def mostrar_pagina_verstream(request: Request):
    # muestra la página de visualización del stream
    return templates.TemplateResponse(
        "VerStream.html",
        {
            "request": request,
            "title": "Panel de Manejo",
            "usuario": request.cookies.get("current_user")
        }
    )