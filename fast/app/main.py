"""
García Velandia Samuel Obed S21002413
Bravo Ibañez Luis Fernando S21002428

Diseño de Aplicaciones Web 
Mtra: Berumen Díaz Yuliana

LUSAM: SELF DRIVING CAR
"""


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.config.database import verify_connection

from app.controllers import login, manejo, salir, registro, recuperacion, verstream, galeria, estadisticas, configuracion, menu, acerca, instrucciones, deteccion, stream,captura


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await  verify_connection()
        print("✅ Conexión a MongoDB verificada.")
    except Exception as e:
        print("❌ Error al conectar a MongoDB:", e)
    yield
    # Aquí puedes cerrar conexiones si fuera necesario en el futuro


app = FastAPI(lifespan=lifespan)

# Incluir routers
app.include_router(manejo.router)
app.include_router(salir.router)
app.include_router(registro.router)
app.include_router(recuperacion.router)
app.include_router(verstream.router)
app.include_router(galeria.router)
app.include_router(estadisticas.router)
app.include_router(configuracion.router)
app.include_router(menu.router)
app.include_router(acerca.router)
app.include_router(instrucciones.router)
app.include_router(deteccion.router)
app.include_router(stream.router)


app.include_router(login.router)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/views/static"), name="static")
