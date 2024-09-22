import tkinter as tk
from tkinter import ttk
import os
import cv2

#now this file will handle all the leaderboards stuff
#and can be imported to main.py to be used



def input_details():

    name,text='',''

    def get_text():
        nonlocal name,text
        name=text_field.get()
        text=var.get()
        root.destroy()

    #Creating the window for GUI and naming it and specifying its size     
    root = tk.Tk()
    root.title("PLAYER INFO")
    root.geometry("600x600")

    #Specifying a label field to give directions to the user
    label=tk.Label(root,text="Enter Name")
    label.pack(pady=5)

    #Specifying a text field for the user to enter name into
    text_field = tk.Entry(root,width=40)
    text_field.pack(pady=5)

    #Specifying the radio buttons for male and female the variable var stores the value of currently selected radio button
    var=tk.StringVar(value="Male")
    radio1=ttk.Radiobutton(root,text="Male",value="Male",variable=var)
    radio2=ttk.Radiobutton(root,text="Female",value="Female",variable=var)

    #This pack function is used to put the widgets into the window
    radio1.pack()
    radio2.pack()

    #The button which when pressed starts a function which extracts the value from text field and var
    button = tk.Button(root,text="Submit",command=get_text)
    button.pack(pady=5)  

    #Display the window
    root.mainloop()
    
    print(name,text)
    return [name,text]  

def write_into_file(val):

    """Players listed sorted by the number of pushups
       Creating two files because a new player can't be inserted in the lines in between
       So reading from one file and writing to another is done"""
    
    #Opening files
    file2=open("D:/file2.txt","w")
    file1=open("D:/file1.txt","r")
    contents=file1.readlines()

    #flag variable for knowing whether the current player was inserted in file or not
    flag1=0
    
    #try catch block for avoiding accidental skipping close() function
    try:

        for content in contents:

            #finding pipe characters
            first_pipe=content.find("|")
            second_pipe=content.rfind("|")

            #extracting name and pushup count (name is to overwrite duplicates and pushup counts is to put the player at the position)
            p_name=content[:first_pipe]
            p_count=int(content[second_pipe+1:-1])

            #Checking for name duplication
            if not flag1 and p_name==val[0]:
                if int(val[2]>=p_count):
                    flag1=1
                    file2.write(f"{val[0]}|{val[1]}|{val[2]}\n")
                    continue

            #Checking if the number of pushup of the current player is greater than currently read line
            if not flag1 and int(val[2])>=p_count:
                file2.write(f"{val[0]}|{val[1]}|{val[2]}\n")
                flag1=1

            #Writing the currently read line
            file2.write(content)

        #If the number of pushup of the current player is least of them all
        if not flag1:
            file2.write(f"{val[0]}|{val[1]}|{val[2]}\n")                 
    
    finally:

        #Closing files
        file2.close()
        file1.close()

        #Deleting the first file and renaming the second file to the name of the first file
        os.remove("D:/file1.txt")
        os.rename("D:/file2.txt","D:/file1.txt")

def read_from_file():

    #opening and reading from file
    file1=open("D:/file1.txt",'r')
    contents=file1.readlines()

    #Lists to store the male top2 and female top2
    mlst,flst=[],[]

    #Loop iterating through each line in contents , One line contains the details of a particular player
    for content in contents:

        #finding the indices of first and second pipe because the gender parameter lies between those two pipe characters
        first_pipe=content.find("|")
        second_pipe=content.find("|",first_pipe+1,-1)
        from_file=content[first_pipe+1:second_pipe]

        #Classifying male and female and putting them into their separate lists
        if from_file=="Male" :
            if len(mlst)<11:
                mlst.append(content)
        else :
            if len(flst)<11:
                flst.append(content) 

        #Breaking from looping through the read lines when top two of both male and female players are obtained
        if len(mlst)==10 and len(flst)==10:
            break

    return mlst+flst
    file1.close()

    




        

