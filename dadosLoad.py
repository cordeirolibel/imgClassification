#>>>>>>>>	Image classification - OpenCV	  <<<<<<<<<<#
#		Cordeiro Libel - UTFPR - April of 2016		    #
#-------------------------------------------------------#

#My libraries
from commons import *
#from border import *
from identify import *
from classify import *
import cPickle as pickle

TESTES = 20 # 20% of data for the final test
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

	show(objs[-1].img,str(n2)+'-'+str(n1)+'-'+objs[-1].name)

	n1+=1

#Calculate attributes for the Classification
attributes(None,objs)
train(objs)


cv2.waitKey(0)

cv2.destroyAllWindows()


print("End =)")
