from pydantic import BaseModel


class ImageProcess(BaseModel):
    base64_img: str


class ImageProcessResponse(BaseModel):
    prescriptionText: str
    error: bool
    reason: str
    validate_result: bool
