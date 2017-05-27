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

inv = False

k=1

if runOnRasp():
    camera.resolution = (1296, 972)

#for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
while True :
	print('frame: '+str(k))
	

	if runOnRasp():
		image = frame.array
	else:
		image = capture()

	#show(image,"Original", size = 300)
	#key1 = cv2.waitKey(10) & 0xFF

	image = cutBorder(image, inv = inv)
	#show(image, 'Without Border')

	#Contours - identify Objects
	objs_yes,objs_not = identifyObjects(image)

	#Calculate attributes for the Deep Learning
	attributes(image,objs_yes)

	#classity the objs
	classify(objs_yes)

	#Draw the contours and the center of mass
	image = drawCnts(image,objs_yes,objs_not)

	show(image,"Final")
	#cv2.imshow("Video", image)
	key2 = cv2.waitKey(10) & 0xFF
	key1 = key2

    # clear the stream in preparation for the next frame
	if runOnRasp():
		rawCapture.truncate(0)
	
    # if the `q` key was pressed, break from the loop
	if (key1 == ord("q")) or (key2 == ord("q") ):
		break		
	
	#save image
	#cv2.imwrite('imgs/teste.jpg',image)
	break

cv2.waitKey(0)

cv2.destroyAllWindows()
