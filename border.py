#>>>>>>>>       Cutting Border Functions      <<<<<<<<<<#
#        Cordeiro Libel - UTFPR - April of 2016         #
#-------------------------------------------------------#

#My libraries
from commons import *

# Find the largest contour
def largestCnt(contours):
	area = 0
	largest_cnt = 0

	for cnt in contours:
		cnt_area = cv2.contourArea(cnt)
		if	cnt_area > area:
			area = cnt_area
			largest_cnt = cnt
	return largest_cnt

#simplify in 4 points
def findCorner(points,x_max,y_max):

	length = {'NW':[],'SW':[],'SE':[],'NE':[],'Point':[]}
	four_points = np.array([[0,0],[0,0],[0,0],[0,0]])

	#save the distance^2 of each point to the vertices of the image
	for pt in points:
		length['NW'].append((pt[0]-  0  )**2 + (pt[1]-  0  )**2) 
		length['NE'].append((x_max-pt[0])**2 + (pt[1]-  0  )**2)
		length['SW'].append((pt[0]-  0  )**2 + (y_max-pt[1])**2)
		length['SE'].append((x_max-pt[0])**2 + (y_max-pt[1])**2)
		length['Point'].append(pt) 

	#save point closer NW vertice
	index = length['NW'].index(min(length['NW']))
	four_points[0] = points[index]
	#save point closer NW vertice
	index = length['NE'].index(min(length['NE']))
	four_points[1] = points[index]
	#save point closer SW vertice
	index = length['SW'].index(min(length['SW']))
	four_points[2] = points[index]
	#save point closer SE vertice
	index = length['SE'].index(min(length['SE']))
	four_points[3] = points[index]

	return four_points


def cutBorder(img, fix_size = False, size = SIZE_IMG):
	# ==> Step 1: Resize 

	#We have 2 options (uncomment):

	#  Option 1:Resize
	#Resize to the max size to be "size" - default SIZE_IMG
	#img_size = img.shape
	#scale,small_img = resize(img,size)

	#  Option 2: Not Resize
	img_size = img.shape
	small_img = img
	scale = 1

	# ==> Step 2: Binary image
	#Transform in a binary image
	binary_img = binaryImg(small_img)

	# ==> Step 3: Contour
	# Find all external contours
	_,contours,_ = cv2.findContours(binary_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE )

	# Find the largest contour
	cnt = largestCnt(contours)[:,0,:]

	#simplify in 4 points
	four_points = findCorner(cnt,small_img.shape[1],small_img.shape[0])

	#uncomment to print contours
	#cv2.drawContours(small_img,[cnt],-1,(255,0,0),5)
	#show(small_img)

	# ==> Step 4: Cut

	#Coordinates of the corresponding quadrangle vertices in the destination image.
	if fix_size:
		dst = [[0,0],[size,0],[0,size],[size,size]]
	else:
		dst = [[0,0],[img_size[1],0],[0,img_size[0]],[img_size[1],img_size[0]]]

	#return to original scale
	#rint = mean each item, dot =  array*scalar
	src = np.rint(np.dot(four_points,1.0/scale))

	#Default format 
	src = np.float32(src)
	dst = np.float32(dst)

	#Transform and cut
	M = cv2.getPerspectiveTransform(src,dst)
	if fix_size:
		warped = cv2.warpPerspective(img, M, (size, size))
	else:
		warped = cv2.warpPerspective(img, M, (img_size[1], img_size[0]))

	return warped