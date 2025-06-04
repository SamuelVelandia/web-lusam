from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# creamos el router para manejar las rutas
router = APIRouter()
# configuramos las plantillas html
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/menu", response_class=HTMLResponse)
async def mostrar_pagina_verstream(request: Request):
    # renderiza la página del menú principal
    return templates.TemplateResponse(
        "Menu.html",
        {
            "request": request,
            "title": "Panel de Manejo",
            "usuario": request.cookies.get("current_user")
        }
    )