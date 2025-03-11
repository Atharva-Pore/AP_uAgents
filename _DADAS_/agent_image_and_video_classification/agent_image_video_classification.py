import cv2
import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.models import load_model
from uagents import Agent, Context, Model

# Define the request model
class DeepfakeRequest(Model):
    file_path: str
    sender_address: str

# Define the response model
class DeepfakeResponse(Model):
    frame_predictions: list[str]
    avg_prediction: str

# Load pre-trained models
model_Vgg16 = load_model("path/to/model/model_epoch_37-val_loss_0.5412.h5")
model_InceptionV3 = load_model("path/to/model/Inception_net_epoch_50_loss_0.5707.h5")

# Define the main agent
mainAgent = Agent(
    name='video_image_classification_agent',
    port=5068,
    endpoint='http://localhost:5068/submit',
    seed='video_image_classification_seed'
)
# Preprocess function for VGG16
def preprocess_for_VGG_(frame):
    frame = cv2.resize(frame, (224, 224))
    frame = frame / 255.0
    frame = np.expand_dims(frame, axis=0)
    return frame

# Preprocess function for InceptionV3
def preprocess_for_inception(frame):
    frame = cv2.resize(frame, (299, 299))
    frame = np.expand_dims(frame, axis=0)
    frame = preprocess_input(frame)
    return frame

# Split video into frames
def split_video_into_frames(video_path):
    video = cv2.VideoCapture(video_path)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    interval = fps
    
    frames = []
    frame_count = 0

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        if frame_count % interval == 0:
            frames.append(frame)
        frame_count += 1

    video.release()
    return frames

# Get predictions for frames
def get_predictions_for_frames(frames, model_Vgg16, model_InceptionV3, weight_a=0.6, weight_b=0.4):
    predictions = []
    combined_probabilities = []

    for frame in frames:
        vgg_frame = preprocess_for_VGG_(frame)
        inception_frame = preprocess_for_inception(frame)

        VGG_predictions = model_Vgg16.predict(vgg_frame)
        Inception_predictions = model_InceptionV3.predict(inception_frame)

        combined_prediction = (weight_a * VGG_predictions) + (weight_b * Inception_predictions)
        combined_probabilities.append(combined_prediction)
        final_prediction = np.argmax(combined_prediction)
        predictions.append("Real" if final_prediction == 1 else "Fake")

    avg_probabilities = np.mean(combined_probabilities, axis=0)
    avg_final_prediction = np.argmax(avg_probabilities)
    avg_result = "Real" if avg_final_prediction == 1 else "Fake"

    return predictions, avg_result

@mainAgent.on_event('startup')
async def startup_handler(ctx: Context):
    ctx.logger.info(f'Agent {ctx.agent.name} started at {ctx.agent.address}')

# Handler for receiving query
@mainAgent.on_message(model=DeepfakeRequest)
async def handle_query(ctx: Context, sender: str, request: DeepfakeRequest):
    file_path = request.file_path
    ctx.logger.info(f"Received query from {request.sender_address}: {file_path}")
    
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        img = cv2.imread(file_path)
        vgg_frame = preprocess_for_VGG_(img)
        inception_frame = preprocess_for_inception(img)

        VGG_predictions = model_Vgg16.predict(vgg_frame)
        Inception_predictions = model_InceptionV3.predict(inception_frame)

        combined_predictions = (0.6 * VGG_predictions) + (0.4 * Inception_predictions)
        final_prediction = "Real" if np.argmax(combined_predictions) == 1 else "Fake"
        response = DeepfakeResponse(frame_predictions=[final_prediction], avg_prediction=final_prediction)
        await ctx.send(request.sender_address, response)
    elif file_path.lower().endswith(('.mp4', '.avi', '.mov')):
        frames = split_video_into_frames(file_path)
        predictions, avg_result = get_predictions_for_frames(frames, model_Vgg16, model_InceptionV3)
        response = DeepfakeResponse(frame_predictions=predictions, avg_prediction=avg_result)
        await ctx.send(request.sender_address, response)
    
    else:
        await ctx.send(request.sender_address, 
                       DeepfakeResponse(frame_predictions=[], avg_prediction="Error: Unsupported file type."))

if __name__ == '__main__':
    mainAgent.run()
