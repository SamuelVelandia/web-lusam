from datetime import datetime
from typing import List, Optional
from app.models.imagenes import ImagenBase
from app.config.database import db
from bson import ObjectId

class ImagenRepository:
    # guardamos las imágenes en la colección 'capturas'
    COLLECTION_NAME = "capturas"

    @staticmethod
    async def get_images_by_user(usuario: str) -> List[dict]:
        # buscamos todas las imágenes que pertenecen a este usuario
        imagenes = await db[ImagenRepository.COLLECTION_NAME].find(
            {"Usuario": usuario}
        ).to_list(1000)
        # los ids de mongo son objetos especiales, los convertimos a texto normal
        for imagen in imagenes:
            imagen["_id"] = str(imagen["_id"])
        return imagenes

    @staticmethod
    async def create_image(imagen: ImagenBase) -> dict:
        # preparamos la imagen para guardarla
        imagen_dict = imagen.dict()
        
        imagen_dict["Fecha"] = datetime.combine(imagen.Fecha, datetime.min.time())
        # la guardamos en la base de datos
        result = await db[ImagenRepository.COLLECTION_NAME].insert_one(imagen_dict)
        # recuperamos la imagen que acabamos de guardar para devolverla
        new_image = await db[ImagenRepository.COLLECTION_NAME].find_one(
            {"_id": result.inserted_id}
        )
        # convertimos el id a texto normal
        new_image["_id"] = str(new_image["_id"])
        return new_image

    @staticmethod
    async def delete_image(image_id: str) -> bool:
        # intentamos borrar la imagen con este id
        result = await db[ImagenRepository.COLLECTION_NAME].delete_one(
            {"_id": ObjectId(image_id)}
        )
        # nos dice si se borró o no
        return result.deleted_count > 0

    @staticmethod
    async def get_image_by_id(image_id: str) -> Optional[dict]:
        # buscamos una imagen específica usando su id
        imagen = await db[ImagenRepository.COLLECTION_NAME].find_one(
            {"_id": ObjectId(image_id)}
        )
        # si la encontramos, convertimos su id a texto normal
        if imagen:
            imagen["_id"] = str(imagen["_id"])
        return imagen