#>>>>>>>>          Camera Functions           <<<<<<<<<<#
#        Cordeiro Libel - UTFPR -  2017                 #
#-------------------------------------------------------#

from commons import *
from border import *
from identify import *
FILE = 'imgs/img3.jpg'

#===================================================
#=============Init Camera
#===================================================

camera = None
rawCapture = None
try: #running only in raspberry
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution=(3280,2464)
    rawCapture = PiRGBArray(camera)
    # allow the camera to warm up, in seconds
    time.sleep(0.1)
except:
    None

#carrega uma imagem
#cam: True (camera), False (file)
def capture(cam = False):

    global camera, rawCapture

    #====CAPTURE IMAGE FROM CAMERA
    if cam is True:
        # clear the stream 
        rawCapture.seek(0)
        rawCapture.truncate()
        
        # grab an image from the camera
        camera.capture(rawCapture, format='bgr',use_video_port = True)
        img = rawCapture.array

    #======CAPTURE IMAGE FROM FILE
    else:
        img = cv2.imread(FILE)
    
    return img
        
#start a video, close the window with key 'q'
def video():
    global camera
    resolution = camera.resolution 
    
    #config
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))


    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
     
        # show the frame
        show(image,'video', size = SIZE_IMG*2/3)
        #cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
     
        # clear the stream in preparation for the next frame
        rawCapture.seek(0)
        rawCapture.truncate()
     
        # exit
        if key == ord("q"):
            quit()
            
        # exit loop
        elif key == ord(" "):
            break

    #return to original
    camera.resolution = resolution




