#>>>>>>>>       Servo Functions               <<<<<<<<<<#
#        Cordeiro Libel - UTFPR - 2017                  #
#-------------------------------------------------------#

from commons import *

#===================================================
#=============Defines
#===================================================


#datasheet is [1000,2000], but in tests [600,2400]
PWM_MIN = 600
PWM_MAX = 2400

SPEED = 40/0.1 # 60degree/0.1s (datasheet)
TIME_MIN = 10/SPEED#Never gives a time less than 20 degrees

ANG_OPEN = -35
ANG_CLOSE = 60

#===================================================
#=============Init Servos GPIO 
#===================================================
if runOnRasp(): #running only in raspberry
    global pigpio
    pigpio = pigpio.pi()
    if not pigpio.connected:
        print("try >> sudo pigpiod")
        exit()

#===================================================
#=============Servo Class
#===================================================
class Servo(object):
    angle = None
    pin = None
    
    def __init__(self, pin, angle = 0):
        self.pin = pin
        self.angle = angle
    
    #go to ang
    def setAngle(self,ang):
        global pigpio

        if ang<-90 or 90<ang:
            print("Out of servo range: "+str(ang)+" degrees")
            return
        
        pulse = valmap(ang,-90,90,PWM_MIN,PWM_MAX)
        
        if runOnRasp():
            pigpio.set_servo_pulsewidth(self.pin, pulse) 
        
        self.wait_time = abs(self.angle - ang)/SPEED

        self.angle = ang

    def open(self):
        smooth(self,ANG_OPEN)
        
    def close(self):
        smooth(self,ANG_CLOSE)
        
    def stop(self):
        if runOnRasp():
            pigpio.set_servo_pulsewidth(self.pin, 0) 


    #wait the servo move (time defined in setAngle)
    def wait(self):
        if self.wait_time > TIME_MIN:
            time.sleep(self.wait_time)
        else:
            time.sleep(TIME_MIN)
            wait_time = 0


#===================================================
#=============Smooth move
#===================================================


#     Angle
#       |
#       |
#  ang1 |*
#       | *       y=(ang1-ang2)*(2^(-x/T+1)-1)^(1/beta)+ang2
#       |  *       
#       |    *
#       |      *
#       |         *
#       |              *
#  ang2 |. . . . . . . . . . . . . .*                           
#       |                           .
#_______|_________________________________ Time(s)
#       |                           T      
#

BETA = 0.4 # convergence speed ]0,1] NEVER ZERO
SPEED_MED = SPEED/4 #this speed define time T
SLEEP = 0.05 # 0.05 - Recomanded

def smooth(servos,angles, wait = True, stop = True):
    
    #if is only 1 servo
    if not isinstance(angles, (list, tuple)):
        angles = [angles]
    if not isinstance(servos, (list, tuple)):
        servos = [servos]

    #find the biggest time of all movement servos and save all angles
    max_time = TIME_MIN
    init_ang = []
    times = []
    for servo,ang in zip(servos,angles):

        #find the biggest time of all movement servos
        _time = abs(ang-servo.angle)/(SPEED_MED)
        times.append(toInt(_time/SLEEP))

        if _time > max_time:
            max_time = _time
        
        #save angles
        if ang<-90 or 90<ang:
            print("Out of servo range: "+str(ang)+" degrees")
            return
        init_ang.append(servo.angle)

    #converting to milliseconds
    max_time = toInt(max_time/SLEEP) #(1000*max_time)/(SLEEP*1000) accuracy

    #movement
    k = 0
    for dtime in range(max_time):

        k+=1
        for servo,ang1,ang2, _time in zip(servos,init_ang,angles, times):
            if dtime > _time:# servo movement finished
                #servo.stop()
                continue
            if _time == 0:
                continue
            else:
                #See above graph 
                angle = (ang1-ang2)*(2**(-1.0*dtime/_time+1)-1)**(1/BETA)+ang2
            servo.setAngle(angle)
        if wait:
            time.sleep(SLEEP)
        
    #stop all servos
    if stop:
        for servo in servos:
            servo.stop()

#move all sevos - not smooth
def allMove(servos,angles, wait = True, stop = True):
    
    #if is only 1 servo
    if not isinstance(angles, (list, tuple)):
        angles = [angles]
    if not isinstance(servos, (list, tuple)):
        servos = [servos]

    for servo,ang in zip(servos,angles):
        servo.setAngle(ang)
        if wait:
            servo.wait()
        if stop:
            servo.stop()


#===================================================
#=============Default Angles
#===================================================
ANG_DEFAULT = [0,0,0]
ANG_TAKE = [0,0,0]#Angles for take the Obj
ANG_BOX = [0,0,0]

def take(servos):

    #Default position
    smooth(servos[:3],ANG_DEFAULT,stop=False)
    servos[3].open()

    #Obj position
    smooth(servos[:3],ANG_TAKE,stop=False)
    servos[3].close()

    #Default position
    smooth(servos[:3],ANG_DEFAULT,stop=False)

    #Box position
    smooth(servos[:3],ANG_BOX,stop=False)
    servos[3].open()

    #Default position
    smooth(servos[:3],ANG_DEFAULT,stop=False)
    servos[3].close()

    #Stop all
    for servo in servos:
        servo.stop()


def start(servos):
    for servo, angle in zip(servos,ANG_DEFAULT+[ANG_CLOSE]):
        servo.angle = 90
        servo.setAngle(0)
        servo.setAngle(angle)
        servo.wait()




    
