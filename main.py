#>>>>>>>>   Image classification - OpenCV     <<<<<<<<<<#
#       Cordeiro Libel - UTFPR - April of 2016          #
#-------------------------------------------------------#

#My libraries
from commons import *
from border import *
from identify import *
from servo import *
from camera import *

#=============================================
#======MAIN
#=============================================

#=====Camera init

 
inv = False
#video()
image = capture(False)

show(image, 'Original')


image = cutBorder(image, inv = inv)
show(image, 'Without Border')

#Contours - identify Objects
objs_yes,objs_not = identifyObjects(image)

#Calculate attributes for the Deep Learning
attributes(image,objs_yes)

k=0
for obj in objs_yes:
    k +=1

    #show(obj.img,"f"+str(k))

#Draw the contours and the center of mass
image = drawCnts(image,objs_yes,objs_not, attributes = True)


show(image,"Contornos")

#save image
#cv2.imwrite('imgs/saida.jpg',image)

cv2.waitKey(0)

cv2.destroyAllWindows()
