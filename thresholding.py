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

binary_thresholding_options = {
    '1': cv2.THRESH_BINARY,
    '2': cv2.THRESH_BINARY_INV,
    '3': cv2.THRESH_TRUNC,
    '4': cv2.THRESH_TOZERO,
    '5': cv2.THRESH_TOZERO_INV
}

adaptive_thresholding_options = {
    '1': cv2.ADAPTIVE_THRESH_MEAN_C,
    '2': cv2.ADAPTIVE_THRESH_GAUSSIAN_C
}

colormapChannels = {
    '1': ['Reds', 'Greens', 'Blues'],
    '2': ['YiOrBr', 'PuBuGn', 'Greys']
}

def binaryThresholding(input_image, frame_number=0, lower_range=177, upper_range=255, thresholdoption='1', colorMap='1', save=False, vis=True):
    
    """
    Newer version intended for use with single individual image 
    """
    
    filePath = ""
    imgChannels = []
    npImage = np.array(input_image)
    for channel in range(len(npImage[0,0])):
        #axs[channel].imshow(cv2.threshold(frame[:,:,channel], lower_range, upper_range, binary_thresholding_options[thresholdoption])[1], cmap=colormapChannels[colorMap][channel]) ### FIND A WAY TO RANDOMISE THE LOWER THRESHOLD 
        imgChannels.append(cv2.threshold(npImage[:,:,channel], lower_range, upper_range, binary_thresholding_options[thresholdoption])[1])### FIND A WAY TO RANDOMISE THE LOWER THRESHOLD         

    rgb = cv2.merge((imgChannels[0], imgChannels[1], imgChannels[2]))

    if save:
        Image.fromarray(rgb).save(f"temp/tempFrame_{frame_number}.jpeg")
        filePath = f"temp/tempFrame_{frame_number}.jpeg"

    if vis:
        axs[image].imshow(rgb)
        axs[image].set_title(f"Lower Threshold Range: {lower_range}, Upper Threshold Range: {upper_range}, Threshold Option: {binary_thresholding_options[thresholdoption]}")
        
    return rgb, filePath

def binaryThresholding_isolateBand(input_image, lower_range=177, upper_range=255, thresholdoption='5'):
    
    """
    """
    
    npImage = np.array(input_image)
    thresholdImg = cv2.threshold(npImage, lower_range, upper_range, binary_thresholding_options[thresholdoption])[1]### FIND A WAY TO RANDOMISE THE LOWER THRESHOLD         

    return Image.fromarray(thresholdImg)

def adaptiveThresholding(input_path, frame_number, upper_range=255, thresholdoption='1'):
    
    """
    """
    
    cap = cv2.VideoCapture(input_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    res, frame = cap.read()    
    
    fig, axs = plt.subplots(len(frame[0,0]))

    for channel in range(len(frame[0,0])):
        axs[channel].imshow(cv2.adaptiveThreshold(frame[:,:,channel], upper_range, adaptive_thresholding_options[thresholdoption], cv2.THRESH_BINARY, 11, 2), cmap='Reds') ### FIND A WAY TO RANDOMISE THE LOWER THRESHOLD 
        ### WITHIN A CERTAIN RANGE
        
def adaptiveThresholding_isolateBand(input_image, upper_range=255, thresholdoption='1'):

    """
    """
    
    npImage = np.array(input_image)
    thresholdImg = cv2.adaptiveThreshold(npImage, upper_range, adaptive_thresholding_options[thresholdoption], cv2.THRESH_BINARY, 11, 2) ### FIND A WAY TO RANDOMISE THE LOWER THRESHOLD 
        ### WITHIN A CERTAIN RANGE
        
    return Image.fromarray(thresholdImg)
        
        
def applyThreshold(input_image, mode, upper_range=255, lower_range=177, thresholdoption='1', colorMap='1'):
    if mode == 'Binary':    
        threshImage = binaryThresholding_isolateBand(input_image, upper_range=upper_range, lower_range=lower_range, thresholdoption=thresholdoption)
        
    elif mode == 'Adaptive':  
        threshImage = adaptiveThresholding_isolateBand(input_image)
        
    elif mode == 'N':  
        threshImage = input_image
        
    return threshImage
        
    
    