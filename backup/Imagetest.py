#!/usr/bin/python
#coding=utf-8
import Tkinter as tk
from PIL import Image, ImageTk  # pillow 模块

root=tk.Tk() # 这句必须先于 ImageTk.PhotoImage 执行。
s=r'./face/face.jpg' # jpg图片文件名 和 路径。
im=Image.open(s)
tkimg=ImageTk.PhotoImage(im) # 执行此函数之前， Tk() 必须已经实例化。
l=tk.Label(root,image=tkimg)
l.grid()
root.mainloop()
