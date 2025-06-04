# modelo para el registro de carros
from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

class RegistroCarro(BaseModel):
    # datos básicos del carro
    Matricula: str = Field(..., min_length=8, max_length=20, description="Matricula del carro")
    Usuario: str = Field(..., min_length=4, max_length=20, description="Nombre de usuario para login")
    Estado: bool = Field(default=True, description="Estado activo/inactivo del estudiante")
    Notas: Optional[str] = Field(None, max_length=500, description="Observaciones o notas adicionales")
    Año: date = Field(..., description="Año académico (usar el primer día del año)")