import cv2
import time
import numpy as np

#video codecs compress video data & encode into format that can later be decoded & played back/edited
fourcc = cv2.VideoWriter_fourcc(*"XVID")
output_file = cv2.VideoWriter("output.avi", fourcc, 20.0, (640,480))

#Starting the webcam
cap = cv2.VideoCapture(0)
#Allowing the webcam to start by making the code sleep for 2 seconds
time.sleep(2)

bg = 0
for i in range(60):
    ret,bg = cap.read()
bg = np.flip(bg, axis = 1)

while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    img = np.flip(img, axis = 1)
     #Converting the color from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #Generating mask to detect red colour
    lowerRed = np.array([0,120,50])
    upperRed = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lowerRed, upperRed)
    
    
    lowerRed = np.array([170,120,70])
    upperRed = np.array([180,255,255])
    mask2 = cv2.inRange(hsv, lowerRed, upperRed)

    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones( (3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones( (3,3),np.uint8))
    
    mask2 = cv2.bitwise_not(mask1)

    res1 = cv2.bitwise_and(img, img, mask = mask2)
    res2 = cv2.bitwise_and(bg, bg, mask = mask1)

     #Generating the final output by merging res_1 and res_2
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    output_file.write(final_output)
    #Displaying the output to the user
    cv2.imshow("Magic", final_output)
    cv2.waitKey(1)

cap.release()
output_file.release()
cv2.destroyAllWindows()