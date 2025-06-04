from datetime import datetime,date
from typing import Optional, List
from app.models.usuario import UsuarioBase
from app.config.database import db
from bson import ObjectId


class UsuarioRepository:
    # nombre de la colección en la base de datos
    COLLECTION_NAME = "usuarios"

    @staticmethod
    async def crear_usuario(usuario: UsuarioBase) -> dict:
        # convertimos el modelo a diccionario
        usuario_dict = usuario.dict()

        # ajustamos las fechas para que sean compatibles con mongodb
        for campo in ['FechaNacimiento', 'Fecha_registro']:
            valor = usuario_dict.get(campo)
            if isinstance(valor, date) and not isinstance(valor, datetime):
                usuario_dict[campo] = datetime.combine(valor, datetime.min.time())

        # guardamos el usuario y obtenemos el resultado
        result = await db[UsuarioRepository.COLLECTION_NAME].insert_one(usuario_dict)
        nuevo_usuario = await db[UsuarioRepository.COLLECTION_NAME].find_one(
            {"_id": result.inserted_id}
        )
        nuevo_usuario["_id"] = str(nuevo_usuario["_id"])
        return nuevo_usuario

    @staticmethod
    async def actualizar_usuario_por_nombre(nombre_usuario: str, datos_actualizados: dict) -> bool:
        # actualizamos los datos del usuario por su nombre
        result = await db[UsuarioRepository.COLLECTION_NAME].update_one(
            {"Usuario": nombre_usuario},
            {"$set": datos_actualizados}
        )
        return result.modified_count > 0

    @staticmethod
    async def obtener_usuario_por_usuario(nombre_usuario: str) -> Optional[dict]:
        # buscamos un usuario por su nombre
        usuario = await db[UsuarioRepository.COLLECTION_NAME].find_one(
            {"Usuario": nombre_usuario}
        )
        if usuario:
            usuario["_id"] = str(usuario["_id"])
        return usuario

    @staticmethod
    async def obtener_todos_los_usuarios() -> List[dict]:
        # obtenemos todos los usuarios de la base de datos
        usuarios = await db[UsuarioRepository.COLLECTION_NAME].find().to_list(1000)
        for usuario in usuarios:
            usuario["_id"] = str(usuario["_id"])
        return usuarios

    @staticmethod
    async def eliminar_usuario(usuario_id: str) -> bool:
        # eliminamos un usuario por su id
        result = await db[UsuarioRepository.COLLECTION_NAME].delete_one(
            {"_id": ObjectId(usuario_id)}
        )
        return result.deleted_count > 0

    @staticmethod
    async def verificar_credenciales(nombre_usuario: str, contrasena: str) -> Optional[dict]:
        # verificamos si las credenciales son correctas
        usuario = await db[UsuarioRepository.COLLECTION_NAME].find_one(
            {"Usuario": nombre_usuario, "Password": contrasena}
        )
        if usuario:
            usuario["_id"] = str(usuario["_id"])
            return usuario
        return None