import time #importing time library
import lcddriver #importing lcddriver library for LED display
from firebase import firebase #importing firebase library to update sensor data to cloud
import RPi.GPIO as GPIO #importing GPIO for pin setup for sensor modules
import sys #importing system library

GPIO.setmode(GPIO.BCM) #setting the GPIO pins as BCM

firebase = firebase.FirebaseApplication("https://smart-park-815ad.firebaseio.com/", None) #referencing realtime database in firebase

#setting up GPIO pins in BCM mode
IREntryDoor_PIN = 17 #setting IR sensor on the entry as GPIO pin 17 in BCM
IRExitDoor_PIN = 15 #setting IR sensor on the exit as GPIO pin 15 in BCM
spot1_PIN = 25 #setting IR sensor on space A as GPIO pin 25 in BCM
spot2_PIN = 21 #setting IR sensor on space B as GPIO pin 21 in BCM
spot3_PIN = 22 #setting IR sensor on space C as GPIO pin 22 in BCM
spot4_PIN = 23 #setting IR sensor on space D as GPIO pin 23 in BCM
SERVO_PIN = 14 #setting servo as GPIO pin 14 in BCM

vacant = ['A', 'B', 'C', 'D'] #Making a list for vacant spots
detected = "Vehicle Detected" #variable for vehicle detection with IR sensors
not_detected = "Object Not Detected" #variable for vehicle detection with IR sensors
total_spots=3 # setting total number of spots

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


GPIO.setup(SERVO_PIN,GPIO.OUT) #Setting up servo
servo1 = GPIO.PWM(SERVO_PIN,50) #Giving 50Hz power to the servo GPIO pin
servo1.start(0) #starting servo

def entry_dooropen(): #module for servo triggred with IR sensor on entry door
    if entrydoor_sensor() == 1:
        print("Opening Door!") # Printing Opening door on the system
        servo1.ChangeDutyCycle(6) #Opening door
        time.sleep(2)
        print ("Closing Door!")
        servo1.ChangeDutyCycle(2) #closing door
        
    else:
        servo1.ChangeDutyCycle(2) #do nothing
        time.sleep(1)
    
def exit_dooropen(): #module for exit door opening and closing       
    if exitdoor_sensor() == 1: #when the IR sensor on the exit door is triggred
        print("Exiting") #Printing Exiting
        servo1.ChangeDutyCycle(6) # Openint the door at 90 degree angle
        time.sleep(2)
        print ("Closing door")
        servo1.ChangeDutyCycle(0)
        exitdoor_sensor() == 0 #closing the ir sensor
    else:
        servo1.ChangeDutyCycle(0) #do nothing
        time.sleep(1)
    return exitdoor_sensor()

def spot_sensor1(): #IR sensor on spot A to detect vehicles
    global total_spots #calling total spots variable
    GPIO.setup(spot1_PIN, GPIO.IN) # setting up the IR sensor
    ir3 = GPIO.input(spot1_PIN) #Setting ir3 as the input for the GPIO pin
    if ir3 == 1: # Obstruction is detected
        print(detected) # Printing Vehicle detected
        total_spots -= 1 # reducing teh total spots by 1
        result = firebase.put('/Space1','-M8KUSRLXu2ucAH83Brg', ir3) # Updating the data (1) into firebase
        print("Updating Firebase") #Printing updating firebase
        time.sleep(1) #Pausing the IR sensor for 1 second
    else: #Object not detected
        print(not_detected) # Printing object not detected
        result = firebase.put('/Space1','-M8KUSRLXu2ucAH83Brg', ir3) #Updating the data (0) into firebase
        print("Updating Firebase") # Printing updating firebase
        time.sleep(1) # Pausing the IR sensor for 1 second
    return ir3  # Returing the value of ir3 if the function is called
    
def spot_sensor2(): #IR sensor on spot B to detect vehicles
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
    
def spot_sensor3(): #IR sensor on spot C to detect vehicles
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

def spot_sensor4(): #IR sensor on spot D to detect vehicles
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

def leddisplay(): #Led display module
    while True: 
        global total_spots #calling total spots
        
        if (total_spots == 3): # If total spots equals 3
            display.lcd_display_string("Empty spots:" + total_spots, 1) # Empty spots 3 is displayed on line 1
            print("All spots empty.") # Prining all spots empty
        elif (total_spots == 1): #If 1 spot is empty on the parking
            if (spot_sensor1() and not(spot_sensor2()) and not(spot_sensor3())): #And that space is A
                display.lcd_display_string("Empty spots:" + total_spots, 1) # Printing total spaces in line 1
                display.lcd_display_string("Spot A empty", 2) 
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
            servo1.stop() # Servo is stopped after the spaces are full

while True: #using while loop for continuous monitoring
    try:
        entry_dooropen() #calling entry door function
        exit_dooropen() #calling exit door function
        spot_sensor1() #calling IR sensor function for spot A
        spot_sensor2() #calling IR sensor function for spot B
        spot_sensor3() #calling IR sensor function for spot C
        spot_sensor4() #calling IR sensor function for spot D
    except KeyboardInterrupt: # When user inturrupts the system by pressing Ctrl-C
        print("System Interruped by user!") #Priting system interruped
        servo1.stop() # Stopping servo
        GPIO.cleanup() #Cleaning up GPIO pins
        sys.exit() #Exiting from the shell

            

        

