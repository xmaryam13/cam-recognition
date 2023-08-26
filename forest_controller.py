from controller import Robot
from controller import Keyboard
from controller import DistanceSensor
import random
from controller import Camera

robot = Robot()
keyboard = Keyboard()

timestep = 64

autoMode = True
pic_num=0

wheel1 = robot.getDevice("wheel1")
wheel1.setPosition(float('inf'))
wheel1.setVelocity(0.0)

wheel2 = robot.getDevice("wheel2")
wheel2.setPosition(float('inf'))
wheel2.setVelocity(0.0)

wheel3 = robot.getDevice("wheel3")
wheel3.setPosition(float('inf'))
wheel3.setVelocity(0.0)

wheel4 = robot.getDevice("wheel4")
wheel4.setPosition(float('inf'))
wheel4.setVelocity(0.0)

ds_left = robot.getDevice("ds_left")
ds_right= robot.getDevice("ds_right")

cam= robot.getDevice("camera")
cam.enable(timestep)

#enable camera recognition
cam.recognitionEnable(timestep)


ds_left.enable(timestep)
ds_right.enable(timestep)

speed = 4
number_of_turns = 0

keyboard.enable(timestep)
random_direction = 0

prev_key = 0
key_pressed = -1

while (robot.step(timestep) != -1):
    prev_key = key_pressed
    key_pressed = keyboard.getKey()
    print(key_pressed)
    
    """ code to recognize a sassafras tree. Here, 
    sassafras trees recognition color is green """
    
    if (cam.getRecognitionObjects()):
        first_object = cam.getRecognitionObjects()[0]
        
        color = first_object.getColors()
        red = color[0]
        green = color[1]
        blue = color[2]
        
        if (red == 0 and green == 1 and blue == 0):
            print("Sassafras tree spotted.")
    

    # when you a key, automode variables value is toggled
    if(prev_key == -1  and  key_pressed == 65):
        autoMode = not autoMode

    # press "s" key to take pictures
    if(prev_key == -1  and  key_pressed==83):
        cam.getImage()
        pic_name= "pic"+str(pic_num)+".png"
        cam.saveImage(pic_name,50)
        pic_num=pic_num+1
        
    if(autoMode):      
        ds_left_value = ds_left.getValue()
        ds_right_value = ds_right.getValue()
        
        if(ds_left_value<1000 or ds_right_value<1000):
            number_of_turns = 8
        
        # when turns have not started, we choose a random direction    
        if(number_of_turns == 0):
            random_direction = random.choice([0,1])
         
        if(number_of_turns > 0):
            # In auto mode, turns when an obstacle is detected.
            number_of_turns = number_of_turns - 1
            if(random_direction == 0):
                wheel1.setVelocity(-speed)
                wheel2.setVelocity(speed)
                wheel3.setVelocity(-speed)
                wheel4.setVelocity(speed)
            elif(random_direction == 1):
                wheel1.setVelocity(speed)
                wheel2.setVelocity(-speed)
                wheel3.setVelocity(speed)
                wheel4.setVelocity(-speed)
        else:
            # In auto mode, keeps going forward when no obstacles are detected.
            wheel1.setVelocity(speed)
            wheel2.setVelocity(speed)
            wheel3.setVelocity(speed)
            wheel4.setVelocity(speed)
         
    
    if(not autoMode):
        # front movement - press up arrow key
        if(key_pressed == 315):
            wheel1.setVelocity(speed)
            wheel2.setVelocity(speed)
            wheel3.setVelocity(speed)
            wheel4.setVelocity(speed)
            
        # back movement - press down arrow key   
        if(key_pressed == 317):
            wheel1.setVelocity(-speed)
            wheel2.setVelocity(-speed)
            wheel3.setVelocity(-speed)
            wheel4.setVelocity(-speed)
        
        # left movement - press left arrow key      
        if(key_pressed == 314):
            wheel1.setVelocity(-speed)
            wheel2.setVelocity(speed)
            wheel3.setVelocity(-speed)
            wheel4.setVelocity(speed)
        
        # right movement - press right arrow key     
        if(key_pressed == 316):
            wheel1.setVelocity(speed)
            wheel2.setVelocity(-speed)
            wheel3.setVelocity(speed)
            wheel4.setVelocity(-speed)
        
        # if no key is pressed   
        if(key_pressed == -1):
            wheel1.setVelocity(0)
            wheel2.setVelocity(0)
            wheel3.setVelocity(0)
            wheel4.setVelocity(0)
