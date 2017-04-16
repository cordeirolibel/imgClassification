#>>>>>>>>		   Identify Objects		  	  <<<<<<<<<<#
#		Cordeiro Libel - UTFPR - April of 2016		    #
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
		#print(cnt_area)
		if	cnt_area > AREA_MIN and cnt_area < AREA_MAX:
			objs_yes.append(Object(cnt, cnt_area))
		else:
			objs_not.append(Object(cnt))

	return objs_yes, objs_not

#Identify all objets and save the contours
def identifyObjects(img, draw = True, inv = False):
	image_b = binaryImg(img, inv = inv)

	#Erosion and Dilate for connect the near objects
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
	#It works in reverse - image is reversed
	image_b = cv2.erode(image_b,kernel,iterations = 1) 
	image_b = cv2.dilate(image_b,kernel,iterations = 1)

	#find all the contours
	_,contours,_ = cv2.findContours(image_b,cv2.RETR_LIST ,cv2.CHAIN_APPROX_SIMPLE )
	objs_yes,objs_not = categoryCnts(image_b,contours)

	#find the center of mass of each object
	for obj in objs_yes:
		obj.moments(img.shape)

	return objs_yes,objs_not

#find and save the minimal image of each object
def imagesSave(img,objs):
	for obj in objs:
		obj.imageSave(img)


#Draw the contours and the center of mass
def drawCnts(img,objs_yes,objs_not, thickness = 5):

	img = img.copy()

	#Converting if is not BRG
	if len(img.shape) is 2:
		img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

	#Draw in green contours accepted
	for obj in objs_yes:
		cv2.drawContours(img,obj.cnt,-1,(0,255,0),thickness)

	#Draw in red contours refused
	for obj in objs_not:
		cv2.drawContours(img,obj.cnt,-1,(0,0,255),thickness)

	#Draw a rectangle of each obj
	for obj in objs_yes:
		box = cv2.boxPoints(obj.rect)
		box = toInt(box)
		img = cv2.drawContours(img,[box],-1,(255,0,255),thickness)

	#Draw the center of mass of each object in blue
	for obj in objs_yes:
		cv2.circle(img, obj.pt_img,2*thickness, (255,0,0),-1)

		#converting points
		pt_text = (obj.pt_img[0]+50,obj.pt_img[1]+50)

		#write text
		cv2.putText(img,str(obj.pt),pt_text,cv2.FONT_HERSHEY_SIMPLEX,0.7, (255,0,0),thickness/2 )

	return img

