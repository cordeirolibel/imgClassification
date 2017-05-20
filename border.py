#>>>>>>>>	   Cutting Border Functions	      <<<<<<<<<<#
#		Cordeiro Libel - UTFPR - April of 2016	  	    #
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

#   Simplify points in 4 points  O(sqrt(n)) n:number of points
#Calculate the best four points is expensive.
#So we indenfy the best points in a samples of all points.
#As soon, we look around this sample and find the best point.
# . . . . . . . . . . . .
# ^         ^         ^ 
# |__jump___|__jump___|
def findCorner(points,x_max,y_max):
	four_points = np.array([[0,0],[0,0],[0,0],[0,0]])

	size = points.size/2

	#the cost function is C(samples) = samples+2*jump-1, for jump = (size-1)/samples
	#the minimal of the cost is dC(samples)/dsamples = 1-2*(size-1)*samples^-2 = 0, so samples = 1+sqrt(2*(size-1))
	#samples: number of samples for the aproximate the minimal and maximal element
	samples = toInt(np.sqrt(2*(size-1)))
	jump = 1.0*(size-1)/samples

	#====The first look (2 points)
	amin = 1000000
	amax = -1000000
	for i in range(samples+1): 
		index = toInt(i*jump)
		val = points[index][0]+points[index][1]
		if val<amin:
			#save point closer NW vertice
			n_min = index
			amin = val
		if val>amax:
			#save point closer SE vertice
			n_max = index
			amax = val
	four_points[0] = points[n_min]
	four_points[3] = points[n_max]

	#====The Second look (2 points), around the n_min and n_max
	for i in range(toInt(2*jump)-1):
		index = (n_min - toInt(jump) + 1 + i)%size
		val = points[index][0]+points[index][1]
		if val<amin:
			#save point closer NW vertice
			four_points[0] = points[index]
			amin = val

		index = (n_max - toInt(jump) + 1 + i)%size
		val = points[index][0]+points[index][1]
		if val>amax:
			#save point closer SE vertice
			four_points[3] = points[index]
			amax = val

	#====The first look (more 2 points)
	amin = 1000000
	amax = -1000000
	for i in range(samples+1): 
		index = toInt(i*jump)
		val = points[index][0]-points[index][1]
		if val<amin:
			#save point closer SW vertice
			n_min = index
			amin = val
		if val>amax:
			#save point closer NE vertice
			n_max = index
			amax = val
	four_points[2] = points[n_min]
	four_points[1] = points[n_max]

	#====The Second look (2 points), around the n_min and n_max
	for i in range(toInt(2*jump)-1):
		index = (n_min - toInt(jump) + 1 + i)%size
		val = points[index][0]-points[index][1]
		if val<amin:
			#save point closer SW vertice
			four_points[2] = points[index]
			amin = val

		index = (n_max - toInt(jump) + 1 + i)%size
		val = points[index][0]-points[index][1]
		if val>amax:
			#save point closer NE vertice
			four_points[1] = points[index]
			amax = val

	return four_points

def cutBorder(img, fix_size = True, size = SIDE, inv = False):
	# ==> Step 1: Resize 
	#We have 2 options (uncomment):

	#  Option 1:Resize
	#Resize to the max size to be SIZE_IMG
	#img_size = img.shape
	#scale,small_img = resize(img,SIZE_IMG)

	#  Option 2: Not Resize
	img_size = img.shape
	small_img = img
	scale = 1.0

	# ==> Step 2: Binary image
	#Transform in a binary image
	binary_img = binaryImg(small_img, inv = inv)

	# ==> Step 3: Contour
	# Find all external contours
	if cv2.__version__[0] is '3':
		_,contours,_ = cv2.findContours(binary_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE )
	else: #version 2.x.x
		contours,_ = cv2.findContours(binary_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE )
	
	# Find the largest contour
	cnt = largestCnt(contours)[:,0,:]

	#simplify in 4 points
	four_points = findCorner(cnt,small_img.shape[1],small_img.shape[0])

	#uncomment to print contours
	#cv2.drawContours(small_img,[four_points],-1,(255,0,0),5)
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
