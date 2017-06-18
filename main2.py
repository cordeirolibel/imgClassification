#>>>>>>>>   Image classification - OpenCV     <<<<<<<<<<#
#       Cordeiro Libel - UTFPR -  2017                  #
#-------------------------------------------------------#

#My libraries

from commons import *
from border import *
from identify import *
from servo import *
from camera import *
from classify import *
from interface import *

#=============================================
#======MAIN
#=============================================

		
#---------------------------------------------
#------SETUP
#---------------------------------------------

#=====set camera
if runOnRasp():
	#camera.resolution = (3280, 2464)
	#camera.resolution = (2592, 1944)
	camera.resolution = (1296, 976)
	#camera.resolution = (1920, 1088)
	#camera.resolution = (640, 480)

#=====set camera
#rasp pins:  6 13 19 26 gnd
#The last servo is the claw
servos = [Servo(6),Servo(19),Servo(13),Servo(26)]

start(servos)
k=1

app = App()

#---------------------------------------------
#------LOOP
#---------------------------------------------

while True :
	#-------------------------------
	#=====>> STEP 1: Take the Image
	#-------------------------------
	if runOnRasp():
		video(app)
		tic()
		image = capture(True)
	else:
		tic()
		image = capture()

	image = cutBorder(image)

	#-------------------------------
	#=====>> STEP 2: Identify and Classify Objects
	#-------------------------------

	#Contours - identify Objects
	objs_yes,objs_not = identifyObjects(image)

	#Calculate attributes for the Deep Learning
	attributes(image,objs_yes)

	#classity the objs
	classify(objs_yes)
	
	#-------------------------------
	#=====>> STEP 3: Movement
	#-------------------------------
	for obj in objs_yes:
		box_num = app.whichBox(obj.name)
		#Draw the contours and the center of mass
		img_draw = drawCnts(image,objs_yes,objs_not,thickness=3, mark = obj)#,attributes=True)  	
		show(img_draw,'out')
		cv2.waitKey(300)

		angs = regression(obj.pt)
		go(servos,box_num,angles = angs)

	#go(servos,box_num)#angles = angs)

	#-------------------------------
	#=====>> STEP 4: Print
	#-------------------------------
	print('='*50)
	print('Frame: %d\tDetected: %d\tTime: %.2fms' %(k,len(objs_yes),tic()))
	
	k+=1


	#escape
	if not runOnRasp():
		cv2.waitKey(0)
		break


cv2.destroyAllWindows()
