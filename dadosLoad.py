#>>>>>>>>	Image classification - OpenCV	  <<<<<<<<<<#
#		Cordeiro Libel - UTFPR - April of 2016		    #
#-------------------------------------------------------#

#My libraries
from commons import *
#from border import *
from identify import *

import cPickle as pickle

#=============================================
#======SAVE IMAGE OF EACH OBJECT
#=============================================

n1=1
n2=1

objs = []

while True:
	#open all objs with name
	try:
		name = 'imgs/data/'+str(n2)+'-'+str(n1)+'.p'
		objs.append(pickle.load( open(name,'rb')))
	except:
		if n1 is 1:
			break
		n1 = 1
		n2 +=1
		continue


	print("objs "+str(n2)+'-'+str(n1))
	n1+=1

#Calculate attributes for the Deep Learning
attributes(None,objs)

	

print("End =)")