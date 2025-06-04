# controlador para cerrar sesión
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

# configuración del router y plantillas
router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/salir")
async def logout_user(request: Request):
    # redirige al login y limpia la sesión
    response = RedirectResponse(url="/login", status_code=303)
    
    # elimina las cookies de sesión
    response.delete_cookie(key="current_user")
    response.delete_cookie(key="session_token")
    
    # limpia el caché del navegador
    response.headers["Cache-Control"] = "no-store"
    
    return response