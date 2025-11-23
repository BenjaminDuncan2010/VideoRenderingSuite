import cv2
import pandas as pd
import numpy as np
import scipy 
import matplotlib.pyplot as plt
from matplotlib import colormaps as cmps
import scipy.io as sio
from PIL import Image
import scipy.signal as signal
import pdb
from PIL import Image
import librosa           # Beat detection, BPM analysis
import statistics
import moviepy

def get_audio_report(file_path):
    
    """
    """
    
    (sig, rate) = librosa.load(file_path, sr=None)
    tempo, beats = librosa.beat.beat_track(y=sig, sr=rate)
    frames = librosa.frames_to_time(beats, sr=rate)
    
    frame_rate = statistics.mode(frames[i+1] - frames[i] for i in range(len(frames)-1))
    return tempo, beats, frames, frame_rate 