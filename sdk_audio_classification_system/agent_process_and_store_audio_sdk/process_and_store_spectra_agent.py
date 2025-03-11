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

# Constants
MODEL_PATH = "/Users/atharvapore/Desktop/Masters/Sem_04/Fetch_ai_Internship/cohort_3_session/spectrogram_analysis_agent/final_deepfake_audio_classifier.pth"
SPECTRA_DIR = "/Users/atharvapore/Desktop/Masters/Sem_04/Fetch_ai_Internship/cohort_3_session/spectrogram_analysis_sdk/temp"
PREDICT_SPECTRA_AGENT_ADDRESS = "agent1qw24cvfndne9jur9vlawmd4q92mhu6v4yhe34gttvxg8ld066v965eunqma"
# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#define image processing functions
def load_spectrogram(path: str) -> np.ndarray:
    """Load grayscale spectrogram image from the specified path."""
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

def threshold_spectrogram(spectrogram: np.ndarray, threshold_value: int = 120) -> np.ndarray:
    """Apply binary threshold to the spectrogram."""
    _, thresholded = cv2.threshold(spectrogram, threshold_value, 255, cv2.THRESH_BINARY)
    return thresholded

def erode_spectrogram(spectrogram: np.ndarray, kernel_size: tuple[int, int] = (3, 3), iterations: int = 1) -> np.ndarray:
    """Perform erosion on the spectrogram."""
    kernel: np.ndarray = np.ones(kernel_size, np.uint8)
    return cv2.erode(spectrogram, kernel, iterations=iterations)

def dilate_spectrogram(spectrogram: np.ndarray, kernel_size: tuple[int, int] = (3, 3), iterations: int = 1) -> np.ndarray:
    """Perform dilation on the spectrogram."""
    kernel: np.ndarray = np.ones(kernel_size, np.uint8)
    return cv2.dilate(spectrogram, kernel, iterations=iterations)

def bitwise_and_spectrogram(original: np.ndarray, processed: np.ndarray) -> np.ndarray:
    """Perform bitwise AND operation between the original and processed spectrogram."""
    return cv2.bitwise_and(original, processed)

def process_and_store_spectrogram(path: str, output_dir:str) -> str:
    """Process spectrograms and store them in the specified directories."""
    print(f'Image path to be processed: {path}')
    
    # Load spectrogram
    spectrogram: np.ndarray = load_spectrogram(path)
    
    if spectrogram is None:
        print(f"Failed to load image at path: {path}")

    # Process steps: threshold -> erosion -> dilation -> bitwise AND
    thresholded: np.ndarray = threshold_spectrogram(spectrogram)
    eroded: np.ndarray = erode_spectrogram(thresholded)
    dilated: np.ndarray = dilate_spectrogram(eroded)
    final_result: np.ndarray = bitwise_and_spectrogram(spectrogram, dilated)

    # Store the processed result
    filename: str = os.path.basename(path)
    
    save_path: str = os.path.join(output_dir, filename)
    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(save_path, final_result)

    return save_path

# Function to register agent
def init_client():
    """Initialize and register the client agent."""
    global client_identity
    try:
        # Load the agent secret key from environment variables
        client_identity = Identity.from_seed(os.getenv("PROCESS_SPECTRA_KEY"), 0)
        logger.info(f"Client agent started with address: {client_identity.address}")

        readme = """
![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
**Description:** This agent will take the proccesses the spectrogram image and will send to predict agent to predict whether it is deepfake or original.
        """
        

        # Register the agent with Agentverse
        register_with_agentverse(
            identity=client_identity,
            url="http://localhost:5002/api/webhook",
            agentverse_token=os.getenv("PROCESS_AND_STORE_SPECTRA_API_KEY"),
            agent_title="Process and Store Spectra Agent",
            readme=readme
        )

        logger.info("Process and Store Spectra Agent!")

    except Exception as e:
        logger.error(f"Initialization error: {e}")
        raise

# @app.route('/api/send-data', methods=['POST'])
# def send_data():
#     """Send payload to the selected agent based on provided address."""
#     try:
#         data = request.json
#         payload = data.get('payload')
#         agent_address = data.get('agentAddress')

#         if not payload or not agent_address:
#             return jsonify({"error": "Missing payload or agent address"}), 400

#         img_path = payload.get('img_path')

#         if not img_path:
#             return jsonify({"error": "Invalid payload structure"}), 400
        
#         processed_img_path = process_and_store_spectrogram(img_path, SPECTRA_DIR)

#         payload_data = json.loads({"img_path":processed_img_path})

#         logger.info(f"Sending payload to agent: {agent_address}")
#         logger.info(f"Payload: {payload_data}")

#         # Send JSON-serialized payload to the agent
#         send_message_to_agent(
#             client_identity,
#             PREDICT_SPECTRA_AGENT_ADDRESS,
#             json.dumps(payload_data)  # Serialize to JSON string
#         )

#         return jsonify({"status": "request_sent", "agent_address": agent_address, "payload": payload_data})

#     except Exception as e:
#         logger.error(f"Error sending data to agent: {e}")
#         return jsonify({"error": str(e)}), 500

# app route to recieve the messages from other agents
@app.route('/api/webhook', methods=['POST'])
def webhook():
    """Handle incoming messages"""
    global agent_response, image_path, processed_img_path
    try:
        # Parse the incoming webhook message
        data = request.get_data().decode("utf-8")
        logger.info("Received response")

        message = parse_message_from_agent(data)
        agent_response = json.loads(message.payload)
        
        # Log the response for debugging
        print(type(agent_response))
        print(agent_response)

        processed_img_path = process_and_store_spectrogram(agent_response['img_paths'], SPECTRA_DIR)
        payload_data = {"img_paths":processed_img_path}
        
        logger.info(f"Sending payload to agent: {PREDICT_SPECTRA_AGENT_ADDRESS}")
        logger.info(f"Payload: {payload_data}")

        # Send JSON-serialized payload to the agent
        send_message_to_agent(
            client_identity,
            PREDICT_SPECTRA_AGENT_ADDRESS,
            json.dumps(payload_data)  # Serialize to JSON string
        )

        # Return a success message
        return jsonify({"status": "success", "agent_response": agent_response}), 200

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    load_dotenv()       # Load environment variables
    init_client()       #Register your agent on Agentverse
    app.run(host="0.0.0.0", port=5002)      
