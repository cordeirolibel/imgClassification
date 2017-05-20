#>>>>>>>>          Camera Functions           <<<<<<<<<<#
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

#set ang1 with mouse wheel
def mouse_wheel(event):
    global ang1

    # respond to Linux or Windows wheel event
    if event.num == 5 or event.delta == -120:
        ang1 -= speed
    if event.num == 4 or event.delta == 120:
        ang1 += speed

    if ang1<-90:
        ang1 =-90
    elif ang1>90:
        ang1 = 90

    #print
    label['text'] = [ang1,ang2,ang3]

    root.quit() 

#set ang2 e ang3 with mouse movement
def motion(event):
    global ang2, ang3

    x, y = event.x, event.y
    
    ang2 = toInt(x/2-90)
    ang3 = toInt(y/2-90)

    #print
    label['text'] = [ang1,ang2,ang3]

    root.quit() 

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
   

#set 'take' with click button
def click(event):
    global take
    if event.type is '4':
        print('Close')
        take = True
    elif event.type is '5':
        print('Open')
        take = False
        
    root.quit() 
    

#return the 3 angles if mouse moves
def mouse():
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

#========== Mouse move

root.bind('<Motion>', motion)

#========== Mouse Wheel

# with Windows OS
root.bind("<MouseWheel>", mouse_wheel)
# with Linux OS
root.bind("<Button-4>", mouse_wheel)
root.bind("<Button-5>", mouse_wheel)

#========== Keys

root.bind('<Key>', keys)

#========== Keys

root.bind('<ButtonPress-1>', click)
root.bind('<ButtonRelease-1>', click)     






#=====================================================
#===========MAIN
#=====================================================
# pins 6 13 19 26 gnd
servos = [Servo(26),Servo(19),Servo(13)]

servo_hand = Servo(6)

while(1):

    claw,angles = mouse()
    smooth(servos,angles)

    if claw:
        servo_hand.close()
    else:
        servo_hand.open()




