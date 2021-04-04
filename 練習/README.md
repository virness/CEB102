===================================================
#三角星星  
for x in range(10):  
    print(""*(x)+" * "*(x+1))  
    
    
===================================================  
#九九乘法
for i in range(1,10):
    for j in range(9,0,-1):
        a=i*j
        print('%d*%d=%2d' % (i,j,a),end=' ')
    print()
    
===================================================   
#表格九九乘法表方法一
print("  |",end='')
for j in range(1,10):
    print("  ",j,end='')
print()
print("----------------------------------------")
for i in range(1,10):
    print(i,"|",end='')
    for j in range(1,10):
        print(format(i * j,"4d"),end='')
    print()
===================================================  
#表格九九乘法表方法二
for i in range(1, 10):

    if i == 1:
        print(' ', ' | ', end=' ')
        print(' '.join([' ' + str(elem) for elem in range(1, 10)]))
        print('-' * 32)

    print(str(i), ' | ', end=' ')

    for j in range(1, 10):
        print('{:>2d}'.format(i * j), end=' ')
    print()  
===================================================  
#將特定數字移動到後面
x1 = [8,1,0,2,0,1]
x2 = [1,0,0,6,0,9,3]

def funtion(a,b):
    for i in a:
        if i == 0:
            a.remove(i)
            a.append(0)
    print(a)
    for i in b:
        if i == 0:
            b.remove(i)
            b.append(0)
    print(b)
funtion(x1,x2)
===================================================  
def checkPW():  
    if(pw.get() == "1234"):  
        msg.set("密碼正確，歡迎登入！")  
    else:  
        msg.set("密碼錯誤，請修正密碼！")  

import tkinter as tk  

win = tk.Tk()  
pw = tk.StringVar()  
msg = tk.StringVar()  
label = tk.Label(win, text="請輸入密碼：")  

label.pack()  
entry = tk.Entry(win, textvariable=pw)  
entry.pack()  
button = tk.Button(win, text="登入", command=checkPW)  
button.pack()  
button = tk.Button(win, text="退出", command=checkPW)  
button.pack()  
lblmsg = tk.Label(win, fg="red", textvariable=msg)  
lblmsg.pack()  
win.mainloop()  
===================================================



