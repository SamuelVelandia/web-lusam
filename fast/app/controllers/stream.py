# controlador para gestionar streams de video
from fastapi import APIRouter, Request, Cookie, HTTPException, Form
from app.repository.stream import StreamRepository

# inicializa el router para las rutas de streaming
router = APIRouter()

@router.post("/start_stream")
async def start_stream(
    request: Request,
    titulo: str = Form(...),  
    usuario: str = Cookie(None, alias="current_user"),
    matricula: str = "UVCARRITO"
):
    # verifica que el usuario esté autenticado
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario no autenticado")

    try:
        # crea un nuevo stream con los datos del usuario
        stream = await StreamRepository.crear_stream(
            usuario=usuario,
            titulo=titulo,
            matricula=matricula
        )
        # devuelve la información del stream creado
        return {
            "message": "Stream iniciado correctamente",
            "stream_id": stream["_id"],
            "titulo": stream["titulo"]
        }
    except Exception as e:
        # maneja errores inesperados
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/stop_stream/{stream_id}")
async def stop_stream(stream_id: str):
    try:
        # detiene el stream y verifica que exista
        updated = await StreamRepository.actualizar_fin_stream(stream_id)
        if not updated:
            # si no se encuentra el stream, devuelve error
            raise HTTPException(status_code=404, detail="Stream no encontrado")
        
        # confirma que el stream se detuvo
        return {"message": "Stream detenido correctamente"}
    
    except Exception as e:
        # maneja errores al detener el stream
        raise HTTPException(status_code=500, detail=f"Error al detener el stream: {str(e)}")


