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

from beatmatcher import *

def extend_image_to_array(file_path, audio_file_path, frame_count, multiplier=2):
    
    """
    Take one image and duplicate it to a specified number of frames, separate by a 
    frame-rate established by a component piece of audio
    
    """
    
    images = []
    
    #### This bit will change, just acquiring image from market video for ease of use as that's what I have uploaded
    cap = cv2.VideoCapture(file_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 10)
    res, frame = cap.read()
    im = Image.fromarray(frame)
    
    i = 1
    while i < frame_count:
        images.append(im)
        i += 1
        
    return images


def split_rgb_frame(inputImg):
    
    """
    """
    
    if type(inputImg) == np.array:
        b, g, r = Image.fromarray(inputImg[:,:,0]), Image.fromarray(inputImg[:,:,1]), Image.fromarray(inputImg[:,:,2])
        
    else: 
        b, g, r = Image.fromarray(np.array(inputImg)[:,:,0]), Image.fromarray(np.array(inputImg)[:,:,1]), Image.fromarray(np.array(inputImg)[:,:,2])
    
    return b, g, r

def video_to_image_array(file_path, audio_file_path, frame_interval=1):
    
    """
    """
    
    cap = cv2.VideoCapture(file_path)
    cap.get(cv2.CAP_PROP_FRAME_COUNT)
    broken_frames = np.arange(0, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), frame_interval)
    
    if audio_file_path != None: 
        tempo, beats, frames, frame_rate = get_audio_report(audio_file_path)
    
    images = []
    for i in range(len(broken_frames)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, broken_frames[i])
        res, frame = cap.read()
        im = Image.fromarray(frame)
        images.append(im)
        
    return images

def export_video_to_image_array(file_path, audio_file_path, output_file_path, multiplier=2, frame_interval=10):
    
    """
    """
    
    cap = cv2.VideoCapture(file_path)
    cap.get(cv2.CAP_PROP_FRAME_COUNT)
    broken_frames = np.arange(0, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), frame_interval)
    
    tempo, beats, frames, frame_rate = get_audio_report(audio_file_path)
    
    filepaths_list = []
    for i in range(len(broken_frames)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, broken_frames[i])
        res, frame = cap.read()
        im = Image.fromarray(frame).save(f"temp/tempFrame_{i}.jpeg")
        filepaths_list.append(f"temp/tempFrame_{i}.jpeg")
        
    clip = moviepy.ImageSequenceClip([f"{img}" for img in filepaths_list], fps = 1/float(frame_rate) * multiplier)
    clip = clip.set_audio(moviepy.AudioFileClip(audio_file_path))
    clip.write_videofile(output_file_path)