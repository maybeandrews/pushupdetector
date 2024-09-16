import cv2
import mediapipe as mp
import numpy as np
from angles import calculate_angle


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

#video feed
cap = cv2.VideoCapture(0)


#to check the size of the webcam feed to pinpoint where to place text
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Frame Width: {frame_width}")
print(f"Frame Height: {frame_height}")

# Wait for the user to press 's' to start push-up detection
def wait_for_start():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.putText(frame, "Press 's' to Start Push-Up Detection", (30, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)
        
        cv2.imshow('Push-Up Detection', frame)
        
        key = cv2.waitKey(10) & 0xFF
        if key == ord('s'):  # If 's' is pressed
            start_pushup_detection()
            break
        elif key == ord('q'):  # If 'q' is pressed, exit the program
            cap.release()
            cv2.destroyAllWindows()
            exit()

#set up mediapipe instance and start detection
def start_pushup_detection():
    #curl counter variables
    counter = 0
    stage = None
    visibility_threshold = 0.9
    with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            #detect stuff and render, recolour image required for mediapipe conditions
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            #recolouring back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)




            #extract landmarks for joints
            #I made a function here to return values to angles.py but we don't need it so I changed it back
            try:
                landmarks = results.pose_landmarks.landmark

                if (landmarks[11].visibiilty > visibility_threshold and
                    landmarks[13].visibiilty > visibility_threshold and
                    landmarks[15].visibiilty > visibility_threshold and
                    landmarks[23].visibiilty > visibility_threshold and
                    landmarks[25].visibiilty > visibility_threshold):
                    

                    #get coords only if the visibility threshold is met
                    l_shoulder = [landmarks[11].x,landmarks[11].y] #left shoulder position in model
                    l_elbow = [landmarks[13].x,landmarks[13].y]
                    l_wrist = [landmarks[15].x, landmarks[15].y]
                    l_hip = [landmarks[23].x, landmarks[23].y]  #Assuming you have hip keypoints
                    l_knee = [landmarks[25].x, landmarks[25].y]

                    #the two angles required for pushups; calculate angle from angles.py
                    elbow_angle = round(calculate_angle(l_shoulder, l_elbow, l_wrist),2)
                    hip_angle = round(calculate_angle(l_shoulder, l_hip, l_knee),2)

                    #visualize angles
                    cv2.putText(image, str(elbow_angle),
                                tuple(np.multiply(l_elbow, [1920,1080]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA 
                                )
                    
                    cv2.putText(image, str(hip_angle),
                                tuple(np.multiply(l_hip, [1920,1080]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA 
                                )
                    #print(landmarks) use landmarks[index] index is for the part of the body corresponding to the model

                    #counter logic
                    if elbow_angle > 160 and hip_angle > 160:
                        stage = "up"
                    if elbow_angle < 90 and hip_angle > 160 and stage == 'up':
                        stage = "down"
                        counter += 1
            except:
                pass


            #set up the rectangle box to display the counters
            cv2.rectangle(image, (0,0), (255,125), (10,117,245), -1)

            #data
            cv2.putText(image, "PUSHUPS: ", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
            cv2.putText(image, str(counter), (40,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)


            #render detections, drawingspec used to change colour of markings
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,66,140), thickness = 4, circle_radius = 4),
                                    mp_drawing.DrawingSpec(color=(255,255,255), thickness = 4, circle_radius = 2)
                                    )
            
        
            cv2.imshow('Mediapipe feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


#calling the functions and making it like a menu based program
wait_for_start()