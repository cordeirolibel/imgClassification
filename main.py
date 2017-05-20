#>>>>>>>>   Image classification - OpenCV     <<<<<<<<<<#
#       Cordeiro Libel - UTFPR - April of 2016          #
#-------------------------------------------------------#

#My libraries
from commons import *
from border import *
from identify import *
from servo import *
from camera import *

#=============================================
#======MAIN
#=============================================

inv = False

k=0
camera.resolution = (1296, 972)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	print('frame: '+str(k))
	k+=1

	image = frame.array
	
	show(image,"Original", size = 300)
	cv2.waitKey(10)

	image = cutBorder(image, inv = inv)
	#show(image, 'Without Border')

	#Contours - identify Objects
	objs_yes,objs_not = identifyObjects(image)

	#Calculate attributes for the Deep Learning
	attributes(image,objs_yes)

	#Draw the contours and the center of mass
	image = drawCnts(image,objs_yes,objs_not, attributes = True)

	show(image,"Final")
	#cv2.imshow("Video", image)
	key = cv2.waitKey(10) & 0xFF
	
    # clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	
    # if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
		
	#save image
	#cv2.imwrite('imgs/teste.jpg',image)
	#break

#cv2.waitKey(0)

cv2.destroyAllWindows()
