import cv2
import time
import numpy as np

#Save output in file output.avi
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))


#Start Webcam
cap = cv2.VideoCapture(0)

#Pause Code for 2 seconds
time.sleep(2)

bg=0

#Capturing video
for i in range(60):
    ret, bg = cap.read()

#Flipping background
bg = np.flip(bg, axis = 1)

#Read frame until camera is open
while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break

    #Flipping image
    img = np.flip(img, axis = 1)

    #Converting the color from rgb to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Generating mask to detect black colour
    #mask 1
    lower_black = np.array([30,30,0])
    upper_black = np.array([104,153,70])
    mask_1 = cv2.inRange(hsv, lower_black, upper_black)
    #mask 2
    lower_black = np.array([30,30,0])
    upper_black = np.array([104,153,70])
    mask_2 = cv2.inRange(hsv, lower_black, upper_black)
    #merge
    mask_1 = mask_1 + mask_2

    #open and expand the image where there is black color in mask 1
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))

    #selecting only the part that does not have mask 1 and saving in mask 2
    mask_2 = cv2.bitwise_not(mask_1)
    
    #Keeping the part of image without black colour
    res_1 = cv2.bitwise_and(img, img, mask = mask_2)

    #Keeping the part of image with black colour
    res_2 = cv2.bitwise_and(bg, bg, mask = mask_1)

    #Generating final output
    final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)
    output_file.write(final_output)
    cv2.imshow("magixx", final_output)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()