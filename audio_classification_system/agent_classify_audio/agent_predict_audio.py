'''
Author: Atharva Pore
'''

#improts
import os
import cv2
import torch
import numpy as np
from PIL import Image
from torchvision import models
import matplotlib.pyplot as plt
from uagents import Agent, Context, Model
import torchvision.transforms as transforms

#global variable
test_image_path = ''

# define the message envolope
class initSpectraProcessing(Model):
    image_path:str

#define the agent
agentPredictSpectra = Agent(
    name = 'predict_spectra',
    port = 5055,
    endpoint = 'http://localhost:5055/submit'
)

# load model
def load_model(model_path, device):
    """
    Load a trained ResNet18 model for deepfake detection.
    
    Args:
        model_path (str): Path to the trained model file.
        device (torch.device): Device to load the model onto.
    
    Returns:
        model (torch.nn.Module): Loaded and ready-to-use model.
    """
    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, 2)  # 2 classes: Deepfake, Original
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    return model

#transform the given image according to the model
def get_transform():
    """
    Define the image transformations used for preprocessing.

    Returns:
        transform (torchvision.transforms.Compose): Image transformations.
    """
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])
    return transform

# get prediction
def predict_image(model, image_path, transform, device):
    """
    Predict the class of an image using a trained model.
    
    Args:
        model (torch.nn.Module): Trained model.
        image_path (str): Path to the input image.
        transform (torchvision.transforms.Compose): Image preprocessing transformations.
        device (torch.device): Device to perform inference on.

    Returns:
        str: Predicted label ("Deepfake" or "Original").
    """
    image = Image.open(image_path).convert("RGB")  # Load Image
    image = transform(image).unsqueeze(0).to(device)  # Apply Transform & Add batch dimension

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)  # Get predicted class

    class_names = ["Deepfake", "Original"]  # Label Mapping
    return class_names[predicted.item()]

#define handlers on which agent will work
@agentPredictSpectra.on_event('startup')
async def startup_handler(ctx:Context):
    ctx.logger.info(f'My Name is {ctx.agent.name} and My Address is {ctx.agent.address}')

@agentPredictSpectra.on_message(model = initSpectraProcessing)
async def message_handler(ctx:Context, sender:str, img_info:initSpectraProcessing):

    #get the confirmation over how many images got tranfered and from whom
    ctx.logger.info(f'I have received the message from {sender}')
    ctx.logger.info(f'We have received {img_info.image_path} image.')
    
    # define the test image path
    global test_image_path
    test_image_path = img_info.image_path

    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Paths
    model_path = "/Users/atharvapore/Desktop/Masters/Sem_04/Fetch_ai_Internship/cohort_3_session/spectrogram_analysis_agent/final_deepfake_audio_classifier.pth"
    
    # Load model and transformation
    model = load_model(model_path, device)
    transform = get_transform()
    
    # Predict and print result
    prediction = predict_image(model, test_image_path, transform, device)
    print(f"*******Prediction: {prediction}*******")

# load model
def load_model(model_path, device):
    """
    Load a trained ResNet18 model for deepfake detection.
    
    Args:
        model_path (str): Path to the trained model file.
        device (torch.device): Device to load the model onto.
    
    Returns:
        model (torch.nn.Module): Loaded and ready-to-use model.
    """
    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, 2)  # 2 classes: Deepfake, Original
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    return model

#transform the given image according to the model
def get_transform():
    """
    Define the image transformations used for preprocessing.

    Returns:
        transform (torchvision.transforms.Compose): Image transformations.
    """
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])
    return transform

# get prediction
def predict_image(model, image_path, transform, device):
    """
    Predict the class of an image using a trained model.
    
    Args:
        model (torch.nn.Module): Trained model.
        image_path (str): Path to the input image.
        transform (torchvision.transforms.Compose): Image preprocessing transformations.
        device (torch.device): Device to perform inference on.

    Returns:
        str: Predicted label ("Deepfake" or "Original").
    """
    image = Image.open(image_path).convert("RGB")  # Load Image
    image = transform(image).unsqueeze(0).to(device)  # Apply Transform & Add batch dimension

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)  # Get predicted class

    class_names = ["Deepfake", "Original"]  # Label Mapping
    return class_names[predicted.item()]

#main
if __name__ == '__main__':

    #run the agent
    agentPredictSpectra.run()
    