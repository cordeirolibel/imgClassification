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

k=38
if runOnRasp():
	#camera.resolution = (3280, 2464)
	#camera.resolution = (2592, 1944)
	camera.resolution = (1296, 976)
	#camera.resolution = (1920, 1088)
	#camera.resolution = (640, 480)
        
while True :
	print('Image: '+str(k))
	
	
	if runOnRasp():
		video()
		image = capture(True)
	else:
		image = capture()
	
	show(image,'out')

	cv2.imwrite('imgs/forTrain/img'+str(k)+'.jpg',image)

	k+=1

	if not runOnRasp():
		break

cv2.waitKey(0)
cv2.destroyAllWindows()
