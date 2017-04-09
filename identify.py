#>>>>>>>>           Identify Objects          <<<<<<<<<<#
#        Cordeiro Libel - UTFPR - April of 2016         #
#-------------------------------------------------------#

#My libraries
from commons import *

# Find the largests contours
def categoryCnts(img,contours):
	objs_yes = [] #Accepted Objects 
	objs_not = [] #Refused Objects

	area_max = img.shape[0]*img.shape[1]

	for cnt in contours:
		cnt_area = cv2.contourArea(cnt)
		#converting the area of pixel scale to cartesian scale of side SIDE
		cnt_area =  valmap(cnt_area,0,area_max,0,SIDE*SIDE)
		if	cnt_area > AREA_MIN and cnt_area < AREA_MAX:
			objs_yes.append(Object(cnt, cnt_area))
		else:
			objs_not.append(Object(cnt))

	return objs_yes, objs_not

#Identify all objets and save the contours
def identifyObjects(image, draw = True):
	image_b = binaryImg(image)

	#Erosion for connect the near objects
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
	image_b = cv2.erode(image_b,kernel,iterations = 1)

	#find all the contours
	_,contours,_ = cv2.findContours(image_b,cv2.RETR_LIST ,cv2.CHAIN_APPROX_SIMPLE )
	objs_yes,objs_not = categoryCnts(image_b,contours)

	#find the center of mass of each object
	for obj in objs_yes:
		obj.moments(image.shape)

	return objs_yes,objs_not


#Draw the contours and the center of mass
def drawCnts(image,objs_yes,objs_not, thickness = 7):

	#Converting if is not BRG
	if len(image.shape) is 2:
		image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)

	#Draw in green contours accepted
	for obj in objs_yes:
		cv2.drawContours(image,obj.cnt,-1,(0,255,0),thickness)

	#Draw in red contours refused
	for obj in objs_not:
		cv2.drawContours(image,obj.cnt,-1,(0,0,255),thickness)

	#Draw the center of mass of each object in blue
	for obj in objs_yes:
		cv2.circle(image, obj.pt_img,2*thickness, (255,0,0),-1)

		#converting points
		pt_text = (obj.pt_img[0]+100,obj.pt_img[1]+100)

		#write text
		cv2.putText(image,str(obj.pt),pt_text,cv2.FONT_HERSHEY_SIMPLEX,1.5, (255,0,0),thickness/2 )

	return image