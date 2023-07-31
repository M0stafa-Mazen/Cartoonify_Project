# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 23:25:29 2022

@author: Mostafa_Mazen
"""

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

def set_camera():
    global cap
  
    cap = cv2.VideoCapture(0)
    cap.set(3, 300)
    cap.set(4, 350)
    cap.set(10, 100) #brightness
    opne_camera()
   

def opne_camera():
    
    img = cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    imgn = filterapp(img)
    imgn = Image.fromarray(imgn)
    imgtk = ImageTk.PhotoImage(image = imgn)
    vlabel.imgtk = imgtk
    vlabel.configure(image=imgtk)
    vlabel.after(10, opne_camera)
    
# def color_quantization(image,k):
    
#     img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     im_pil = Image.fromarray(np.uint8(img))
#     im_pil = im_pil.quantize(k, None, 0, None)
#     return cv2.cvtColor(np.array(im_pil.convert("RGB")), cv2.COLOR_RGB2BGR) 

def color_quantization(img, k):
  # reshape the image to a 2D array of pixels and 3 color values (RGB)
  # convert to float
  data=np.float32(img).reshape((-1, 3))
  # define stopping criteria
  criteria=(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,20,0.001)

  ret, label, center=cv2.kmeans(data, k , None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
  # convert back to 8 bit values
  center = np.uint8(center)
  # flatten the labels array
  # convert all pixels to the color of the centroids
  result = center[label.flatten()]
  result = result.reshape(img.shape)
  return result

def edge_mask(img, line_size, blur_value):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  gray_blur = cv2.medianBlur(gray, blur_value)
  edges = cv2.adaptiveThreshold(gray_blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, line_size, blur_value)
  return edges


def filterapp(img):
    line_size=5
    blur_value=7
    edges=edge_mask(img, line_size,blur_value)
    
    total_color = 9
    img = color_quantization(img, total_color)
    blurred = cv2.bilateralFilter(img, d=5, sigmaColor=200, sigmaSpace=200,)
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
    return cartoon

def cartoonf(): 
    global converted ,imgn ,cartoon
    cartoon = filterapp(imf)
    cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    imgn = Image.fromarray(cartoon)
    vlabel.imgns = ImageTk.PhotoImage(imgn)
    vlabel.configure(image = vlabel.imgns)
    # vlabel=tk.Label(root,text = "",image = root.imgns)#image=root.photo
    # vlabel.grid(row=3,column=2) 
    converted = True

def checkg():
    if uploaded != True:
        print("Need To Upload The Image.")
        vlabel.text1 = "Upload The Image First"
        vlabel.configure(text = vlabel.text1)
        # vlabel=tk.Label(root,text = "Upload The Image First")#image=root.photo
        # vlabel.grid(row=3,column=2)
    else:
        cartoonf()
        print("Image Was Converted.")
        
    
def resize_max(image,max_dimension):
    image_height,image_width,channels = image.shape

    if image_height < max_dimension and image_width < max_dimension: ##Only resize larger images
        return image
    if image_height > image_width:
        final_height = max_dimension
        final_width = int(final_height *  image_width / image_height )
    else:
        if not image_width == 0:
            final_width = max_dimension
            final_height = int(final_width *  image_height / image_width)
        else:
            final_height = 0
            final_width = 0
    return cv2.resize(image,(int(final_width),int(final_height)))
    
    
def upload_file(): 
    global imf , fileTypes ,fileName , uploaded ,converted,h,w
    uploaded = True
    converted = False
    try:
     cap
    except NameError:
        print("camera still not opend")
    else:
        cap.release()
    fileTypes = [('PNG Files', '*.png'),('JPG file','.jpg'),('JPEG file','.jpeg'),('All Files','.')]
    fileName = filedialog.askopenfilename(title='Select Image File',filetypes=fileTypes)
    imf = cv2.imread(fileName)
    h,w,c = imf.shape
    imf = resize_max(imf,400)
    im = cv2.cvtColor(imf, cv2.COLOR_BGR2RGB)
    print(fileName)
    im = Image.fromarray(im)
    vlabel.img = ImageTk.PhotoImage(im)
    vlabel.configure(image = vlabel.img)
    # vlabel=tk.Label(root,image = img)#image=root.photo
    # vlabel.grid(row=3,column=2)

def savefile():
    if uploaded != True:
        print("Need To Upload The Image.")
        vlabel.text1 = "Upload The Image First"
        vlabel.configure(text = vlabel.text1)
        # vlabel=tk.Label(root,text = "Upload The Image First")#image=root.photo
        # vlabel.grid(row=3,column=2)
    elif converted == True:
        print("Image Is Saved.")
        filename = filedialog.asksaveasfile(mode='w',filetypes = [('JPG file','.jpg')], defaultextension=".jpg")
        if not filename:
            return
        cartoon1 = cv2.resize(cartoon,(w,h))
        imgn = Image.fromarray(cartoon1)
        imgn.save(filename)
    else:
        print("Image Is Not Converted")
        vlabel.text1 = "Image Is Not Converted"
        vlabel.configure(text = vlabel.text1,image = "")
        # vlabel=tk.Label(root,text = "Image Is Not Converted")#image=root.photo
        # vlabel.grid(row=3,column=2)
        
def exitf():
    try:
     cap
    except NameError:
        root.destroy()
    else:
        cap.release()
        root.destroy()
    
###################################################
#################GUI Section#######################
###################################################

uploaded = False
converted = False
root = tk.Tk()
#root.geometry("500x550")
root.title("Cartoon App")
root['background']='#BDE0FE'
font1=('times', 18, 'bold')
#root.iconbitmap(r'C:\Users\Mostafa_Mazen\Desktop\project\icons\i4.ico')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

l1 = tk.Label(root,text="*Convert your image*",bg='#BDE0FE',fg='#905AAF',width=30,font=font1) 
l1.grid(row=1, column=1,sticky="NESW")

vlabel=tk.Label(root,text = "Add You Image here!",bg = '#BDE0FE',fg='#905AAF',font = "Times 12 italic bold")
vlabel.grid(row=2,column=1,sticky="NESW")

b1 = tk.Button(root, text='Upload File',bg = '#A2D2FF',fg='#905AAF',width=20,command = upload_file)
b1.grid(row=2,column=0,padx=5,pady=5,sticky="NEW") 

b2 = tk.Button(root, text="Open cam",bg='#A2D2FF',fg='#905AAF',width=15, command = set_camera)
b2.grid(row=2,column=2,padx=5,pady=5,sticky="NEW")

b3=tk.Button(root,text="Convert",bg = '#A2D2FF',fg='#905AAF',command = checkg)
b3.grid(row=3,column=0,padx=5,pady=5,sticky="NEW")#,sticky = tk.EW,padx=5,pady=5

b4 = tk.Button(root, text="Save as",bg = '#A2D2FF',fg='#905AAF', command = savefile)
b4.grid(row=3,column=2,padx=5,pady=5,sticky="NEW")

b5 = tk.Button(root,text="Exit",bg = '#A2D2FF',fg = 'red',command = exitf)
b5.grid(row=4,column=1,padx=5,pady=5,sticky="NESW")#,sticky = tk.EW,padx=5,pady=5

root.mainloop()

