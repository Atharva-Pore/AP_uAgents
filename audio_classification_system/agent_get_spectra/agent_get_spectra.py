'''
Author: Aishwarya Dekhane
'''

import os
import librosa
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
import argparse
from uagents import Agent, Context, Model

# Constants
DATA_DIR = '/Users/atharvapore/Desktop/Masters/Sem_03/Thesis/activation_layer/data'
SPEAKER_NAME = 'DonaldTrump_v2'
TRAIN = 'train'
TEST = 'test'
DEEPFAKE = 'E2tts_img'
ORIGINAL = 'original_img'

# Global variables
img_paths = ''

# Define the envelope to send the images to process agent
class initSpectraProcessing(Model):
    image_path:str

# Define the agent
agentGetSpectra = Agent(
    name='get_spectra',
    port=5053,
    endpoint='http://localhost:5053/submit'
)

spectraProcessingAgentAddress = 'agent1q2djlg27wdcyj872q60x3y7yj8n8pc475q9e5vhp4h8mlh544vmyyn7rsr0'

# Define the handler on which agent will work
@agentGetSpectra.on_event('startup')
async def startup_handler(ctx: Context):
    ctx.logger.info(f'Sending Spectrogram Image Paths for Processing...')
    await ctx.send(spectraProcessingAgentAddress, initSpectraProcessing(image_path=img_paths))

# Function to plot and save spectrogram
def plot_spectrogram(audio_path, save_path, dpi=300):
    # Load the audio file
    y, sr = librosa.load(audio_path, sr=None)

    # Compute the Short-Time Fourier Transform (STFT)
    D = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))

    # Convert to dB (log scale)
    S_db = librosa.amplitude_to_db(D, ref=np.max)

    # Plot spectrogram
    plt.figure(figsize=(10, 5), dpi=dpi)
    librosa.display.specshow(S_db, sr=sr, hop_length=512, x_axis='time', y_axis='log', cmap='magma')

    # Save as RGB image
    plt.axis('off')  # Remove axis for saving as an image
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0, format='png')
    plt.close()

# Function to process the wav file
def process_wav_file(file_name, destination_folder, dpi=100):
    global img_paths
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    audio_path = file_name
    img_paths = os.path.join(destination_folder, os.path.basename(file_name).replace(".wav", ".png"))

    # Plot and save spectrogram for the wav file
    plot_spectrogram(audio_path, img_paths, dpi=dpi)
    print(f"Saved spectrogram for {file_name} at {img_paths}")

if __name__ == '__main__':
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Process a .wav file and generate its spectrogram.")
    parser.add_argument('file_name', type=str, help="Path to the .wav file")
    destination_folder = '/Users/atharvapore/Desktop/Masters/Sem_04/Fetch_ai_Internship/cohort_3_session/spectrogram_analysis_agent/temp'

    args = parser.parse_args()

    # Ensure the file is a .wav file
    if not args.file_name.lower().endswith('.wav'):
        print("Error: The input file must be a .wav file.")
        exit(1)

    process_wav_file(args.file_name, destination_folder, 100)

    # Run the agent
    agentGetSpectra.run()
