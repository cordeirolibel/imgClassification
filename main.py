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


# Resize to the max size to be SIZE_IMG
#size,image = resize(image,SIZE_IMG)

#show(image, 'Original')
image = cutBorder(image, inv = inv)
#show(image, 'Without Border')

blue, green, red = cv2.split(image)

image_b = binaryImg(image)






imgHSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

mask = cv2.inRange(imgHSV, np.array([0,0,0]), np.array([180,255,120]))

image_mask = cv2.bitwise_and(image,image, mask = mask)

show(image, 'image')
#image = cv2.cvtColor(imgThreshold,cv2.COLOR_HSV2BGR)
show(mask, 'mask')
show(image_mask, 'image_mask')

image = cv2.addWeighted(image_mask, 1.0, image, 1.0, 0)
show(image, 'image2')





#Contours - identify Objects
objs_yes,objs_not = identifyObjects(image)
#find and save the minimal image of each object
imagesSave(image,objs_yes)

k=0
for obj in objs_yes:
	k +=1
	#show(obj.img,"f"+str(k))

#Draw the contours and the center of mass
image = drawCnts(image,objs_yes,objs_not, 5)


show(image,"Contornos")

#save image
#cv2.imwrite('imgs/saida.jpg',image)

cv2.waitKey(0)

cv2.destroyAllWindows()