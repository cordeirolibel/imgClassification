#>>>>>>>>		   Identify Objects		  	  <<<<<<<<<<#
#		Cordeiro Libel - UTFPR - April of 2017		    #
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

	#remove shawdow, because it is not an object
	img = shadowRemove(img)

	#show(img,"sem sombra")
	image_b = binaryImg(img, inv = inv)

	#Erosion and Dilate for connect the near objects
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
	#It works in reverse - image is reversed
	image_b = cv2.erode(image_b,kernel,iterations = 1) 
	image_b = cv2.dilate(image_b,kernel,iterations = 1)

	#find all the contours
	if cv2.__version__[0] is '3':
		_,contours,_ = cv2.findContours(image_b,cv2.RETR_LIST ,cv2.CHAIN_APPROX_SIMPLE )
	else:#version 2.x.x
		contours,_ = cv2.findContours(image_b,cv2.RETR_LIST ,cv2.CHAIN_APPROX_SIMPLE )
	objs_yes,objs_not = categoryCnts(image_b,contours)

	return objs_yes,objs_not

#Calculate attributes for the Deep Learning
def attributes(img,objs):

	for obj in objs:
		#if img is not None:

		#best rectangle of image in Point and angles
		obj.rect = cv2.minAreaRect(obj.cnt)

		#Save the minimal image of each object
		#obj.imageSave(img)

		#Find the center of mass of each object
		obj.moments(img.shape)

		#Area
		if obj.area is None:
			obj.area = cv2.contourArea(obj.cnt)

		#Distance of mass center and rectangle center
		if cv2.__version__[0] is '3':
			box = cv2.boxPoints(obj.rect)
		else:#version 2.x.x
			box = cv2.cv.BoxPoints(obj.rect)
			box = np.array(box, dtype=np.float32)
		
		center_pt = [np.mean(box[:,0]),np.mean(box[:,1])]
		obj.deform = np.sqrt((center_pt[0]-obj.pt_img[0])**2+(center_pt[1]-obj.pt_img[1])**2)

		#Square sum of the distance of contours and mean of contours
		dists = []
		for pt in obj.cnt:
			dists.append(np.sqrt((obj.pt_img[0]-pt[0,0])**2+(obj.pt_img[1]-pt[0,1])**2))
		mean = np.mean(dists) #distance mean of contours and mass center
		obj.circle = 0.0
		for dist in dists:
			obj.circle += (mean-dist)**2
		obj.circle = obj.circle/len(dists)
		
		#Reason between the large and small size
		obj.oblong = 1.0*obj.rect[1][1]/obj.rect[1][0]

		#Contour perimeter
		obj.perimeter = cv2.arcLength(obj.cnt,True)
		
		#aproximate the edges number 
		obj.edges = len(cv2.approxPolyDP(obj.cnt, 0.03 * obj.perimeter, True))
		
		#Intensity of colors <=====================Ver melhor isso ak, ele tira a media junto com a borda que eh sempre branca(todas as cores)
		#mean_colors = cv2.mean(obj.img)
		#obj.blue = mean_colors[0]
		#obj.green = mean_colors[1]
		#obj.red = mean_colors[2]
		#obj.red_per_blue = obj.red/obj.blue
		obj.red_per_blue = 8000

		#White area per Area (White area: out of object, but in the rectangle rect)
		obj.out_per_in = (cv2.contourArea(box) - obj.area)/obj.area

#remove the simple shadow (not all shadow)
def shadowRemove(img):

	imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	#colors filter between color 1 and color2
	mask = cv2.inRange(imgHSV,  np.array([0,0,0]),  np.array([255,130,179]))#in pc
	#mask = cv2.inRange(imgHSV,  np.array([0,0,100]),  np.array([255,100,179]))#in raspberry 

	#removing noise of mask
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(4,4))
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)#or cv2.MORPH_HITMISS

	#Join mask with the img
	img = img.copy()
	img[mask > 0] = 255

	return img

#Draw the contours and the center of mass
def drawCnts(img,objs_yes,objs_not, thickness = 4, attributes = False):

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
		if cv2.__version__[0] is '3':
			box = cv2.boxPoints(obj.rect)
		else: #version 2.x.x
			box = cv2.cv.BoxPoints(obj.rect)
			box = np.array(box)
		box = toInt(box)
		cv2.drawContours(img,[box],-1,(255,50,255),thickness)

	#Draw the center of mass of each object in blue
	for obj in objs_yes:
		cv2.circle(img, (toInt(obj.pt_img)),2*thickness, (0,0,0),-1)

		#converting points
		pt_text = (int(obj.pt_img[0])+25,int(obj.pt_img[1])+25)

		#define text
		if attributes:
			text = [str(obj.pt),\
					'area: '+str(obj.area),\
					'deform: '+str(round(obj.deform,2)),\
					'circle: '+str(round(obj.circle,1)),\
					'oblong: '+str(round(obj.oblong,2)),\
					'perimeter: '+str(toInt(obj.perimeter)),\
					'edges:'+str(obj.edges),\
					'RperB: '+str(round(obj.red_per_blue,2)),\
					'OutPerIn: '+str(round(obj.out_per_in,2))]
		else:
			text = [str(obj.pt)]
		if obj.name is not None:
			text = [obj.name]+ text
		#write text
		for line in text:
			pt_text = (pt_text[0],pt_text[1]+thickness*5)
			cv2.putText(img,line,pt_text,cv2.FONT_HERSHEY_SIMPLEX,thickness/5.0, (0,0,0),thickness/2 )

	return img
