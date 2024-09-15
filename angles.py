import numpy as np
import cv2

#angle calculation

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

# def get_angles(lndmrk):
#     shoulder = lndmrk[11] #left shoulder position in model
#     elbow = lndmrk[13]
#     wrist = lndmrk[15]
#     hip = lndmrk[23]  # Assuming you have hip keypoints

#     elbow_angle = calculate_angle(shoulder, elbow, wrist) #check if you need .x and .y here idk 
#     shoulder_angle = calculate_angle(elbow, shoulder, hip)
    
#     return elbow_angle, shoulder_angle


