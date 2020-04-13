import time
from gpiozero import LED
from signal import pause
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#IR sensor gate
IREntryDoor_PIN = 14

IRExitDoor_PIN = 15

vacant = ['A', 'B', 'C'] #Making a list for vacant spots
detected = "Vehicle Detected"
not_detected = "Object Not Detected"
car_sensed = False


def entrydoor_sensor():
    GPIO.setup(IREntryDoor_PIN, GPIO.IN)
    ir1 = GPIO.input(IREntryDoor_PIN)
    if ir1 == 1:
        print(detected)
    else:
        print(not_detected)
        
    return ir1

def exitdoor_sensor():
    GPIO.setup(IRExitDoor_PIN, GPIO.IN)
    ir1 = GPIO.input(IRExitDoor_PIN)
    if ir2 == 1:
        print(detected)
    else:
        print(not_detected)
        
    return ir2
#firebase = firebase.FirebaseApplication('https://smart-parking-system-4b401.firebaseio.com/', None)    
    
#servo motor gate
SERVO_PIN = 17
GPIO.setup(SERVO_PIN,GPIO.OUT)
servo1 = GPIO.PWM(SERVO_PIN,50) #Giving 50Hz power to GIPO17 pin
servo1.start(0)

duty = 2
# Opening the door
def entry_dooropen:
    if entrydoor_sensor() == 1:
        print("Entering")
        servo1.ChangeDutyCycle(6)

        time.sleep(2)
        print ("Closing door")
        servo1.ChangeDutyCycle(2)
        entrydoor_sensor1() == 0 #closing the ir sensor
    else:
        servo1.ChangeDutyCycle(2) #do nothing
        time.sleep(0.5)


def exit_dooropen:        
    if exitdoor_sensor() == 1:
        print("Entering")
        servo1.ChangeDutyCycle(6)

        time.sleep(2)
        print ("Closing door")
        servo1.ChangeDutyCycle(2)
        exitdoor_sensor() == 0 #closing the ir sensor
    else:
        servo1.ChangeDutyCycle(2) #do nothing
        time.sleep(0.5)
#def update_firebase():
    #if ir_sensor2() == 1:
     #   print("Object Detected")
        
#data = {"Spot1": detected}
#firebase.post('/sensor/dht', data)

servo1.stop()
GPIO.cleanup()  
