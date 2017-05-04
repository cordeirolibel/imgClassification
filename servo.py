#>>>>>>>>      Cutting Border Functions       <<<<<<<<<<#
#        Cordeiro Libel - UTFPR - may of 2016           #
#-------------------------------------------------------#

from commons import *

#===================================================
#=============Defines
#===================================================


#datasheet is [1000,2000], but in tests [600,2400]
PWM_MIN = 600
PWM_MAX = 2400
SPEED = 40/0.1 # 60degree/0.1s (datasheet)
TIME_MIN = SPEED*20#Never gives a time less than 20 degrees


#===================================================
#=============Init Servos GPIO 
#===================================================
pigpio = None
try: #running only in raspberry
    pigpio = pigpio.pi()
    if not pigpio.connected:
        print("try >> sudo pigpiod")
        exit()
except:
    None
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
        
        pigpio.set_servo_pulsewidth(self.pin, pulse) 
        
        self.wait_time = abs(self.angle - ang)/SPEED

        self.angle = ang
        
    def stop(self):
        pigpio.set_servo_pulsewidth(self.pin, 0) 

    #wait the servo move (time defined in serAngle)
    def wait():
        time.sleep(wait_time)


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
SPEED_MED = SPEED/2 #this speed define time T
def smooth(servos,angles):

    #find the biggest time of all movement servos and save all angles
    max_time = 0
    init_ang = []
    for servo,ang in zip(servos,angles):
        _time = abs(ang-servo.angle)/(SPEED_MED)
        if _time > max_time:
            max_time = _time

        init_ang.append(servo.angle)

    #converting to milliseconds
    max_time *= 1000 
    print(max_time)
    #movement
    for dtime in range(toInt(max_time)):
        for servo,ang1,ang2 in zip(servos,init_ang,angles):
            #See above graph 
            angle = (ang1-ang2)*(2**(-dtime/max_time+1)-1)**(1/BETA)+ang2
            servo.setAngle(angle)
        time.sleep(0.001)

#===================================================
#=============Main
#===================================================

servos = []
servos.append(Servo(26))
#servos.append(Servo(25))
#servos.append(Servo(24))
#servos.append(Servo(23))
#smooth(servos,[4,2,5,2])
servos[0].angle = -40





    
