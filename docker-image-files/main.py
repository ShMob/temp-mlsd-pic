# main.py
from fastapi import FastAPI
from fastapi import UploadFile , File
from torchvision.models import efficientnet_b0
from torchvision import transforms
import torch
import numpy as np
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
import psutil
import mlflow
import time
import random
from enum import Enum
from predictor import Predictor
# import pyuac

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MappingType(Enum):
    MLP = 'mlp'
    Transformer = 'transformer'

model_weights_path = 'prefix_only_10_8_10-009.pt'
prefix_length_clip = 10
num_layers = 8
prefix_length = 10
prefix_size = 768
mapping_type = 'transformer'

mapping_type = {'mlp': MappingType.MLP, 'transformer': MappingType.Transformer}[mapping_type]
print("Before predictor.py")
predictor = Predictor(model_weights_path, mapping_type=mapping_type,clip_length=prefix_length_clip, num_layers=num_layers, prefix_length=prefix_length, prefix_size=prefix_size)

# model = efficientnet_b0(pretrained=True)
# model.eval()
# MLflow configuration
# mlflow.set_tracking_uri("http://mlflow-server:5000")


def model_predict(image, predictor):
    return predictor.predict(image, use_beam_search=False)

@app.post("/predict")
def predict(image: UploadFile = File(...)):
    # print("predicting...")
    image = Image.open(image.file)
    image = np.array(image.convert('RGB'))

    with mlflow.start_run() as run:
        # Measure latency
        start_time = time.time()
        output_caption = model_predict(image, predictor)
        latency = time.time() - start_time

        # Log latency
        mlflow.log_metric("latency", latency)

        # Log word count of the generated caption
        word_count = len(output_caption.split())
        mlflow.log_metric("word_count", word_count)

        # Log system metrics
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        mlflow.log_metric("cpu_usage", cpu_usage)
        mlflow.log_metric("memory_usage", memory_usage)

        # Occasionally log the generated caption (for example, 5% of the times)
        if random.random() < 0.05:
            mlflow.log_text(output_caption, "sample_caption.txt")

        print(output_caption)

    return {"class": output_caption}
    # image = Image.open(image.file)
    # image = np.array(image.convert('RGB'))
    # # reading the image With PIL.image
    # # tensor = preprocess_image(image)
    # output = model_predict(image, predictor)
    # print(output)
    # # _, predicted_idx = torch.max(output.data, 1)
    # return {"class": output.replace("[CLS] ", "").replace("[SEP]", ".")}

# def preprocess_image(image):
#     # Preprocessing logic
#     tensor = transform(image).unsqueeze(0)
#     return tensor
print("after method definitions!")

if __name__ == "__main__":
    import uvicorn

    # if not pyuac.isUserAdmin():
    #     print("Re-launching as admin!")
    #     pyuac.runAsAdmin()

    uvicorn.run(app, host="0.0.0.0", port=8000)
