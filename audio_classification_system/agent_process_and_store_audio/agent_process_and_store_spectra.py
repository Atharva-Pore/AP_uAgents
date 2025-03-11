'''
Author: Atharva Pore
'''

#improts
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from uagents import Agent, Context, Model

#global variable
img_paths = ''

# Corresponding output directories for original and deepfake images
output_dir:str = '/Users/atharvapore/Desktop/Masters/Sem_04/Fetch_ai_Internship/cohort_3_session/spectrogram_analysis_agent/processed_temp'

# define the message envolope
class initSpectraProcessing(Model):
    image_path:str

#define the agent
agentProcessSpectra = Agent(
    name = 'process_spectra',
    port = 5054,
    endpoint = 'http://localhost:5054/submit'
)

agentPredictAddress = 'agent1qf37m5z9rh5p72ehnhueua5hdhjt0q4377n7runyqaxwm6ktf93kuxm3pw8'

#define handlers on which agent will work
@agentProcessSpectra.on_event('startup')
async def startup_handler(ctx:Context):
    ctx.logger.info(f'My Name is {ctx.agent.name} and My Address is {ctx.agent.address}')

@agentProcessSpectra.on_message(model = initSpectraProcessing)
async def message_handler(ctx:Context, sender:str, img_info:initSpectraProcessing):
    global img_paths

    #get the confirmation over how many images got tranfered and from whom
    ctx.logger.info(f'I have received the message from {sender}')
    ctx.logger.info(f'We have received {img_info.image_path} image.')
    
    img_paths = img_info.image_path

    # Process and store images
    status = await process_and_store_spectrogram(img_info.image_path, output_dir)
    ctx.logger.info(status)

    if 'Saved' in status:
        img_paths = img_info.image_path
        await ctx.send(agentPredictAddress, initSpectraProcessing(image_path=img_paths))

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

async def process_and_store_spectrogram(path: str, output_dir:str) -> str:
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

    return f"Saved processed spectrogram at: {save_path}"

#main
if __name__ == '__main__':

    #run the agent
    agentProcessSpectra.run()
