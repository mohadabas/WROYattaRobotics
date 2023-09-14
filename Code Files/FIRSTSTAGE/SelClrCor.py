import numpy as np 
import cv2 
from picamera.array import PiRGBArray
from picamera import PiCamera
import time





class ColorsCoordinations:
    camera = PiCamera()
    camera.brightness = 60
    camera.awb_mode = 'auto'
    camera.resolution = (1008, 400)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(1008, 400))
    # allow the camera to warmup
    time.sleep(0.1)
    x=y=w=h=-1

    #Ignore the warning message

    #Set pin mode
    def __init__(self,e,t):
        self.camera.brightness=e
        self.camera.awb_mode=t

    def getcoor(self,l1,l2,l3,u1,u2,u3):
        for frame in self.camera.capture_continuous(self.rawCapture, format="rgb", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            imageFrame = frame.array
            
            # show the frame
            key = cv2.waitKey(1) & 0xFF
            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

            # Convert the imageFrame in 
            # BGR(RGB color space) to 
            # HSV(hue-saturation-value) 
            # color space
            imageFrame=imageFrame[0:400,300:700]

            hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

            # Set range for red color and 
            # define mask 
            lower = np.array([l1, l2, l3], np.uint8) 
            upper = np.array([u1, u2, u3], np.uint8) 
            mask = cv2.inRange(hsvFrame, lower, upper) 

            # Set range for green color and 
            # define mask 
            

            
            
            # Morphological Transform, Dilation 
            # for each color and bitwise_and operator 
            # between imageFrame and mask determines 
            # to detect only that particular color 
            kernal = np.ones((5, 5), "uint8") 
            
            # For red color 
            mask = cv2.dilate(mask, kernal) 
            red = cv2.bitwise_and(imageFrame, imageFrame, 
                                    mask = mask) 
            

            

            # Creating contour to track red color 
            contours, hierarchy = cv2.findContours(mask, 
                                                cv2.RETR_TREE, 
                                                cv2.CHAIN_APPROX_SIMPLE) 
            
            for pic, contour in enumerate(contours): 
                area = cv2.contourArea(contour) 
                if(area > 13000): 
                    self.x, self.y, w, h = cv2.boundingRect(contour)


            # Creating contour to track green color 
            contours, hierarchy = cv2.findContours(mask, 
                                                cv2.RETR_TREE, 
                                                cv2.CHAIN_APPROX_SIMPLE) 
        
            x=self.x 
            y=self.y

            self.x=self.y=-1

            return x,y    
       

