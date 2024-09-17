import cv2
import mediapipe as mp
import numpy as np
from angles import calculate_angle
from angles import draw_live_vertical_progress_bar
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

#video feed
cap = cv2.VideoCapture(0)


#to check the size of the webcam feed to pinpoint where to place text
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Frame Width: {frame_width}")
print(f"Frame Height: {frame_height}")


#function to display the final count
def display_final_count(image, counter):
    cv2.rectangle(image, (300,300), (1600,600), (255,255,255), -1)
    cv2.putText(image, f"Push-Ups: {counter}", (500, 500),
                cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 0), 10, cv2.LINE_AA)
    cv2.imshow('Mediapipe feed', image)
    cv2.waitKey(3000)



# Wait for the user to press 's' to start push-up detection
def wait_for_start():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.putText(frame, "Press 's' to Start Push-Up Detection", (30, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)
        
        cv2.putText(frame, "Press 'l' to Open Leaderboards", (30, 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)
        
        
        cv2.imshow('MENU', frame)
        
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
    #timer values
    start_time = time.time()
    duration = 10

    #curl counter variables
    counter = 0
    stage = None
    visibility_threshold = 0.5
    
    with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
        while cap.isOpened():

            elapsed_time = time.time() - start_time  # Calculate elapsed time
            remaining_time = int(duration - elapsed_time)
            if remaining_time > 0:
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

                    if (landmarks[11].visibility > visibility_threshold and
                        landmarks[13].visibility > visibility_threshold and
                        landmarks[15].visibility > visibility_threshold and
                        landmarks[23].visibility > visibility_threshold and
                        landmarks[25].visibility > visibility_threshold):
                        

                        #get coords only if the visibility threshold is met
                        l_shoulder = [landmarks[11].x,landmarks[11].y] #left shoulder position in model
                        l_elbow = [landmarks[13].x,landmarks[13].y]
                        l_wrist = [landmarks[15].x, landmarks[15].y]
                        l_hip = [landmarks[23].x, landmarks[23].y]  #Assuming you have hip keypoints
                        l_knee = [landmarks[25].x, landmarks[25].y]

                        #the two angles required for pushups; calculate angle from angles.py
                        elbow_angle = round(calculate_angle(l_shoulder, l_elbow, l_wrist),2)
                        hip_angle = round(calculate_angle(l_shoulder, l_hip, l_knee),2)

                        draw_live_vertical_progress_bar(image, elbow_angle)

                        #visualize angles
                        cv2.putText(image, str(elbow_angle),
                                    tuple(np.multiply(l_elbow, [frame_width,frame_height]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA 
                                    )
                        
                        cv2.putText(image, str(hip_angle),
                                    tuple(np.multiply(l_hip, [frame_width,frame_height]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA 
                                    )
                        #print(landmarks) use landmarks[index] index is for the part of the body corresponding to the model

                        #counter logic
                        if elbow_angle > 150 and hip_angle > 150:
                            stage = "up"
                        if elbow_angle < 90 and hip_angle > 150 and stage == 'up':
                            stage = "down"
                            counter += 1
                    # else:
                    #     print("NOT VISIBLE")
                except:
                    pass


                #set up the rectangle box to display the counters
                cv2.rectangle(image, (0,0), (255,125), (10,117,245), -1)

                #data
                cv2.putText(image, "PUSHUPS: ", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
                cv2.putText(image, str(counter), (40,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)

                # Display countdown timer
                cv2.putText(image, f"Time Left: {remaining_time}s", (700, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4, cv2.LINE_AA)

                #render detections, drawingspec used to change colour of markings
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,66,140), thickness = 4, circle_radius = 4),
                                        mp_drawing.DrawingSpec(color=(255,255,255), thickness = 4, circle_radius = 2)
                                        )
                
            
                cv2.imshow('Mediapipe feed', image)
                

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            else:
                display_final_count(image, counter)
                break
        
        #return to menu screen
        cv2.destroyWindow('Mediapipe feed')
        wait_for_start()


#calling the functions and making it like a menu based function
wait_for_start()
