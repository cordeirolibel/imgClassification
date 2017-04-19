#>>>>>>>>	Image classification - OpenCV	  <<<<<<<<<<#
#		Cordeiro Libel - UTFPR - April of 2016		    #
#-------------------------------------------------------#

#My libraries
from commons import *
from border import *
from identify import *

#=============================================
#======SAVE IMAGE OF EACH OBJECT
#=============================================

k=1
while True:
	#open all images with name
	image = cv2.imread('imgs/objs'+str(k)+'.jpg')
	
	if image is None:
		break

	image = cutBorder(image)
	
	#Contours - identify Objects
	objs_yes,_ = identifyObjects(image)

	#find and save the minimal image of each object
	imagesSave(image,objs_yes)

	i=1
	for obj in objs_yes:
		cv2.imwrite('imgs/dados/'+str(k)+'-'+str(i)+'.jpg',obj.img)
		i +=1

	
	print("objs"+str(k))
	k+=1
print("End =)")