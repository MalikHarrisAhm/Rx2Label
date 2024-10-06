from turtle import up
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from modules.buckets import upload_image
from models import ImageProcess, ImageProcessResponse
import base64
import os
from modules.mistral import process_image
import time

tmp_dir = os.path.join(os.path.dirname(__file__), 'tmp')


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.mount("/tmp", StaticFiles(directory=tmp_dir), name="tmp")


@app.post("/process-image")
async def send_image(data: ImageProcess):
    print("recieved image")
    image_data = base64.b64decode(data.base64_img)

    img_path = f"{os.path.dirname(__file__)}/tmp/tmp.png"

    with open(img_path, "wb") as file:
        file.write(image_data)

    public_path = upload_image(img_path)
    print(public_path)

    time.sleep(5)

    return process_image(public_path)


@app.get("/")
async def read_root():
    return "OK"
