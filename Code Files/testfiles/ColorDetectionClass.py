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
    gy=gx=ry=rx=-1

    #Ignore the warning message

    #Set pin mode
    def __init__(self,e,t):
        self.camera.brightness=e
        self.camera.awb_mode=t

    def getcoor(self):
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
            hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

            # Set range for red color and 
            # define mask 
            red_lower = np.array([120, 60, 60], np.uint8) 
            red_upper = np.array([141, 255, 255], np.uint8) 
            red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

            # Set range for green color and 
            # define mask 
            
            green_lower = np.array([38, 65, 50], np.uint8) 
            green_upper = np.array([61, 195, 195], np.uint8) 
            green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 

            
            
            # Morphological Transform, Dilation 
            # for each color and bitwise_and operator 
            # between imageFrame and mask determines 
            # to detect only that particular color 
            kernal = np.ones((5, 5), "uint8") 
            
            # For red color 
            red_mask = cv2.dilate(red_mask, kernal) 
            res_red = cv2.bitwise_and(imageFrame, imageFrame, 
                                    mask = red_mask) 
            
            # For green color 
            green_mask = cv2.dilate(green_mask, kernal) 
            res_green = cv2.bitwise_and(imageFrame, imageFrame, 
                                        mask = green_mask) 
            
            

            # Creating contour to track red color 
            contours, hierarchy = cv2.findContours(red_mask, 
                                                cv2.RETR_TREE, 
                                                cv2.CHAIN_APPROX_SIMPLE) 
            
            for pic, contour in enumerate(contours): 
                area = cv2.contourArea(contour) 
                if(area > 13000): 
                    self.rx, self.ry, w, h = cv2.boundingRect(contour)


            # Creating contour to track green color 
            contours, hierarchy = cv2.findContours(green_mask, 
                                                cv2.RETR_TREE, 
                                                cv2.CHAIN_APPROX_SIMPLE) 
            
            for pic, contour in enumerate(contours): 
                area = cv2.contourArea(contour) 
                if(area > 13000): 
                    self.gx, self.gy, w, h = cv2.boundingRect(contour)



            rx=self.rx 
            ry=self.ry
            gy=self.gy
            gx=self.gx
            self.rx=self.ry=self.gy=self.gx=-1

            return rx,ry,gx,gy     
       
