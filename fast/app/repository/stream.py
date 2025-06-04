from datetime import datetime, date
from typing import Optional, List
from app.models.stream import StreamBase
from app.config.database import db
from bson import ObjectId


class StreamRepository:
    # nombre de la colección en la base de datos
    COLLECTION_NAME = "streams"

    @staticmethod
    async def crear_stream(
        usuario: str,
        titulo: str,
        matricula: str = "UVCARRITO"
    ) -> dict:
        # crea un nuevo stream con los datos proporcionados
        stream_data = {
            "Usuario": usuario,
            "Matricula": matricula,
            "titulo": titulo,
            "inicio": datetime.now(),
            "fin": None
        }

        # inserta el stream en la base de datos
        result = await db[StreamRepository.COLLECTION_NAME].insert_one(stream_data)
        # recupera el stream recién creado y convierte su id a string
        nuevo_stream = await db[StreamRepository.COLLECTION_NAME].find_one(
            {"_id": result.inserted_id}
        )
        nuevo_stream["_id"] = str(nuevo_stream["_id"])
        return nuevo_stream

    @staticmethod
    async def actualizar_fin_stream(stream_id: str) -> bool:
        # actualiza la fecha de finalización del stream
        # retorna true si se actualizó correctamente
        result = await db[StreamRepository.COLLECTION_NAME].update_one(
            {"_id": ObjectId(stream_id)},
            {"$set": {"fin": datetime.now()}}
        )
        return result.modified_count > 0

    @staticmethod
    async def obtener_stream_por_id(stream_id: str) -> Optional[dict]:
        # busca un stream específico por su id
        # retorna None si no se encuentra
        stream = await db[StreamRepository.COLLECTION_NAME].find_one(
            {"_id": ObjectId(stream_id)}
        )
        if stream:
            stream["_id"] = str(stream["_id"])
        return stream

    @staticmethod
    async def obtener_streams_por_usuario(usuario: str) -> List[dict]:
        # obtiene todos los streams de un usuario específico
        # límite de 1000 streams por consulta
        streams = await db[StreamRepository.COLLECTION_NAME].find(
            {"Usuario": usuario}
        ).to_list(1000)
        for stream in streams:
            stream["_id"] = str(stream["_id"])
        return streams

    @staticmethod
    async def obtener_streams_activos() -> List[dict]:
        # obtiene todos los streams que no han finalizado
        # streams con campo 'fin' en None
        streams = await db[StreamRepository.COLLECTION_NAME].find(
            {"fin": None}
        ).to_list(1000)
        for stream in streams:
            stream["_id"] = str(stream["_id"])
        return streams

    @staticmethod
    async def obtener_todos_los_streams() -> List[dict]:
        # obtiene todos los streams de la base de datos
        # límite de 1000 streams por consulta
        streams = await db[StreamRepository.COLLECTION_NAME].find().to_list(1000)
        for stream in streams:
            stream["_id"] = str(stream["_id"])
        return streams

    @staticmethod
    async def eliminar_stream(stream_id: str) -> bool:
        # elimina un stream específico por su id
        # retorna true si se eliminó correctamente
        result = await db[StreamRepository.COLLECTION_NAME].delete_one(
            {"_id": ObjectId(stream_id)}
        )
        return result.deleted_count > 0