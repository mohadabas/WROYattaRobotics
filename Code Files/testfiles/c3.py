from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import cv2
import numpy as np
def nothing(x):
    pass
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("test", "frame", 50, 500, nothing)
cv2.createTrackbar("color/gray", "frame", 0, 1, nothing)
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 360, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 360, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 360, nothing)
cv2.createTrackbar("U - H", "Trackbars", 255, 360, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 360, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 360, nothing)
#Loop
while True:
    _, frame1 = cap.read() #Store Video snap in varialble "frame1"
    frame2 = cv2.flip(frame1,-1) # Flip image vertically
    frame2 = cv2.flip(frame1, 0) # flip image vertically
    frame2 = imutils.resize(frame2, width=400)
    hsv_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    blurred_frame = cv2.GaussianBlur(frame1, (5, 5), 0)
#Creat Mask
    low = np.array([l_h,l_s,l_v])
    high = np.array([u_h,u_s,u_v])
    mask = cv2.inRange(hsv_frame2,low,high)
#Contors
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        cv2.drawContours(frame2, contour, -1, (0, 255, 0), 2)
    #Printing frames
    cv2.imshow("IN Frame", frame2)
    cv2.imshow("Masked Image", mask)
#Exit Key        
    key = cv2.waitKey(100)
    if key ==27:
        break
cv2.destroyAllWindows()
cap.release()