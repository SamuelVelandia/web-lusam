# modelo para los mensajes del chat
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class MensajeChat(BaseModel):
    # información del mensaje
    stream_id: str = Field(..., description="ID del stream al que pertenece el mensaje")
    usuario: str = Field(..., description="Usuario que envía el mensaje")
    mensaje: str = Field(..., description="Contenido del mensaje")
    timestamp: datetime = Field(default_factory=datetime.now, description="Fecha y hora del mensaje")
    tipo: str = Field(default="chat", description="Tipo de mensaje (chat por defecto)")
    color: Optional[str] = Field(None, description="Color personalizado del mensaje") 