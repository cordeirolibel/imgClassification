#>>>>>>>>	Image classification - OpenCV	  <<<<<<<<<<#
#		Cordeiro Libel - UTFPR - 2017	        	    #
#-------------------------------------------------------#

#My libraries
from commons import *
from border import *
from identify import *
import random

k=1
images = []

while True:
	#open all images with name
	img = cv2.imread('imgs/forTrain/img'+str(k)+'.jpg')

	if img is None:
		break

	images.append(img)

	k+=1

#rand the array
random.shuffle(images)

#replace
k=1
for img in images:
	cv2.imwrite('imgs/forTrain/img'+str(k)+'.jpg',img)
	k+=1


print('End =)')

cv2.destroyAllWindows()
