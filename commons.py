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
SIZE_IMG = 700 #default size image
AREA_MIN = 1000
AREA_MAX = 10000

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