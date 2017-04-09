#>>>>>>>>          Commons Functions          <<<<<<<<<<#
#        Cordeiro Libel - UTFPR - April of 2016         #
#-------------------------------------------------------#

#from picamera.array import PiRGBArray
#from picamera import PiCamera
import time
import cv2
import numpy as np

#==============
#====DEFINES
#==============
SIZE_IMG = 800 #default size image
SIDE = 1000 #for the cartesian plan
AREA_MIN = SIDE*SIDE*0.003
AREA_MAX = SIDE*SIDE*0.015

class Object(object):
	cnt = None #conturs
	pt = None  #Point in Cartesian plane
	pt_img = None #Point in pixel
	area = None #area

	def __init__(self, cnt, area = None):
		self.cnt = cnt
		self.area = area

	#find the center of mass 
	#shape is the image.shape where be all objects
	def moments(self,shape):
		mu = cv2.moments(self.cnt)
		#calculate the center of mass and rint to int
		self.pt_img = (np.rint(mu["m10"]/mu["m00"]).astype(int),np.rint(mu["m01"]/mu["m00"]).astype(int))

		#Converting to cartesian plane
		self.pt= (valmap(self.pt_img[0],0,shape[1],0,SIDE),
			     valmap(self.pt_img[1],0,shape[0],SIDE,0))

# Resize to the max size to be max_size
def resize(image, max_size = SIZE_IMG):
	# Make a consistent size
	#get largest dimension
	max_dimension = max(image.shape)
	#the percent of original image
	scale = 1.0*max_size/max_dimension
	#resize it. same width and hieght none since output is 'image'.
	image = cv2.resize(image, None, fx=scale, fy=scale)
	return scale,image

# display the image on screen and wait for a keypress
def show(img, name = 'fig'):
	_,img = resize(img,SIZE_IMG)#the max size is SIZE_IMG
	cv2.imshow(name, img)

#Transform in a binary image
#scale 0~1.0, near 0 more white
def binaryImg(img, scale = 0.5):
	gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#_,binary_img = cv2.threshold(gray_img,int(255*scale),255,cv2.THRESH_BINARY_INV) #for the inverted image
	_,binary_img = cv2.threshold(gray_img,int(255*scale),255,cv2.THRESH_BINARY)
	return binary_img

#converting value in  [in_min,in_max] to [out_min,out_max] keeping the scale
def valmap(value, in_min, in_max, out_min, out_max, is_int = True):
	if is_int:
  		return np.rint(out_min + (out_max - out_min) * (1.0*(value - in_min) / (in_max - in_min))).astype(int)
  	return out_min + (out_max - out_min) * (1.0*(value - in_min) / (in_max - in_min))