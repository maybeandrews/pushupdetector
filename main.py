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

#set up mediapipe instance
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

            #get coords
            l_shoulder = [landmarks[11].x,landmarks[11].y] #left shoulder position in model
            l_elbow = [landmarks[13].x,landmarks[13].y]
            l_wrist = [landmarks[15].x, landmarks[15].y]
            l_hip = [landmarks[23].x, landmarks[23].y]  # Assuming you have hip keypoints

            #the two angles required for pushups; calculate angle from angles.py
            elbow_angle = round(calculate_angle(l_shoulder, l_elbow, l_wrist),2) #check if you need .x and .y here idk 
            shoulder_angle = round(calculate_angle(l_elbow, l_shoulder, l_hip),2)

            #visualize angles
            cv2.putText(image, str(elbow_angle),
                        tuple(np.multiply(l_elbow, [1920,1080]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA 
                        )
            
            cv2.putText(image, str(shoulder_angle),
                        tuple(np.multiply(l_shoulder, [1920,1080]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA 
                        )
            
            #print(landmarks)    use landmarks[index] index is for the part of the body corresponding to the model
        except:
            pass

        #render detections, drawingspec used to change colour of markings
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245,117,66), thickness = 2, circle_radius = 2),
                                  mp_drawing.DrawingSpec(color=(245,66,230), thickness = 4, circle_radius = 2)
                                  )
        
    
        cv2.imshow('Mediapipe feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
