import cv2
import mediapipe as mp

# Define your model path
model_path = '/Users/andrews/Desktop/Takshak project/pose_landmarker_full.task'

# MediaPipe setup
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Setup drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Callback function to handle the results
def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    # Convert output_image to a numpy array for display with OpenCV
    output_image_np = output_image.numpy_view()

    # Draw pose landmarks on the image
    if result.pose_landmarks:
        for landmarks in result.pose_landmarks:
            mp_drawing.draw_landmarks(
                output_image_np,
                landmarks,
                mp.tasks.vision.PoseLandmarker.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )
    
    # Display the frame with landmarks
    cv2.imshow('Pose Detection', output_image_np)
    if cv2.waitKey(5) & 0xFF == 27:  # Exit on ESC key
        cv2.destroyAllWindows()

# Set up the PoseLandmarker with the custom model
options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result
)

# Initialize the PoseLandmarker
with PoseLandmarker.create_from_options(options) as landmarker:
    # Open video capture
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to MediaPipe Image format
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        
        # Process the frame
        landmarker.detect_async(mp_image, timestamp_ms=int(cv2.getTickCount() / cv2.getTickFrequency() * 1000))
        
    cap.release()
    cv2.destroyAllWindows()
