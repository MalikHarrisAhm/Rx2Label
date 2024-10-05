from fastapi import FastAPI
from models import ImageProcess, ImageProcessResponse


app = FastAPI()


@app.post("/process-image")
def send_image(data: ImageProcess):
    print(data.base64_img)
    return ImageProcessResponse(prescriptionText="test", error=True, reason="A reason", validate_result=True).model_dump()


@app.get("/")
def read_root():
    return "OK"
