from flask import Flask, request, jsonify
from flask_cors import CORS
from fetchai.crypto import Identity
from fetchai import fetch
from fetchai.registration import register_with_agentverse
from fetchai.communication import parse_message_from_agent, send_message_to_agent
import logging
import os
from dotenv import load_dotenv
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
import torch
import numpy as np
from PIL import Image
from torchvision import models
import torchvision.transforms as transforms

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)

# Initialising client identity to get registered on agentverse
client_identity = None 

#global variable
image_path = ''
processed_img_path = ''

# Paths
MODEL_PATH = "/Users/atharvapore/Desktop/Masters/Sem_04/Fetch_ai_Internship/cohort_3_session/spectrogram_analysis_agent/final_deepfake_audio_classifier.pth"

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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

# Function to register agent
def init_client():
    """Initialize and register the client agent."""
    global client_identity
    try:
        # Load the agent secret key from environment variables
        client_identity = Identity.from_seed(os.getenv("PREDICT_SPECTRA_KEY"), 0)
        logger.info(f"Client agent started with address: {client_identity.address}")

        readme = """
![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
**Description:** This agent will take the processed spectrogram image and will predict whether it is deepfake or original.
        """
        

        # Register the agent with Agentverse
        register_with_agentverse(
            identity=client_identity,
            url="http://localhost:5006/api/webhook",
            agentverse_token=os.getenv("PREDICT_AUDIO_API_KEY"),
            agent_title="Predict Spectra Agent",
            readme=readme
        )

        logger.info("Quickstart agent registration complete!")

    except Exception as e:
        logger.error(f"Initialization error: {e}")
        raise

# app route to recieve the messages from other agents
@app.route('/api/webhook', methods=['POST'])
def webhook():
    """Handle incoming messages"""
    global agent_response, image_path
    try:
        # Parse the incoming webhook message
        data = request.get_data().decode("utf-8")
        logger.info("Received response")

        message = parse_message_from_agent(data)
        #agent_response = message.payload
        agent_response = json.loads(message.payload)
        print(type(agent_response))
        print(agent_response)

        image_path = agent_response['img_paths']
        
        print(f'********Predicting: {image_path}********')

        # Load model and transformation
        model = load_model(MODEL_PATH, device)
        transform = get_transform()
    
        # Predict and print result
        prediction = predict_image(model, image_path, transform, device)

        logger.info(f"Prediction: {prediction}")
        return jsonify({"status": "success"})

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    load_dotenv()       # Load environment variables
    init_client()       #Register your agent on Agentverse
    app.run(host="0.0.0.0", port=5006)      
