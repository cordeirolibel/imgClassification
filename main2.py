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
servos = [Servo(26),Servo(19),Servo(13),Servo(6)]

k=1

#---------------------------------------------
#------LOOP
#---------------------------------------------
while True :
	#-------------------------------
	#=====>> STEP 1: Take the Image
	#-------------------------------
	if runOnRasp():
		video()
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

	#Draw the contours and the center of mass
	image = drawCnts(image,objs_yes,objs_not,thickness=3,attributes=True)  	
	
	show(image,'out')

	#-------------------------------
	#=====>> STEP 3: Movement
	#-------------------------------
	take(servos)

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
