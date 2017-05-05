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

def keys(event):
    global speed
    if event.char is 'w':
        speed += 1
    elif event.char is 's':
        speed -= 1

    if speed <= 0:
        speed = 1

    print('Speed: '+str(speed))

#return the 3 angles if mouse moves
def mouse():
    root.mainloop()
    return ang1,ang2,ang3

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



#=====================================================
#===========MAIN
#=====================================================

servos = [Servo(26)]


while(1):

    angles = mouse()

    smooth(servos,angles[1])

    time.sleep(1)