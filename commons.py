#>>>>>>>>		  Commons Functions		      <<<<<<<<<<#
#		Cordeiro Libel - UTFPR - April of 2016		    #
#-------------------------------------------------------#

import time
import cv2
import numpy as np

try: #running only in raspberry
	import pigpio # for pwm servos
	from picamera.array import PiRGBArray
	from picamera import PiCamera
except:
	None

#==============
#====DEFINES
#==============
SIZE_IMG = 500 #default size image
SIDE = 1000 #for the cartesian plan
AREA_MIN = SIDE*SIDE*0.005
AREA_MAX = SIDE*SIDE*0.020

class Object(object):
	cnt = None 	#contours
	pt = None  	#Point in Cartesian plane (mass center)
	pt_img = None #Point in pixel (mass center)
	img = None 	#minimal image of object
	rect = None #best rectangle of image in Point and angles
	name = None #name of the object (sphere,cube, L, plus,...)
	#red cube,red sphere,red L,red plus,blue cube,blue sphere,blue L,blue plus

	#   For the DEEP LEARNING
	area = None 	#area 
	deform = None 	#distance of mass center and rectangle center
	circle = None 	#square sum of the distance of contours and mean of contours
	oblong = None 	#Reason between the large and small size
	perimeter = None #contour perimeter
	edges = None 	#aproximate the edges number 
	red = None 		#Intensity of red
	blue = None 	#Intensity of blue
	green = None 	#Intensity of green
	red_per_blue = None #Red per Blue
	out_per_in = None #White area per Area (White area: out of object, but in the rectangle rect)

	def __init__(self, cnt, area = None):
		self.cnt = cnt
		self.area = area
	
	#find the center of mass 
	#shape is the image.shape where be all objects
	def moments(self,shape):

		mu = cv2.moments(self.cnt)
		#calculate the center of mass and rint to int
		self.pt_img = (mu["m10"]/mu["m00"],mu["m01"]/mu["m00"])

		#Converting to cartesian plane
		self.pt= (valmap(self.pt_img[0],0,shape[1],0,SIDE),
				 valmap(self.pt_img[1],0,shape[0],SIDE,0))


	#find and save the minimal image of self in img
	def imageSave(self, img):
		self.rect = cv2.minAreaRect(self.cnt)
		self.img = cropMinRect(img,self.rect)


# Resize to the max size to be max_size
def resize(img, max_size = SIZE_IMG):
	# Make a consistent size
	#get largest dimension
	max_dimension = max(img.shape)
	#the percent of original image
	scale = 1.0*max_size/max_dimension
	#resize it. same width and hieght none since output is 'img'.
	img = cv2.resize(img, None, fx=scale, fy=scale)
	return scale,img


# display the image on screen and wait for a keypress
def show(img, name = 'fig', size = SIZE_IMG):	
	_,img = resize(img,max_size = size)#the max size is SIZE_IMG
	cv2.imshow(name, img)


#Transform in a binary image
#scale 0~1.0, near 0 more white
def binaryImg(img, scale = 0.5, inv = False):
	gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	if inv is False:
		_,binary_img = cv2.threshold(gray_img,int(255*scale),255,cv2.THRESH_BINARY)
	else:
		_,binary_img = cv2.threshold(gray_img,int(255*scale),255,cv2.THRESH_BINARY_INV) #for the inverted image
	
	return binary_img

# send a img and a rect (rectangle rotated)
# return a image in rectangle
def cropMinRect(img, rect):

	#===expand img
	angle = rect[2]
	rows,cols = img.shape[0], img.shape[1]
	# size fit 
	theta = np.deg2rad(abs(angle))
	phi = np.pi/2 - theta
	cols_new = toInt(cols*np.sin(theta) + rows*np.sin(phi))
	rows_new = toInt(cols*np.cos(theta) + rows*np.cos(phi))
	cols_add = toInt((cols_new-cols)/2) #in the border
	rows_add = toInt((rows_new-rows)/2)
	#create a Border, for don't crop in rotation
	img = cv2.copyMakeBorder(img,rows_add,rows_add,cols_add,cols_add,cv2.BORDER_CONSTANT,value=(255,255,255))
	
	# rotate img
	M = cv2.getRotationMatrix2D((toInt(cols_new/2),toInt(rows_new/2)),angle,1.0)
	img_rot = cv2.warpAffine(img,M,(cols_new,rows_new)) ######<<==================FUNCAO LENTA
	#show(img_rot)

	#===rotate bounding box
	rect0 = (rect[0], rect[1], 0.0)
	if cv2.__version__[0] is '3':
		box = cv2.boxPoints(rect)
	else: #version 2.x.x
		box = cv2.cv.BoxPoints(rect)
		box = np.array(box)

	for pt in box: #resize box
		pt[0] +=cols_add
		pt[1] +=rows_add

	pts = np.int0(cv2.transform(np.array([box]), M))[0]	
	pts[pts < 0] = 0

	# crop
	img_crop = img_rot[pts[1][1]:pts[0][1], 
					   pts[1][0]:pts[2][0]]

	#fix the base to be the largest side, if is not
	if img_crop.shape[0] > img_crop.shape[1]:
		#for color in img_crop:
		img_crop = cv2.transpose(img_crop)

	return img_crop


#converting value in  [in_min,in_max] to [out_min,out_max] keeping the scale
def valmap(value, in_min, in_max, out_min, out_max, is_int = True):
	if is_int:
  		return np.rint(out_min + (out_max - out_min) * (1.0*(value - in_min) / (in_max - in_min))).astype(int)
  	return out_min + (out_max - out_min) * (1.0*(value - in_min) / (in_max - in_min))

#converting var to int - accepts vectors and tuple
def toInt(val):
	#for tuple, rint each item
	if type(val) is tuple:
		out = ()
		for item in val:
			out += (np.rint(item).astype(int),)
		return out
	else:
		return np.rint(val).astype(int)

last_time  = time.time()
#function of time, milliseconds of last tic() 
#reset difine if you want clear the clock for ne next tic()
def tic(reset = True):
	global last_time
	toc = time.time()
	delta = toc - last_time
	if reset:
		last_time = toc
	return delta*1000

