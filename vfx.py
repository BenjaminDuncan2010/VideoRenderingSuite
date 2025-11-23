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

def ghosting_effect(frames, alpha=0.7):
    
    """
    """
    
    prev = None
    for frame in frames:
        if prev is not None:
            frame = cv2.addWeighted(frame, alpha, prev, 1 - alpha, 0)
            prev = frame
            
            
def sobelEdgeDetection(inputImg, display=True):
    
    """
    """
    
    sobelx = cv2.Sobel(inputImg, cv2.CV_64F, 1, 0, ksize=3)  # Horizontal edges
    sobely = cv2.Sobel(inputImg, cv2.CV_64F, 0, 1, ksize=3)  # Vertical edges

    # Compute gradient magnitude
    gradient_magnitude = cv2.magnitude(sobelx, sobely)

    # Convert to uint8
    gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)

    # Display result
    if display:
        plt.imshow(gradient_magnitude, cmap='gray')
        
    return gradient_magnitude

def laplacianEdgeDetection(inputImg, display=True):
    
    """
    """
    
    laplacian = cv2.Laplacian(inputImg, cv2.CV_64F)
 
    # Convert to uint8
    laplacian_abs = cv2.convertScaleAbs(laplacian)

    # Display result
    plt.imshow(laplacian_abs, cmap='gray')
    
def cartoonify(inputImg, mode, d=9, sigmaColor=75, sigmaSpace=75, display=False):  
    
    """
    """
    
    if mode == 'Sobel':
        blurred = cv2.bilateralFilter(inputImg, d=d, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)
        edges = sobelEdgeDetection(inputImg, display=False)
        cartoon = cv2.subtract(blurred, edges)
        
    elif mode == 'Laplacian':
        blurred = cv2.bilateralFilter(inputImg, d=d, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)
        edges = laplacianEdgeDetection(inputImg, display=False)
        cartoon = cv2.subtract(blurred, edges)
        
    elif mode == 'N':
        cartoon = inputImg
        
    if display:
        plt.imshow(cartoon, cmap='gray')
    
    return cartoon
    