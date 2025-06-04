from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class StreamBase(BaseModel):
    # datos básicos del stream
    Usuario: str = Field(..., min_length=4, max_length=20, description="Persona que lo maneja")
    Matricula: str = Field(..., min_length=8, max_length=20, description="Carro del stream")
    titulo: str = Field(..., min_length=5, max_length=100, description="Título del stream")
    
    # control de tiempo del stream
    inicio: datetime = Field(..., description="Fecha y hora de inicio del stream")
    fin: Optional[datetime] = Field(None, description="Fecha y hora de finalización del stream")