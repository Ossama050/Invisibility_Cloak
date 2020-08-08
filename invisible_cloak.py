##Import opencv(cv2), Numpy array(numpy) 
import cv2
import time
import numpy as np


# Preparation for writing the ouput video
vid = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('invisibility_cloak.avi',vid,20.0, (640,480))

#capturing the video using webcam
cap = cv2.VideoCapture(0)

#sleep time
time.sleep(3)
count = 0
background = 0

# Capture the background in range of 60
for i in range(60):
    ret,background = cap.read()
background = np.flip(background,axis=1)


# Read every frame from the webcam, until the camera is open
while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    count+=1
    img = np.flip(img,axis=1)
    
    # Convert the color space from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Generate masks to detect blue color
    lower_blue = np.array([0,120,70])
    upper_blue = np.array([9,255,255])
    mask1 = cv2.inRange(hsv,lower_blue,upper_blue)

    lower_blue = np.array([171,120,70])
    upper_blue = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_blue,upper_blue)

    mask1 = mask1+mask2

    # Open and Dilate the mask image to remove noise
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
 
 
    # Create an inverted mask to segment out the blue color from the frame
    mask2 = cv2.bitwise_not(mask1)
 
 
    # Segment the blue color part out of the frame using bitwise and with the inverted mask
    res1 = cv2.bitwise_and(img,img,mask=mask2)

    # Create image showing static background frame pixels only for the masked region
    res2 = cv2.bitwise_and(background, background, mask = mask1)
 
 
    # Generating the final output and writing
    finalOutput = cv2.addWeighted(res1,1,res2,1,0)
    out.write(finalOutput)
    cv2.imshow("invisibility",finalOutput)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()