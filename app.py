from fastapi import FastAPI, File, UploadFile
from inference import predict_image

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Coconut Disease API Running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = predict_image(image_bytes)
    return result
