#>>>>>>>>	Image classification - OpenCV	  <<<<<<<<<<#
#		Cordeiro Libel - UTFPR - April of 2016		    #
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
def cubeR():
	global obj_name
	obj_name = 'red cube'
	root.quit() 
def sphereR():
	global obj_name
	obj_name = 'red sphere'
	root.quit() 
def LR():
	global obj_name
	obj_name = 'red L'
	root.quit() 
def plusR():
	global obj_name
	obj_name = 'red plus'
	root.quit() 
def cubeB():
	global obj_name
	obj_name = 'blue cube'
	root.quit() 
def sphereB():
	global obj_name
	obj_name = 'blue sphere'
	root.quit() 
def LB():
	global obj_name
	obj_name = 'blue L'
	root.quit() 
def plusB():
	global obj_name
	obj_name = 'blue plus'
	root.quit() 
def on_closing():
	global obj_name
	obj_name = 'end'
	root.quit() 

# Create buttons
root = Tk()
root.wm_title('Select object')
Button(root, text='[ ] cube', fg='white', bg='red', command=cubeR).pack()
Button(root, text='( ) sphere', fg='white', bg='red', command=sphereR).pack()
Button(root, text='     L     ', fg='white', bg='red', command=LR).pack()
Button(root, text='+ plus', fg='white', bg='red', command=plusR).pack()
Button(root, text='[ ] cube', fg='white', bg='blue', command=cubeB).pack()
Button(root, text='( ) sphere', fg='white', bg='blue', command=sphereB).pack()
Button(root, text='     L     ', fg='white', bg='blue', command=LB).pack()
Button(root, text='+ plus', fg='white', bg='blue', command=plusB).pack()
root.protocol("WM_DELETE_WINDOW", on_closing)

k=1
while True:
	#open all images with name
	image = cv2.imread('imgs/objs'+str(k)+'.jpg')

	if image is None:
		break

	image = cutBorder(image)
	
	#Contours - identify Objects
	objs_yes,_ = identifyObjects(image)

	i=1
	for obj in objs_yes:
		#find and save the minimal image of each object
		obj.imageSave(image)
		#find the center of mass 
		obj.moments(image.shape)

		#wait for visual classification
		show(obj.img,'image')
		cv2.moveWindow('image', 300,20);
		cv2.waitKey(1000)
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

	if obj_name is 'end':#escape
		break

print('End =)')

cv2.destroyAllWindows()
