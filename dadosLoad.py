#>>>>>>>>	Image classification - OpenCV	  <<<<<<<<<<#
#		Cordeiro Libel - UTFPR - 2017       		    #
#-------------------------------------------------------#

#My libraries
from commons import *
#from border import *
from identify import *
from classify import *
import cPickle as pickle


#=============================================
#======SAVE IMAGE OF EACH OBJECT
#=============================================

n1=1
n2=1

objs = []

n_objs = dict()

while True:
	#open all objs with name
	try:
		name = 'imgs/data/'+str(n2)+'-'+str(n1)+'.p'
		obj = pickle.load( open(name,'rb'))
		objs.append(obj)

		if obj.name in n_objs:#save the number of each object
			n_objs[obj.name] += 1
		else:
			n_objs[obj.name] = 1

	except:
		if n1 is 1:
			break
		n1 = 1
		n2 +=1
		continue

	#show(objs[-1].img,str(n2)+'-'+str(n1)+'-'+objs[-1].name)

	n1+=1

#number of each object
print(n_objs)

#Calculate attributes for the Classification
#attributes(None,objs)

train(objs)


cv2.waitKey(0)

cv2.destroyAllWindows()


print("End =)")
