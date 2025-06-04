from motor.motor_asyncio import AsyncIOMotorClient
import os

# url de conexión a mongodb, por defecto local
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
# nombre de la base de datos
DB_NAME = "Lusam"

# inicializamos el cliente y la conexión a la base de datos
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]

async def verify_connection():
    # verifica que la conexión esté activa
    await client.admin.command("ping")

async def list_collections():
    # obtiene la lista de todas las colecciones en la base de datos
    collections = await db.list_collection_names()
    return collections  