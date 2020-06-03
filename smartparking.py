import time #importing time library
import lcddriver #importing lcddriver library for LED display
from firebase import firebase #importing firebase library to update sensor data to cloud
import RPi.GPIO as GPIO #importing GPIO for pin setup for sensor modules
import sys #importing system library

GPIO.setmode(GPIO.BCM) #setting the GPIO pins as BCM

firebase = firebase.FirebaseApplication("https://smart-park-815ad.firebaseio.com/", None) #referencing realtime database in firebase

#setting up GPIO pins in BCM mode
IREntryDoor_PIN = 14
IRExitDoor_PIN = 15
spot1_PIN = 25
spot2_PIN = 21
spot3_PIN = 22
spot4_PIN = 23

vacant = ['A', 'B', 'C', 'D'] #Making a list for vacant spots
detected = "Vehicle Detected" #variable for vehicle detection with IR sensors
not_detected = "Object Not Detected" #variable for vehicle detection with IR sensors
total_spots=4 # setting total number of spots

def entrydoor_sensor(): #module for sensing vehicles in entry door
    GPIO.setup(IREntryDoor_PIN, GPIO.IN) #setting entry sensor pi as input
    ir1 = GPIO.input(IREntryDoor_PIN) #setting ir1 as input
    if ir1 == 1: #condition for IR pin triggred
        print(detected)
        time.sleep(1)
    else: #condition if IR pin does not detect obstacle
        print(not_detected)
        time.sleep(1)
    return ir1 #module returns ir1 value if called

def exitdoor_sensor():
    GPIO.setup(IRExitDoor_PIN, GPIO.IN)
    ir2 = GPIO.input(IRExitDoor_PIN)
    if ir2 == 1:
        print(detected)
        time.sleep(1)
    else:
        print(not_detected)
        time.sleep(1)
    return ir2

#servo motor gate
SERVO_PIN = 17 #setting servo as BCM GPIO pin 17
GPIO.setup(SERVO_PIN,GPIO.OUT) #Setting up servo
servo1 = GPIO.PWM(SERVO_PIN,50) #Giving 50Hz power to GIPO17 pin
servo1.start(0) #initalizing servo

duty = 2 #setting initial duty cycle of servo 2

def entry_dooropen(): #module for servo triggred with IR sensor on door
    if entrydoor_sensor() == 1:
        print("Opening Door!")
        servo1.ChangeDutyCycle(6) #Opening door
        time.sleep(2)
        print ("Closing Door!")
        servo1.ChangeDutyCycle(2) #closing door
        
    else:
        servo1.ChangeDutyCycle(2) #do nothing
        time.sleep(0.5)
    
def exit_dooropen(): #module for exit door opening and closing       
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
    return exitdoor_sensor()

def spot_sensor1(): #IR sensor on spot to detect vehicles
    global total_spots
    GPIO.setup(spot1_PIN, GPIO.IN)
    ir3 = GPIO.input(spot1_PIN)
    if ir3 == 1:
        print(detected)
        total_spots -= 1
        result = firebase.put('/Space1','-M8KUSRLXu2ucAH83Brg', ir3)
        print("Updating Firebase")
        time.sleep(1)
    else:
        print(not_detected)
        result = firebase.put('/Space1','-M8KUSRLXu2ucAH83Brg', ir3)
        print("Updating Firebase")
        time.sleep(1)
    return ir3  
    
def spot_sensor2():
    global total_spots
    
    GPIO.setup(spot2_PIN, GPIO.IN)
    ir4 = GPIO.input(spot2_PIN)
    if ir4 == 1:
        print(detected)
        total_spots -= 1
        result = firebase.put('/Space2','-M8LBEPeDLOOpG3KuaPe', ir4)
        print(result)
        time.sleep(1)
    else:
        print(not_detected)
        result = firebase.put('/Space2','-M8LBEPeDLOOpG3KuaPe', ir4)
        print(result)
        time.sleep(1)
    return ir4
    
def spot_sensor3():
    global total_spots
    GPIO.setup(spot3_PIN, GPIO.IN)
    ir5 = GPIO.input(spot3_PIN)
    if ir5 == 1:
        print(detected)
        total_spots -= 1
        result = firebase.put('/Space3','-M8feie8DM7uLW5eyZzN', ir5)
        print(result)
        
    else:
        print(not_detected)
        result = firebase.put('/Space3','-M8feie8DM7uLW5eyZzN', ir5)
        print(result)
    return ir5

def spot_sensor4():
    global total_spots
    
    GPIO.setup(spot4_PIN, GPIO.IN)
    ir6 = GPIO.input(spot4_PIN)
    if ir6 == 1:
        print(detected)
        total_spots -= 1
        result = firebase.put('/Space4','-M8fomUu-8vHW6DCvOQl', ir6)
        print(result)
        time.sleep(1)
    else:
        print(not_detected)
        result = firebase.put('/Space4','-M8fomUu-8vHW6DCvOQl',ir6)
        print(result)
        time.sleep(1)
    return ir6
def leddisplay():
    while True:
        global total_spots
        
        if (total_spots == 3):
            display.lcd_display_string("Empty spots:" + total_spots, 1)
            print("All spots empty.")
        elif (total_spots == 1):
            if (spot_sensor1() and not(spot_sensor2()) and not(spot_sensor3())):
                display.lcd_display_string("Empty spots:" + total_spots, 1)
                display.lcd_display_string("Spot 1 empty", 2)
                print("Spot 1" + not_detected)
            elif (not(spot_sensor1()) and spot_sensor2() and not(spot_sensor3())):
                display.lcd_display_string("Total Number of empty spots:" + total_spots, 1)
                display.lcd_display_string("Spot 2 empty", 2)
                print("Spot 2" + not_detected)
            
            elif (not(spot_sensor1()) and not(spot_sensor2()) and spot_sensor3()):
                display.lcd_display_string("Total Number of empty spots:" + total_spots, 1)
                display.lcd_display_string("Spot 3 empty", 2)            
                print("Spot 3" + not_detected)
        elif (total_spots == 2):
            if (spot_sensor1() and (spot_sensor2()) and not(spot_sensor3())):
                display.lcd_display_string("Empty spots:" + total_spots, 1)
                display.lcd_display_string("Spot 1 and 2 empty", 2)
                print("Spot 1 and 2" + not_detected)
            elif (spot_sensor1() and not((spot_sensor2())) and spot_sensor3()):
                display.lcd_display_string("Empty spots:" + total_spots, 1)
                display.lcd_display_string("Spot 1 and 3 empty", 2)
                print("Spot 1 and 3" + not_detected)
            elif (not(spot_sensor1()) and (spot_sensor2()) and spot_sensor3()):
                display.lcd_display_string("Empty spots:" + total_spots, 1)
                display.lcd_display_string("Spot 2 and 3 empty", 2)
                print("Spot 2 and 3" + not_detected)
        elif (total_spots == 0):
            display.lcd_display_string("Empty spots:" + total_spots, 1)
            display.lcd_display_string("Parking full", 2)
            servo1.stop()
def occupied(ir3, ir4, ir5, ir6):
    if ir3 == 1 and ir4 == 1 and ir5 == 1 and ir6 == 1:
        servo1.stop()
        print("All Spaces Occupied!")

while True: #using while loop for continuous monitoring
    try:
        entry_dooropen()
        exit_dooropen()
        spot_sensor1()
        spot_sensor2()
        spot_sensor3()
        spot_sensor4()
    except KeyboardInterrupt:
        print("System Interruped by user!")
        servo1.stop()
        GPIO.cleanup()
        sys.exit()

            

        

