from datetime import date
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# modelo base para usuarios del sistema
class UsuarioBase(BaseModel):
    # datos personales básicos
    Nombre: str = Field(..., min_length=2, max_length=50, description="Nombre(s) del usuario")
    Password: str = Field(..., min_length=8, max_length=50, description="Contraseña")
    ApellidoPaterno: str = Field(..., min_length=2, max_length=50, description="Apellido paterno")
    ApellidoMaterno: Optional[str] = Field(None, max_length=50, description="Apellido materno (opcional)")
    
    # datos de contacto y autenticación
    Correo: EmailStr = Field(..., description="Correo electrónico")
    Usuario: str = Field(..., min_length=2, max_length=20, description="Nombre de usuario para login")
    
    # datos de control
    FechaNacimiento: date = Field(..., description="Fecha de nacimiento (YYYY-MM-DD)")
    Status: bool = Field(default=True, description="Estado activo/inactivo")
    Fecha_registro: date = Field(default_factory=date.today, description="Fecha de registro automática")

