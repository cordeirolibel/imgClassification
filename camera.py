#>>>>>>>>          Camera Functions           <<<<<<<<<<#
#        Cordeiro Libel - UTFPR - may of 2017           #
#-------------------------------------------------------#

from commons import *

FILE = 'imgs/cam1.jpg'

#===================================================
#=============Init Camera
#===================================================

camera = None
rawCapture = None
try: #running only in raspberry
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    #camera.resolution=(3280,2464)
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
        # grab an image from the camera
        camera.capture(rawCapture, format='bgr')
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
        cv2.imshow("Video", image)
        key = cv2.waitKey(1) & 0xFF
     
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
     
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    
    cv2.destroyWindow("Video")

    #return to original
    camera.resolution = resolution






