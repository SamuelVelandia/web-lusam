from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.repository.usuario_rep import UsuarioRepository
from datetime import datetime, timedelta

# configuración del router y las plantillas
router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

# muestra la página de inicio de sesión
@router.get("/login", response_class=HTMLResponse)
async def show_login(request: Request):
    # renderiza la plantilla de login con el título
    return templates.TemplateResponse(
        "Login.html",
        {"request": request, "title": "Inicio de Sesión"}
    )

# procesa el formulario de inicio de sesión
@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    nombre_usuario: str = Form(...),  
    contrasena: str = Form(...)       
):
    # verifica las credenciales del usuario en la base de datos
    usuario = await UsuarioRepository.verificar_credenciales(nombre_usuario, contrasena)

    if usuario:
        # si las credenciales son correctas, redirige al menú
        response = RedirectResponse(url="/menu", status_code=302)
        
        # guarda la información del usuario en cookies
        # cookie principal con el identificador del usuario
        response.set_cookie(
            key="current_user",
            value=usuario["Usuario"],
            max_age=3600,        # expira en una hora
            httponly=True,       # solo accesible por http
            secure=True,         # solo por https
            samesite="lax"       # protección contra ataques
        )
        
        # guarda el nombre del usuario para mostrar en la interfaz
        # cookie secundaria para mostrar el nombre en la ui
        response.set_cookie(
            key="user_display_name",
            value=usuario.get("Nombre", ""),
            max_age=3600         # misma duración que la cookie principal
        )
        
        return response
    else:
        # si las credenciales son incorrectas, muestra error
        # devuelve al formulario con mensaje de error
        return templates.TemplateResponse(
            "Login.html",
            {
                "request": request,
                "title": "Inicio de Sesión",
                "error": "Usuario o contraseña incorrectos",
                "nombre_usuario": nombre_usuario  # mantiene el usuario ingresado
            }
        )