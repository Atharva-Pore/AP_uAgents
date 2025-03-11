from flask import Flask, request, jsonify
from flask_cors import CORS
from fetchai.crypto import Identity
from fetchai import fetch
from fetchai.registration import register_with_agentverse
from fetchai.communication import parse_message_from_agent, send_message_to_agent
import logging
import os
import librosa
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import matplotlib
import json

matplotlib.use('Agg')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)

# Initialize client identity
client_identity = None

# Function to plot and save spectrogram
def plot_spectrogram(audio_path, save_path, dpi=300):
    y, sr = librosa.load(audio_path, sr=None)
    D = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    S_db = librosa.amplitude_to_db(D, ref=np.max)
    plt.figure(figsize=(10, 5), dpi=dpi)
    librosa.display.specshow(S_db, sr=sr, hop_length=512, x_axis='time', y_axis='log', cmap='magma')
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0, format='png')
    plt.close()

# Function to process the WAV file
def process_wav_file(file_name, destination_folder, dpi=100):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    img_path = os.path.join(destination_folder, os.path.basename(file_name).replace(".wav", ".png"))
    plot_spectrogram(file_name, img_path, dpi=dpi)
    logger.info(f"Saved spectrogram for {file_name} at {img_path}")

    return img_path

# Function to register agent
def init_client():
    """Initialize and register the client agent."""
    global client_identity
    try:
        client_identity = Identity.from_seed(os.getenv("GET_SPECTRA_KEY"), 0)
        logger.info(f"Client agent started with address: {client_identity.address}")

        readme = """
            ![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
            domain:domain-of-your-agent
            <description>This Agent can only send a message to another agent in string format.</description>
            <use_cases><use_case>To send a message to another agent.</use_case></use_cases>
        """

        register_with_agentverse(
            identity=client_identity,
            url="http://localhost:5008/api/webhook",
            agentverse_token=os.getenv("GET_SPECTRA_API_KEY"),
            agent_title="Get Spectra Agent",
            readme=readme
        )
        logger.info("Quickstart agent registration complete!")

    except Exception as e:
        logger.error(f"Initialization error: {e}")
        raise

@app.route('/api/send-data', methods=['POST'])
def send_data():
    """Send payload to the selected agent based on provided address."""
    try:
        data = request.json
        payload = data.get('payload')
        agent_address = data.get('agentAddress')

        if not payload or not agent_address:
            return jsonify({"error": "Missing payload or agent address"}), 400

        wav_file = payload.get('wav_file')
        destination_folder = payload.get('destination_folder')
        dpi = payload.get('dpi', 100)

        if not wav_file or not destination_folder:
            return jsonify({"error": "Invalid payload structure"}), 400

        img_path = process_wav_file(wav_file, destination_folder, dpi)
        payload_data = {"img_paths": img_path}

        logger.info(f"Sending payload to agent: {agent_address}")
        logger.info(f"Payload: {payload_data}")

        # Send JSON-serialized payload to the agent
        send_message_to_agent(
            client_identity,
            agent_address,
            json.dumps(payload_data)  # Serialize to JSON string
        )

        return jsonify({"status": "request_sent", "agent_address": agent_address, "payload": payload_data})

    except Exception as e:
        logger.error(f"Error sending data to agent: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    load_dotenv()  # Load environment variables
    init_client()  # Register your Agent on Agentverse
    app.run(host="0.0.0.0", port=5008)
