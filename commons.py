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
	img = None #minimal image of object
	rect = None #best rectangle of image in Point and angles

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

# send a img and a rect (rectangle rotated)
# return a image in rectangle
def cropMinRect(img, rect):

    # rotate img
    angle = rect[2]
    rows,cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    img_rot = cv2.warpAffine(img,M,(cols,rows))

    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.boxPoints(rect)
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