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

#the progress bar is only for the elbow as of now 
MAX_ANGLE = 160 #fully extended position 
MIN_ANGLE = 70 #Down position of the pushup (bar max size)

def draw_live_vertical_progress_bar(image, elbow_angle, bar_height=300):
    """Draw a live vertical progress bar based on the current elbow angle."""
    # Calculate the progress based on the elbow angle
    if elbow_angle > MAX_ANGLE:
        progress = 0
    else:
        progress = max(0, min(1, (MAX_ANGLE - elbow_angle) / (MAX_ANGLE - MIN_ANGLE)))

    # Progress bar background (gray)
    bar_x = 20 # x position of the bar
    bar_y = 160  # y position of the bar's bottom
    cv2.rectangle(image, (bar_x, bar_y), (bar_x + 100, bar_y + bar_height), (50, 50, 50), -1)

    # Progress fill (yellow or green depending on stage)
    bar_fill_height = int(progress * bar_height)
    bar_color = (0, 255, 0) if elbow_angle <= 90 else (0, 255, 255)  #Green when in down position
    cv2.rectangle(image, (bar_x, bar_y + (bar_height - bar_fill_height)), (bar_x + 100, bar_y + bar_height), bar_color, -1)
