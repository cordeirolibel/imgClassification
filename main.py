#>>>>>>>>	Image classification - OpenCV	  <<<<<<<<<<#
#		Cordeiro Libel - UTFPR - April of 2016		    #
#-------------------------------------------------------#

#My libraries
from commons import *
from border import *
from identify import *


#=============================================
#======MAIN
#=============================================


#=============================================
#====CAPTURE IMAGE FROM CAMERA
#=============================================
# initialize the camera and grab a reference to the raw camera capture
#camera = PiCamera()
#rawCapture = PiRGBArray(camera)

# allow the camera to warm up, in seconds
#time.sleep(0.1)

# grab an image from the camera
#camera.capture(rawCapture, format='bgr')
#image = rawCapture.array

#=============================================
#======CAPTURE IMAGE FROM FILE
#=============================================
image = cv2.imread('imgs/objs1.jpg')
inv = False
#=============================================

show(image, 'Original')
image = cutBorder(image, inv = inv)
show(image, 'Without Border')

#Contours - identify Objects
objs_yes,objs_not = identifyObjects(image)

#Calculate attributes for the Deep Learning
attributes(image,objs_yes)

k=0
for obj in objs_yes:
	k +=1
	#show(obj.img,"f"+str(k))

#Draw the contours and the center of mass
image = drawCnts(image,objs_yes,objs_not, attributes = True)


show(image,"Contornos")

#save image
#cv2.imwrite('imgs/saida.jpg',image)

cv2.waitKey(0)

cv2.destroyAllWindows()