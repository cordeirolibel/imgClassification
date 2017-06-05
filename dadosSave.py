#>>>>>>>>	Image classification - OpenCV	  <<<<<<<<<<#
#		Cordeiro Libel - UTFPR - 2017	        	    #
#-------------------------------------------------------#

#My libraries
from commons import *
from border import *
from identify import *

import cPickle as pickle #for the save objects 
from Tkinter import * #for buttons

#=============================================
#======SAVE IMAGE OF EACH OBJECT
#=============================================
obj_name = ''

# Events of Buttons
def cube():
	global obj_name
	obj_name = 'cube'
	root.quit() 
def sphere():
	global obj_name
	obj_name = 'sphere'
	root.quit() 
def L():
	global obj_name
	obj_name = 'L'
	root.quit() 
def plus():
	global obj_name
	obj_name = 'plus'
	root.quit() 
def rect():
	global obj_name
	obj_name = 'rect'
	root.quit() 
def coin():
	global obj_name
	obj_name = 'coin'
	root.quit() 
def on_closing():
	global obj_name
	obj_name = 'end'
	root.quit() 

# Create buttons
root = Tk()
root.wm_title('Select object')
Button(root, text='[ ] cube', command=cube).pack()
Button(root, text='( ) sphere', command=sphere).pack()
Button(root, text='     L     ', command=L).pack()
Button(root, text=' + plus ', command=plus).pack()
Button(root, text='[===] rect', command=rect).pack()
Button(root, text='(#) coin', command=coin).pack()
root.protocol("WM_DELETE_WINDOW", on_closing)

k=1
while True:
	#open all images with name
	image = cv2.imread('imgs/img'+str(k)+'.jpg')

	if image is None:
		break

	image = cutBorder(image)
	
	#Contours - identify Objects
	objs_yes,_ = identifyObjects(image, force_rasp = True)

	#Calculate attributes for the Classification
	attributes(image,objs_yes)
	show(image,'original')
	i=1
	for obj in objs_yes:
		#find and save the minimal image of each object
		obj.imageSave(image)
		#find the center of mass 
		obj.moments(image.shape)

		#wait for visual classification
		show(obj.img,'image')
		cv2.moveWindow('image', 300,20);
		cv2.waitKey(500)
		root.mainloop()
		#cv2.destroyWindow('image')

		if obj_name is 'end':#escape
			break

		#save obj name
		obj.name = obj_name

		#save obj in file
		name = 'imgs/data/'+str(k)+'-'+str(i)
		pickle.dump( obj, open(name+'.p', 'wb' ) )
		i +=1

		print('objs'+str(k)+'-'+str(i)+'  '+obj_name)

	k+=1

	if k is 11:
		break

	if obj_name is 'end':#escape
		break

print('End =)')

cv2.destroyAllWindows()
