import socket
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

# dirección ip y puerto para la comunicación udp
UDP_IP = "192.168.4.1"
UDP_PORT = 5000

def send_udp_command(command: str):
    # envía el comando por udp al dispositivo
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(command.encode(), (UDP_IP, UDP_PORT))

@router.get("/manejo", response_class=HTMLResponse)
async def mostrar_pagina_manejo(request: Request):
    # muestra la página de control
    return templates.TemplateResponse(
        "Manejo.html",
        {
            "request": request,
            "title": "Panel de Manejo",
            "usuario": request.cookies.get("current_user")
        }
    )

# rutas para los comandos de movimiento
@router.post("/manejo/command/w")
async def command_up():
    send_udp_command("W")
    return {"status": "OK", "command": "ADELANTE"}

@router.post("/manejo/command/s")
async def command_down():
    send_udp_command("S")
    return {"status": "OK", "command": "ATRAS"}

@router.post("/manejo/command/a")
async def command_left():
    send_udp_command("A")
    return {"status": "OK", "command": "IZQUIERDA"}

@router.post("/manejo/command/d")
async def command_right():
    send_udp_command("D")
    return {"status": "OK", "command": "DERECHA"}