import tkinter
import tkinter.messagebox
import customtkinter
import tkinter as tk
import cv2
from PIL import ImageTk, Image
import os
import time
import glob
import datetime
import torch

#Title for GUI window
gui = customtkinter.CTk()
gui.title("Tamarind Damage Type Identification")
gui.geometry(f"{640}x{480}")
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
customtkinter.set_widget_scaling(0.8)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#cap = cv2.VideoCapture(0)
cap.set(3, 352)
cap.set(4, 288)
IMAGES_PATH_CAPTURED = os.path.join('Captured')
label = 'Image'
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

#Functions
def captureButton_command():
    textBox.configure(state="normal")
    textBox.insert("2.0","\nImage saved to\nCaptured")
    textBox.configure(state="disabled")
    ret, frame = cap.read()
    cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
    date = datetime.datetime.now()
    imgname = os.path.join(IMAGES_PATH_CAPTURED, label+'_%s%s%sT%s%s%s'%(date.year, date.month, date.day, date.hour, date.minute, date.second)+'.jpg')
    cv2.imwrite(imgname, frame)
    time.sleep(1)
    print("Image saved to {}".format(IMAGES_PATH_CAPTURED))
    
def exitButton_command():
    gui.destroy()
    
def video_stream():
    ret, frame = cap.read()
    cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    cameraLabel.imgtk = imgtk
    cameraLabel.configure(image=imgtk)
    cameraLabel.after(1, video_stream)
    
def last_img():
    ####GET LATEST IMAGE FROM CAPTURED FOLDER#######
    ts = 0
    logic = 0
    found = None
    for file_name in glob.glob('Captured/*.jpg'):
        fts = os.path.getmtime(file_name)
        if fts > ts:
            ts = fts
            found = file_name
            logic = 1
    if logic == 1:
        first = Image.open(found)
        second = first.resize((160,145), Image.Resampling.LANCZOS)
        third = ImageTk.PhotoImage(second)
        captureLabel.third = third  # keep a reference so it's not garbage collected
        captureLabel['image'] = third
        #get latest image from captured folder then use model to save to detected
        img = first
        results = model(img)
        results.save(save_dir='Detected', exist_ok = True)
        logic = 0
    #####GET LATEST IMAGE FROM DETECTED FOLDER##########
    ts2 = 0
    logic2 = 0
    found2 = None
    for file_name in glob.glob('Detected/*.jpg'):
        fts2 = os.path.getmtime(file_name)
        if fts2 > ts2:
            ts2 = fts2
            found2 = file_name
            logic2 = 1
    if logic2 == 1:
        first2 = Image.open(found2)
        second2 = first2.resize((160,145), Image.Resampling.LANCZOS)
        third2 = ImageTk.PhotoImage(second2)
        detectedLabel.third = third2  # keep a reference so it's not garbage collected
        detectedLabel['image'] = third2
        
        logic2 = 0
        
      
def c_and_n():
    captureButton_command()
    last_img()
    
def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)
    
def alwaysTopLevel():
    gui.attributes('-topmost','true')

#MAIN GUI
#Configure Grid Layout(5x6)
gui.grid_columnconfigure((1, 3, 5), weight=1)
gui.grid_rowconfigure((0, 1, 2), weight=1)

#Sidebar frame with widgets
sidebar_frame = customtkinter.CTkFrame(gui, width=140)
sidebar_frame.grid(row=0, column=0, rowspan = 4, sticky="nsew")
sidebar_frame.grid_rowconfigure(4, weight=1)
logo_label = customtkinter.CTkLabel(sidebar_frame, text="YOLOv5", font=customtkinter.CTkFont(size=20, weight="bold"))
logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

#Capture Button
captureButton = customtkinter.CTkButton(sidebar_frame, command=c_and_n, text="Capture")
captureButton.grid(row=1, column=0, padx=20, pady=10)

#Made by label
namelabel = customtkinter.CTkLabel(sidebar_frame, text="Made by:\nArevalo\nNerpio", anchor="w")
namelabel.grid(row=4, column=0, padx=20, pady=(10, 0))
namelabel.place(x=70,y=340)

#Appearance mode label
appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["Light", "Dark"],
                                                               command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

#Mapua logo
mapuaLabel = tk.Label(gui)
open_photo_mapua = Image.open('mapua_logo.png')
resized_photo_mapua = open_photo_mapua.resize((120,60), Image.Resampling.LANCZOS)
logo_mapua = ImageTk.PhotoImage(resized_photo_mapua)
mapuaLabel.logo_mapua = logo_mapua  # keep a reference so it's not garbage collected
mapuaLabel['image'] = logo_mapua
mapuaLabel.configure(background='#2B2B2B')
mapuaLabel.place(x=10,y=340)

###INSERT CODE HERE FOR OUTPUT IMAGES
#Captured
captureFrame = customtkinter.CTkFrame(gui, width=300)
captureFrame.grid(row=0, column=1, columnspan = 2, padx=10 , pady=10, sticky="nsew")
captureLabel = tk.Label(gui)
captureLabel["borderwidth"] = "1px"
captureLabel["relief"] = "solid"
captureLabel["text"] = "No image found"
captureLabel.place(x=160,y=15,width=160,height=145)

#Detected
detectedFrame = customtkinter.CTkFrame(gui, width = 300)
detectedFrame.grid(row=0, column=3, columnspan = 2, padx=10 , pady=10, sticky="nsew")
detectedLabel = tk.Label(gui)
detectedLabel["borderwidth"] = "1px"
detectedLabel["relief"] = "solid"
detectedLabel["text"] = "No image found"
detectedLabel.place(x=355,y=15,width=160,height=145)

#Camera
cameraFrame = customtkinter.CTkFrame(gui, width =350, height=385)
cameraFrame.grid(row=1, column=1, columnspan =4, rowspan =3, padx=10, pady=1, sticky="nsew")
cameraLabel = tk.Label(gui)
cameraLabel["borderwidth"] = "1px"
cameraLabel["relief"] = "solid"
cameraLabel["text"] = "No image found"
cameraLabel.place(x=160,y=185, width=352, height=288)

#Text
textFrame = customtkinter.CTkFrame(gui, width=210)
textFrame.grid(row=0, column=5, rowspan = 3, padx=1, pady=10, sticky="nsew")
textBox = customtkinter.CTkTextbox(master=textFrame, width=117, height=520)
textBox.insert("0.0", "Logs\n\n")
textBox.place(x=8,y=7)
textBox.configure(state="disabled")

#Exit Button
exitButton = customtkinter.CTkButton(master=gui, 
                                            text='Exit', 
                                            fg_color="transparent", 
                                            border_width=2, 
                                            text_color=("gray10", "#DCE4EE"), 
                                            height=10,
                                            command=exitButton_command)
exitButton.grid(row=3, column=5, padx=10, pady=10, sticky = "nsew")  

#set default values
appearance_mode_optionemenu.set("Dark")
            
#end
video_stream()
last_img()
alwaysTopLevel()
gui.mainloop()
