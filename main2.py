import cv2
import mediapipe as mp
import numpy as np
from angles import calculate_angle
from angles import draw_live_vertical_progress_bar
import time
from positioning import draw_rectangle, put_text
from leaderboard import input_details,write_into_file,read_from_file,out_list

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


#video feed
cap = cv2.VideoCapture(0)


#to check the size of the webcam feed to pinpoint where to place text
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Frame Width: {frame_width}")
print(f"Frame Height: {frame_height}")

flagm=0
lst=[]

#function to display the final count
def display_final_count(image, counter):
    
    draw_rectangle(image, 0.2, 0.3, 0.75, 0.6, (255,255,255), -1)
    put_text(image, f"Push-Ups: {counter}", 0.25, 0.5, 0.003, (0,0,0), 0.010)
    cv2.imshow('Mediapipe feed', image)
    cv2.waitKey(3000)
    
   #flagm variable used to know whether a new player arrived
    global flagm
    if flagm:
        filem=open("file1.txt","w")
        lst.append(str(counter))
        write_into_file(lst)



# Wait for the user to press 's' to start push-up detection
def wait_for_start():
    #finding the screen size for full screen shinanigans
    #cv2.namedWindow('MENU', cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('MENU', 1440, 932)

    global lst,flagm
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        put_text(frame, "Press 'd' Enter player information", 0.15, 0.15, 0.001, (0,0,0), 0.003)

        put_text(frame, "Press 's' to Start Push-Up Detection", 0.15, 0.30, 0.001, (0,0,0), 0.003)

        put_text(frame, "Press 'l' to Start Open Leaderboards", 0.15, 0.45, 0.001, (0,0,0), 0.003)
        
        put_text(frame, "Press 'q' to QUIT", 0.15, 0.60, 0.001, (0,0,0), 0.003)
        
        cv2.imshow('MENU', frame)


        key = cv2.waitKey(10) & 0xFF

        if key == ord('s'):  # If 's' is pressed
            flagm=0
            start_pushup_detection()
            break

        elif key == ord('d'):

            #Pressing d indicates the arrival of a new player so setting flagm and then inputting player details
            flagm=1
            lst=input_details()
            start_pushup_detection()

        elif key == ord('l'):

            #Everything done here was lucky i am still unaware of how frame cap etc work

            cv2.namedWindow('Leaderboard', cv2.WINDOW_NORMAL)
            mlst,flst=read_from_file()

            while cap.isOpened():

                ret,frame=cap.read()

                if not ret:
                    break

                draw_rectangle(frame,0.01,0.01,0.45,0.5,(0,0,0),-1)
                draw_rectangle(frame,0.50,0.01,0.95,0.5,(0,0,0),-1)

                cv2.putText(frame,"MALE",(40,20), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1,cv2.LINE_AA)

                for i in range(len(mlst)):

                    clst=out_list(mlst[i])
                    cv2.putText(frame,"#"f"{i+1}", (20,40+15*i ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
                    cv2.putText(frame,f"{clst[0]}", (50,40+15*i ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
                    cv2.putText(frame,f"{clst[1]}", (230,40+15*i ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

                cv2.putText(frame,"FEMALE",(400,20), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1,cv2.LINE_AA)

                i+=1

                for j in range(len(flst)):

                    clst=out_list(flst[j])
                    cv2.putText(frame,"#"f"{j+1}", (350,40+15*j ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA) 
                    cv2.putText(frame,f"{clst[0]}", (380,40+15*j ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA) 
                    cv2.putText(frame,f"{clst[1]}", (580,40+15*j), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)             
               
               
                cv2.imshow('Leaderboard',frame)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            cv2.destroyWindow('Leaderboard')
            
        elif key == ord('q'):  # If 'q' is pressed, exit the program
            cap.release()
            cv2.destroyAllWindows()
            exit()

#set up mediapipe instance and start detection
def start_pushup_detection():
    cv2.namedWindow('Mediapipe feed', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Mediapipe feed', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    #timer values
    start_time = time.time()
    duration = 40

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
                    else:
                        put_text(image, "UNABLE TO DETECT", 0.15, 0.9, 0.003, (0,0,255), 0.006)
                        
                except:
                    pass


                #set up the rectangle box to display the counters
                draw_rectangle(image, 0, 0, 0.14, 0.12, (10,117,245), -1)


                #data pushup counter box
                put_text(image, "PUSHUPS:", 0.02, 0.03, 0.001, (0,0,0), 0.003)
                put_text(image, str(counter), 0.025, 0.1, 0.002, (255,255,255), 0.003)

                # Display countdown timer
                put_text(image, f"Time Left: {remaining_time}s", 0.4, 0.1, 0.002, (0,0,0), 0.004)

                #defining custom connections to only draw the required connections and ignore others
                custom_connections = [
                (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
                (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST),
                (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP),
                (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE)
                ]

                #render detections, drawingspec used to change colour of markings
                mp_drawing.draw_landmarks(image, results.pose_landmarks, custom_connections,
                                        mp_drawing.DrawingSpec(color=(245,66,140), thickness = 4, circle_radius = 4),
                                        mp_drawing.DrawingSpec(color=(255,255,255), thickness = 4, circle_radius = 2)
                                        )
                
            
                cv2.imshow('Mediapipe feed', image)
                

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    display_final_count(image, counter)
                    break
            else:
                display_final_count(image, counter)
                break
        
        #return to menu screen
        cv2.destroyWindow('Mediapipe feed')
        wait_for_start()


#calling the functions and making it like a menu based function
wait_for_start()
