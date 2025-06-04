import cv2
import numpy as np
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()

# configuración de la cámara esp32
ESP32_IP = "192.168.4.1"
STREAM_URL = f"http://{ESP32_IP}:81/stream"

# cargamos las clases que puede detectar el modelo
# estas son las etiquetas de los objetos que el modelo puede reconocer
classNames = []
with open('app/models/coco.names', 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# rutas de los archivos del modelo
# necesitamos tanto el archivo de configuración como los pesos entrenados
configPath = 'app/models/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'app/models/frozen_inference_graph.pb'

# inicializamos el modelo de detección
# configuramos los parámetros para el preprocesamiento de las imágenes
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)  # tamaño de entrada para el modelo
net.setInputScale(1.0 / 127.5)  # escala para normalizar los valores de píxeles
net.setInputMean((127.5, 127.5, 127.5))  # media para normalización
net.setInputSwapRB(True)  # intercambia los canales rojo y azul

# control para activar/desactivar la detección
# cuando es true, se detectan objetos en el video
detectar = False

def generar_frames():
    # conectamos con el stream de video
    cap = cv2.VideoCapture(STREAM_URL)
    if not cap.isOpened():
        print("❌ No se pudo abrir el stream de video")
        return

    while True:
        # leemos frame por frame del video
        ret, frame = cap.read()
        if not ret:
            continue

        # si la detección está activa, procesamos el frame
        if detectar:
            # detectamos objetos con una confianza mínima del 50%
            classIds, confs, bbox = net.detect(frame, confThreshold=0.5)
            if len(classIds) != 0:
                for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                    # dibujamos el rectángulo y la etiqueta para cada detección
                    # mostramos el nombre del objeto y su porcentaje de confianza
                    label = f'{classNames[classId - 1]}: {int(round(confidence * 100))}%'
                    cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(frame, label, (box[0], box[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # convertimos el frame a bytes para streaming
        # esto permite enviar el video a través de la red
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@router.post("/deteccion/toggle")
def toggle_deteccion():
    # activa o desactiva la detección
    # este endpoint permite controlar si queremos detectar objetos o no
    global detectar
    detectar = not detectar
    return {"status": "started" if detectar else "stopped"}

@router.get("/deteccion_feed")
def video_feed():
    # endpoint para el stream de video
    # devuelve el video en tiempo real con las detecciones si están activas
    return StreamingResponse(generar_frames(),
                          media_type='multipart/x-mixed-replace; boundary=frame')