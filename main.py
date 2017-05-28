#>>>>>>>>   Image classification - OpenCV     <<<<<<<<<<#
#       Cordeiro Libel - UTFPR - April of 2016          #
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
	#camera.resolution = (1296, 972)
	camera.resolution = (1920, 1088)
	#camera.resolution = (640, 480)
        
while True :
	print('Image: '+str(k))

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
	classify(objs_yes)

	#Draw the contours and the center of mass
	image = drawCnts(image,objs_yes,objs_not)  	
	
	show(image,'out')
	cv2.waitKey(0)
	#save image
	#cv2.imwrite('imgs/teste.jpg',image)
	
	if not runOnRasp():
		break

cv2.waitKey(0)

cv2.destroyAllWindows()
