from fastapi import APIRouter, Request, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.models.imagenes import ImagenBase
from app.repository.imagen_rep import ImagenRepository
from datetime import date
import shutil
import os

# configuración del router y las plantillas
router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

# carpeta donde se guardarán las imágenes subidas
# se crea automáticamente si no existe
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/vergaleria", response_class=HTMLResponse)
async def mostrar_galeria(request: Request):
    try:
        # verifica si el usuario está autenticado
        # obtiene el usuario de las cookies de la sesión
        usuario = request.cookies.get("current_user")
        if not usuario:
            # redirige al login si no hay usuario
            return RedirectResponse(url="/login")
        
        # obtiene todas las imágenes del usuario
        # las imágenes se ordenan por fecha de subida
        imagenes = await ImagenRepository.get_images_by_user(usuario)
        
        # muestra la galería con las imágenes del usuario
        # renderiza la plantilla con los datos obtenidos
        return templates.TemplateResponse(
            "Galeria.html",
            {
                "request": request,
                "title": "Galería de Capturas",
                "usuario": usuario,
                "imagenes": imagenes
            }
        )
    except Exception as e:
        # maneja cualquier error inesperado
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-image")
async def upload_image(
    request: Request,
    etiqueta: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # verifica si el usuario está autenticado
        # obtiene el usuario de las cookies de la sesión
        usuario = request.cookies.get("current_user")
        if not usuario:
            # redirige al login si no hay usuario
            return RedirectResponse(url="/login")
        
        # guarda el archivo en el servidor
        # crea la ruta completa para el archivo
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            # copia el contenido del archivo subido
            shutil.copyfileobj(file.file, buffer)
        
        # crea el registro de la imagen en la base de datos
        # incluye metadatos como usuario, etiqueta y fecha
        imagen_data = ImagenBase(
            Usuario=usuario,
            codigo_acceso="default",
            Etiqueta=etiqueta,
            Fecha=date.today(),
            Ruta=f"/{UPLOAD_DIR}/{file.filename}"
        )
        
        # guarda la información en la base de datos
        await ImagenRepository.create_image(imagen_data)
        
        # redirige a la galería después de subir
        return RedirectResponse(url="/vergaleria", status_code=303)
    except Exception as e:
        # maneja cualquier error inesperado
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/delete-image/{image_id}")
async def delete_image(request: Request, image_id: str):
    try:
        # verifica si el usuario está autenticado
        # obtiene el usuario de las cookies de la sesión
        usuario = request.cookies.get("current_user")
        if not usuario:
            # redirige al login si no hay usuario
            return RedirectResponse(url="/login")
        
        # verifica que la imagen exista y pertenezca al usuario
        # obtiene los detalles de la imagen de la base de datos
        imagen = await ImagenRepository.get_image_by_id(image_id)
        if not imagen or imagen["Usuario"] != usuario:
            # lanza error si la imagen no existe o no pertenece al usuario
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        
        # elimina el archivo físico del servidor
        # quita el slash inicial de la ruta para el sistema de archivos
        if os.path.exists(imagen["Ruta"].lstrip('/')):
            os.remove(imagen["Ruta"].lstrip('/'))
        
        # elimina el registro de la base de datos
        await ImagenRepository.delete_image(image_id)
        
        # redirige a la galería después de eliminar
        return RedirectResponse(url="/vergaleria", status_code=303)
    except Exception as e:
        # maneja cualquier error inesperado
        raise HTTPException(status_code=500, detail=str(e))