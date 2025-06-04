from datetime import date
from pydantic import BaseModel, Field

# modelo base para registrar distancias
class RegistroDistanciaBase(BaseModel):
    # código único para acceder al stream de datos
    codigo_acceso: str = Field(..., min_length=6, max_length=12, description="Código de acceso al stream")
    # distancia medida en kilómetros
    Distancia: float = Field(..., gt=0, le=1000, description="Distancia en kilómetros (0-1000 km)")
    # fecha en que se realizó el registro
    Fecha: date = Field(..., description="Fecha del registro (YYYY-MM-DD)")