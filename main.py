from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import torch
import io
from PIL import Image

app = FastAPI()

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    results = model(image)
    annotated = results.render()[0]
    annotated_image = Image.fromarray(annotated)

    buf = io.BytesIO()
    annotated_image.save(buf, format='JPEG')
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/jpeg")