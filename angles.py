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




#the progress bar is only for the elbow as of now 
MAX_ANGLE = 160 #fully extended position 
MIN_ANGLE = 70 #Down position of the pushup (bar max size)

def draw_live_vertical_progress_bar(image, elbow_angle, bar_height_pct=0.3, bar_width_pct=0.05, bar_x_pct=0.02, bar_y_pct=0.25):
    """Draw a live vertical progress bar based on the current elbow angle, with relative positioning."""
    frame_height, frame_width = image.shape[:2]

    # Calculate the bar dimensions and position
    bar_height = int(frame_height * bar_height_pct)
    bar_width = int(frame_width * bar_width_pct)
    bar_x = int(frame_width * bar_x_pct)
    bar_y = int(frame_height * bar_y_pct) + bar_height

    # Calculate progress based on elbow angle
    if elbow_angle > MAX_ANGLE:
        progress = 0
    else:
        progress = max(0, min(1, (MAX_ANGLE - elbow_angle) / (MAX_ANGLE - MIN_ANGLE)))

    # Progress bar background (gray)
    cv2.rectangle(image, (bar_x, bar_y - bar_height), (bar_x + bar_width, bar_y), (50, 50, 50), -1)

    # Progress fill (green or yellow depending on stage)
    bar_fill_height = int(progress * bar_height)
    bar_color = (0, 255, 0) if elbow_angle <= 90 else (0, 255, 255)  # Green when in down position
    cv2.rectangle(image, (bar_x, bar_y - bar_fill_height), (bar_x + bar_width, bar_y), bar_color, -1)