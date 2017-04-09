#>>>>>>>>    Image classification - OpenCV    <<<<<<<<<<#
#        Cordeiro Libel - UTFPR - April of 2016         #
#-------------------------------------------------------#

#My libraries
from commons import *
from border import *


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



# Find the largests contours
def categoryCnts(contours):
	areas_yes = [] #Accept areas 
	areas_not = [] #Refused areas

	for cnt in contours:
		cnt_area = cv2.contourArea(cnt)
		if	cnt_area > AREA_MIN and cnt_area < AREA_MAX:
			areas_yes.append(cnt)
		else:
			areas_not.append(cnt)

	return areas_yes, areas_not

#find the center of mass of each object
def moments(contours):
	pts = []
	
	for cnt in contours:
		mu = cv2.moments(cnt)
		pts.append([mu["m10"]/mu["m00"],mu["m01"]/mu["m00"]])

	return np.rint(pts)

#=============================================
#======MAIN
#=============================================

# Resize to the max size to be SIZE_IMG
#size,image = resize(image,SIZE_IMG)


show(image, 'Original')

image = cutBorder(image, True)

show(image, 'Sem Borda')

image_b = binaryImg(image)
show(image_b, 'Binaria')

#Erosion and Dilation
#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))
#image_b = cv2.erode(image_b,kernel,iterations = 1)
#show(image_b, 'Erosion')
#image_b = cv2.dilate(image_b,kernel,iterations = 1)
#show(image_b, 'Dilation')

#Contornos - Identificacao de Objetos
_,contours,_ = cv2.findContours(image_b,cv2.RETR_LIST ,cv2.CHAIN_APPROX_SIMPLE )
cnts_yes,cnts_not = categoryCnts(contours)
image = cv2.cvtColor(image_b,cv2.COLOR_GRAY2BGR)
cv2.drawContours(image,cnts_yes,-1,(0,255,0),3)
cv2.drawContours(image,cnts_not,-1,(0,0,255),2)

#Identificacao do centro de cada objeto
pts = moments(cnts_yes)
for pt in pts:
	cv2.circle(image, (int(pt[0]),int(pt[1])), 5, (255,0,0),-1)

show(image,"Contornos")

#save image
cv2.imwrite('imgs/saida.jpg',image)

cv2.waitKey(0)

cv2.destroyAllWindows()