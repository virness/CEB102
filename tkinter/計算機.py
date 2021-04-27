#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
import math
# define font 
font = ('Verdana',22,'bold')
 
#calculator button function
def click_btn(event):
    print("btn click")
    b = event.widget
    text = b['text']
    print(text)
# back buttion
    if text=='ᐊ':
        ex = textfield.get()
        ex = ex[0:len(ex)-1]
        textfield.delete(0,END)
        textfield.insert(0,ex)
        return
# all clear
    if text=='C':
        textfield.delete(0,END)
        return
# under_root
    if text=='√':
        ex = textfield.get()
        ans = math.sqrt(float(ex))
        textfield.delete(0,END)
        textfield.insert(0,ans)
        return
# miultiply button 
    if text=='X':
        textfield.insert(END,"*")
        return
# equal button
    if text=='=':
        try:
            ex = textfield.get()
            ans = eval(ex)
            textfield.delete(0,END)
            textfield.insert(0,ans)
        except Exception as e:
            textfield.delete(0,END)
            textfield.insert(0,'Error')
        return
#to dislplay input   
    textfield.insert(END,text)
    

#create window
gui = Tk()
#window icon
# icon = PhotoImage(file = "cal.png")
# gui.iconphoto(False,icon)
#create title for window
gui.title('TkinterCLC')
#create windows size
gui.geometry('450x550')
#title hading
hading = Label(gui,text='TkinterCLC',font=('kanit',22),fg='orange')
hading.pack(side=TOP,pady=12)
 
#textfield
textfield = Entry(gui,justify=CENTER,font=('Digital-7',26),relief='solid')
textfield.pack(side=TOP,fill=X,padx=30,ipady=10)
 
#button
btnFrame = Frame(gui)
btnFrame.pack(side=TOP,pady=20)
 
#add button(0-9)
num = 1
for i in range(0,3):
    for j in range(0,3):
        btn = Button(btnFrame,text=num,font=font,width=4,height=1,relief='solid',activebackground='orange',activeforeground='#fff')
        btn.grid(row = i , column = j,padx=5,pady=5)
        num += 1
        #bind button
        btn.bind('<Button-1>',click_btn)

btn_dot = Button(btnFrame,text=".",font=font,width=4,height=1,relief='solid',activebackground='orange',activeforeground='#fff')
btn_dot.grid(row = 3, column = 0,padx=5,pady=5)
 
btn_zero = Button(btnFrame,text="0",font=font,width=4,height=1,relief='solid',activebackground='orange',activeforeground='#fff')
btn_zero.grid(row = 3, column = 1,padx=5,pady=5)
 
btn_equal = Button(btnFrame,text="=",font=font,width=4,height=1,relief='solid',activebackground='orange',activeforeground='#fff')
btn_equal.grid(row = 3, column = 2,padx=5,pady=5)
 
btn_mul = Button(btnFrame,text="X",font=font,width=4,height=1,relief='solid',activebackground='orange',activeforeground='#fff')
btn_mul.grid(row = 0, column = 3,padx=5,pady=5)
 
btn_div = Button(btnFrame,text="/",font=font,width=4,height=1,relief='solid',activebackground='orange',activeforeground='#fff')
btn_div.grid(row = 1, column = 3,padx=5,pady=5)
 
btn_sub = Button(btnFrame,text="-",font=font,width=4,height=1,relief='solid',activebackground='orange',activeforeground='#fff')
btn_sub.grid(row = 2, column = 3,padx=5,pady=5)
 
btn_add = Button(btnFrame,text="+",font=font,width=4,height=3,relief='solid',activebackground='orange',activeforeground='#fff')
btn_add.grid(row = 3, column = 3,padx=5,pady=5,rowspan=2)
 
btn_cls = Button(btnFrame,text="C",font=font,width=4,height=1,relief='solid',activebackground='red',activeforeground='#fff')
btn_cls.grid(row = 4, column = 0,padx=5,pady=5)
 
btn_back = Button(btnFrame,text="ᐊ",font=font,width=4,height=1,relief='solid',activebackground='orange',activeforeground='#fff')
btn_back.grid(row = 4, column = 1,padx=5,pady=5)
 
btn_unroot = Button(btnFrame,text="√",font=font,width=4,height=1,relief='solid',activebackground='orange',activeforeground='#fff')
btn_unroot.grid(row = 4, column = 2,padx=5,pady=5)
 
#button biniding
btn_dot.bind('<Button-1>',click_btn)
btn_zero.bind('<Button-1>',click_btn)
btn_equal.bind('<Button-1>',click_btn)
btn_mul.bind('<Button-1>',click_btn)
btn_div.bind('<Button-1>',click_btn)
btn_sub.bind('<Button-1>',click_btn)
btn_add.bind('<Button-1>',click_btn)
btn_cls.bind('<Button-1>',click_btn)
btn_back.bind('<Button-1>',click_btn)
btn_unroot.bind('<Button-1>',click_btn)
 
gui.mainloop()

