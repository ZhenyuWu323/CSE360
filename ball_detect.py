# Untitled - By: WUzy2 - Fri Mar 29 2024

import pyb # Import module for board related functions
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
import time # Import module for tracking elapsed time
import math

sensor.reset() # Resets the sensor
sensor.set_pixformat(sensor.RGB565) # Sets the sensor to RGB
sensor.set_framesize(sensor.QVGA) # Sets the resolution to 320x240 px
sensor.set_vflip(True) # Flips the image vertically
sensor.set_hmirror(True) # Mirrors the image horizontally
sensor.skip_frames(time = 2000) # Skip some frames to let the image stabilize

# Define the min/max LAB values we're looking for
target = (14, 95, -35, 127, 29, 75)

ledRed = pyb.LED(1) # Initiates the red led
ledGreen = pyb.LED(2) # Initiates the green led

clock = time.clock() # Instantiates a clock object

#milimeter
actual_diameter = 63.4492
focal_len = 2.2
px_per_mm = 0.00175

#Px
u_0 = 320/2
v_0 = 240/2

#Degree
view_angle = 80

while(True):
    clock.tick() # Advances the clock
    img = sensor.snapshot() # Takes a snapshot and saves it in memory

    # Find blobs with a minimal area of 50x50 = 2500 px
    # Overlapping blobs will be merged
    blobs = img.find_blobs([target], area_threshold=2500, merge=True)

    # Draw blobs
    for blob in blobs:
        print("++++++++++++++++++++++++++++++++++++++++++++++++++")
        # Draw a rectangle where the blob was found
        img.draw_rectangle(blob.rect(), color=(0,255,0))
        # Draw a cross in the middle of the blob
        img.draw_cross(blob.cx(), blob.cy(), color=(0,255,0))
        print("Center of blob: u: ",blob.cx())
        print("Center of blob: v: ",blob.cy())
        blob_radius = max(blob.w(), blob.h()) / 2
        blob_size = math.pi * (blob_radius ** 2)
        print("Blob size (area): ", blob_size)
        #Calculate Distance
        distance = ((actual_diameter * focal_len)/ (blob_radius * 2 * px_per_mm))
        print("Distance: ", distance)

        #Calculate Angle
        dx = blob.cx() - u_0
        angle = (dx / u_0) * (view_angle / 2)
        print("Angle: ", angle)



        print("++++++++++++++++++++++++++++++++++++++++++++++++++")
        print()


    # Turn on green LED if a blob was found
    if len(blobs) > 0:
        ledGreen.on()
        ledRed.off()
    else:
    # Turn the red LED on if no blob was found
        ledGreen.off()
        ledRed.on()

    pyb.delay(50) # Pauses the execution for 50ms
    #print(clock.fps()) # Prints the framerate to the serial console
