# controlador para la recuperación de contraseña
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# inicializamos el router y las plantillas
router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")


@router.get("/recuperacion", response_class=HTMLResponse)
async def mostrar_recuperacion(request: Request):
    # renderiza la página de recuperación de contraseña
    return templates.TemplateResponse(
        "recuperacion.html",
        {"request": request, "title": "Recuperar Contraseña"}
    )