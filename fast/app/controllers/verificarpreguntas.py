from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.repository.preguntas import PreguntasSeguridadRepository

router = APIRouter()

# estructura para validar las respuestas del usuario
class VerificarRespuestasInput(BaseModel):
    usuario: str
    respuestas: List[str]

# obtiene las preguntas de seguridad asociadas al usuario
@router.get("/preguntas/{usuario}")
async def obtener_preguntas(usuario: str):
    preguntas = await PreguntasSeguridadRepository.get_preguntas_by_user(usuario)

    if preguntas and "preguntas" in preguntas:
        return {
            "success": True,
            "preguntas": preguntas["preguntas"]
        }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# valida si las respuestas proporcionadas son correctas
@router.post("/verificar_respuestas")
async def verificar_respuestas(data: VerificarRespuestasInput):
    resultado = await PreguntasSeguridadRepository.verify_respuestas(
        usuario=data.usuario,
        respuestas=data.respuestas
    )

    if resultado["success"]:
        return resultado
    raise HTTPException(status_code=400, detail=resultado["message"])
