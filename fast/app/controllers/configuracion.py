from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.repository.usuario_rep import UsuarioRepository


router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/configuracion", response_class=HTMLResponse)
async def mostrar_pagina_verstream(request: Request):
    # muestra la página de configuración del usuario
    return templates.TemplateResponse(
        "Configuracion.html",
        {
            "request": request,
            "title": "Panel de Manejo",
            "usuario": request.cookies.get("current_user")
        }
    )

@router.post("/actualizar_perfil")
async def actualizar_perfil(
    request: Request,
    Nombre: str = Form(...),
    ApellidoPaterno: str = Form(...),
    ApellidoMaterno: str = Form(None),
    Correo: str = Form(...),
    FechaNacimiento: str = Form(...),
    Usuario: str = Form(...),
    password: str = Form("")
):
    # verifica si el usuario está logueado
    current_user = request.cookies.get("current_user")
    if not current_user:
        return RedirectResponse(url="/login")
    
    # prepara los datos del perfil para actualizar
    datos_actualizados = {
        "Nombre": Nombre,
        "ApellidoPaterno": ApellidoPaterno,
        "ApellidoMaterno": ApellidoMaterno,
        "Correo": Correo,
        "FechaNacimiento": FechaNacimiento,
        "Usuario": Usuario
    }
    
    # actualiza la contraseña solo si se proporcionó una nueva
    if password:
        datos_actualizados["Password"] = password
    
    # actualiza los datos del usuario en la base de datos
    actualizado = await UsuarioRepository.actualizar_usuario_por_nombre(
        nombre_usuario=current_user,
        datos_actualizados=datos_actualizados
    )
    
    # si el usuario cambió su nombre, actualiza la cookie
    if actualizado and Usuario != current_user:
        response = RedirectResponse(url="/perfil", status_code=303)
        response.set_cookie(key="current_user", value=Usuario)
        return response
    
    return RedirectResponse(url="/login", status_code=303)