from typing import Dict
from app.config.database import db


class EstadisticasRepository:
    # cuenta el total de fotos subidas por un usuario
    @staticmethod
    async def contar_fotos_por_usuario(usuario: str) -> int:
        total = await db["imagenes"].count_documents({"Usuario": usuario})
        return total

    # cuenta el total de obstáculos detectados por un usuario
    @staticmethod
    async def contar_obstaculos_por_usuario(usuario: str) -> int:
        total = await db["distancias"].count_documents({"Usuario": usuario})
        return total

    # obtiene un resumen de estadísticas del usuario
    @staticmethod
    async def obtener_estadisticas(usuario: str) -> Dict[str, int]:
        fotos = await EstadisticasRepository.contar_fotos_por_usuario(usuario)
        obstaculos = await EstadisticasRepository.contar_obstaculos_por_usuario(usuario)
        return {
            "fotos": fotos,
            "obstaculos": obstaculos
        }
