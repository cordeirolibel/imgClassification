#>>>>>>>>		  Servos Analysis		       <<<<<<<<<<#
#		Cordeiro Libel - UTFPR -  2017		    		 #
#--------------------------------------------------------#

from commons import *
from servo import *
from camera import *
import Tkinter as tk #for mouse read
from sklearn.svm import SVC

speed = 1

ang1 = 0
ang2 = 0
ang3 = 0
take = False
photo = False

#set speed of scroll and quit
def keys(event):
	global speed, ang1, ang2, ang3, take, photo
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
	elif event.char is ' ':
		photo = True
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

if runOnRasp():
	#camera.resolution = (3280, 2464)
	#camera.resolution = (2592, 1944)
	camera.resolution = (1296, 976)
	#camera.resolution = (1920, 1088)
	#camera.resolution = (640, 480)
		
while(1):

	claw,angles = update()
	#smooth(servos,angles)
	allMove(servos,angles)
	if claw:
		servo_hand.close()
	else:
		servo_hand.open()

	if photo:
		photo = False

		if runOnRasp():
			image = capture(True)
		else:
			image = capture()
		
		img_cut =  cutBorder(image, draw = True)
		show(img_cut,'cut')
		show(image,'original')

		pt = find_ball(img_cut)

		#escape
		if not runOnRasp():
			cv2.waitKey(0)
			break



cv2.destroyAllWindows()
