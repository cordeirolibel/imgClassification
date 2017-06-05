#>>>>>>>>       Servos by keyboard            <<<<<<<<<<#
#        Cordeiro Libel - UTFPR - may of 2017           #
#-------------------------------------------------------#

from commons import *
from servo import *
import Tkinter as tk #for mouse read

speed = 1

ang1 = 0
ang2 = 0
ang3 = 0
take = False

#set speed of scroll and quit
def keys(event):
    global speed, ang1, ang2, ang3, take
    if event.char is 'r':
        speed += 1
    elif event.char is 'f':
        speed -= 1
    elif event.char is 'w':
        ang1 += speed
    elif event.char is 's':
        ang1 -= speed
    elif event.char is 'a':
        ang2 += speed
    elif event.char is 'd':
        ang2 -= speed
    elif event.char is 'q':
        ang3 += speed
    elif event.char is 'e':
        ang3 -= speed 
    elif event.char is '1':
        take = True
    elif event.char is '2':
        take = False
    elif event.char is 'k':
        root.quit() 
        exit()
        
    def setAng(ang):
        if ang>90:
            return 90
        elif ang<-90:
            return -90
        return ang
    ang1 = setAng(ang1)
    ang2 = setAng(ang2)
    ang3 = setAng(ang3)
        
    
    if speed <= 0:
        speed = 1
    
    print('ang1:'+str(ang1)+' ang2:'+str(ang2)+' ang3:'+str(ang3)+' speed:'+str(speed)+' Open'*take+' Close'*(not take))
    root.quit() 
   

#return the 3 angles and take
def update():
    root.mainloop()
    return take, [ang1,ang2,ang3]


def on_closing():
    root.quit() 
    exit()

#========== Screen Config

root = tk.Tk()
root.geometry("360x360")
root.protocol("WM_DELETE_WINDOW", on_closing)
label = tk.Label(root, font=('courier', 18, 'bold'), width=20)
label.pack(padx=40, pady=40)

#========== Keys

root.bind('<Key>', keys)


#=====================================================
#===========MAIN
#=====================================================

#rasp pins:  6 13 19 26 gnd
servos = [Servo(26),Servo(19),Servo(13)]
servo_hand = Servo(6)

start(servos+[servo_hand])

while(1):

    claw,angles = update()
    #smooth(servos,angles)
    allMove(servos,angles)
    if claw:
        servo_hand.close()
    else:
        servo_hand.open()




