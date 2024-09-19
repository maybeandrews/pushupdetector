import tkinter as tk
from tkinter import ttk
import os
import cv2

#now this file will handle all the leaderboards stuff
#and can be imported to main.py to be used



def input_details():
    name,text='',''
    def get_text():
        global name,text
        name=text_field.get()
        text=var.get()
        root.destroy()
        
    root = tk.Tk()
    root.title("PLAYER INFO")

    root.geometry("600x600")

    label=tk.Label(root,text="Enter Name")
    label.pack(pady=5)

    text_field = tk.Entry(root,width=40)
    text_field.pack(pady=5)

    var=tk.StringVar(value="Male")
    radio1=ttk.Radiobutton(root,text="Male",value="Male",variable=var)
    radio2=ttk.Radiobutton(root,text="Female",value="Female",variable=var)

    radio1.pack()
    radio2.pack()

    button = tk.Button(root,text="Submit",command=get_text)
    button.pack(pady=5)  

    root.mainloop()
    return name,text  

def write_into_file(val):
    file2=open("D:/file2.txt","w")
    file1=open("D:/file1.txt","r")
    count=-1
    track=0
    flag1=0
    lines=file1.readlines()
    try:
        for content in lines:
            for i in content:
                count+=1
                if i=="|":
                    track+=1
                    if track==2:
                        print(int(content[count+1:-1]))
                        from_file=int(content[count+1:-1])
                        if int(val[2])>=from_file:
                            file2.write(f"{val[0]}|{val[1]}|{val[2]}\n")
                            flag1=1
                            break
            file2.write(content)
        if not flag1:
            file2.write(f"{val[0]}|{val[1]}|{val[2]}\n")
    finally:
        file2.close()
        file1.close()
        os.remove("D:/file1.txt")
        os.rename("D:/file2.txt","D:/file1.txt")

def read_from_file():
    file1=open('file1.txt','r')
    mnumber,fnumber=0,0
    mlst,flst=[],[]
    for content in file1:
        for i in content:
            count+=1
            if i=="|":
                track+=1
                if track==1:
                    start=count
                if track==2:
                    from_file=int(str[start:count])
                    if from_file=="Male" :
                        mnumber+=1
                        if mnumber<3:
                            mlst.append(content)
                    else :
                        fnumber+=1
                        if fnumber<3:
                            flst.append(content)
    return mlst+flst
    file1.close()





        

