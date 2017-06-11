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

k=1
if runOnRasp():
	#camera.resolution = (3280, 2464)
	#camera.resolution = (2592, 1944)
	camera.resolution = (1296, 976)
	#camera.resolution = (1920, 1088)
	#camera.resolution = (640, 480)
        
while True :
	print('Image: '+str(k))
	k+=1
	
	if runOnRasp():
		video()
		image = capture(True)
	else:
		image = capture()

	image = cutBorder(image)
	#show(image, 'Without Border')

	#Contours - identify Objects
	objs_yes,objs_not = identifyObjects(image)

	#Calculate attributes for the Deep Learning
	attributes(image,objs_yes)

	#classity the objs
	#
	classify(objs_yes)

	#Draw the contours and the center of mass
	image = drawCnts(image,objs_yes,objs_not,thickness=3)#,attributes=True)  	
	
	show(image,'out')
	#cv2.waitKey(0)
	#save image
	#cv2.imwrite('imgs/teste.jpg',image)
	
	if not runOnRasp():
		break

cv2.waitKey(0)

cv2.destroyAllWindows()
