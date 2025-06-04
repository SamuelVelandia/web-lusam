from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.repository.estadisticas_rep import EstadisticasRepository  

# configuración del router y las plantillas
router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/estadisticas", response_class=HTMLResponse)
async def mostrar_pagina_verstream(request: Request):
    # verifica si el usuario está autenticado
    # obtiene el usuario de las cookies de la sesión
    usuario = request.cookies.get("current_user")
    if not usuario:
        # si no hay usuario, muestra la página con valores por defecto
        # esto evita errores y muestra un mensaje apropiado
        return templates.TemplateResponse(
            "Estadisticas.html",
            {
                "request": request,
                "title": "Panel de Manejo",
                "error": "Usuario no autenticado",
                "usuario": None,
                "fotos": 0,
                "obstaculos": 0
            }
        )

    # obtiene las estadísticas del usuario desde la base de datos
    # incluye conteo de fotos y obstáculos detectados
    estadisticas = await EstadisticasRepository.obtener_estadisticas(usuario)

    # muestra la página con las estadísticas del usuario
    # renderiza la plantilla con los datos obtenidos
    return templates.TemplateResponse(
        "Estadisticas.html",
        {
            "request": request,
            "title": "Panel de Manejo",
            "usuario": usuario,
            "fotos": estadisticas["fotos"],
            "obstaculos": estadisticas["obstaculos"]
        }
    )
