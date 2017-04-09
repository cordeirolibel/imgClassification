#>>>>>>>>    Image classification - OpenCV    <<<<<<<<<<#
#        Cordeiro Libel - UTFPR - April of 2016         #
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
image = cv2.imread('imgs/foto.jpg')
#=============================================


# Resize to the max size to be SIZE_IMG
#size,image = resize(image,SIZE_IMG)

#show(image, 'Original')
image = cutBorder(image)


#show(image, 'Without Border')

image_b = binaryImg(image)

show(image_b, 'Bin')

#Contours - identify Objects
objs_yes,objs_not = identifyObjects(image)


#Draw the contours and the center of mass
image = drawCnts(image,objs_yes,objs_not)


show(image,"Contornos")

#save image
cv2.imwrite('imgs/saida.jpg',image)

cv2.waitKey(0)

cv2.destroyAllWindows()