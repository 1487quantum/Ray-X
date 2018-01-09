import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# CLAHE (Contrast Limited Adaptive Histogram Equalization)
# https://en.wikipedia.org/wiki/Adaptive_histogram_equalization#Contrast_Limited_AHE
clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8,8))

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame)
    
    #Sharpen image by increasing contrast
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)                  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)                                      # split on 3 different channels

    l2 = clahe.apply(l)                                           # apply CLAHE to the L-channel

    lab = cv2.merge((l2,a,b))                                     # merge channels
    img2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)                   # Convert back to bgr
    img2 =cv2.fastNlMeansDenoisingColored(img2,None,10,10,7,21)   # Image Denoising (https://docs.opencv.org/trunk/d5/d69/tutorial_py_non_local_means.html)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV) 
    # lower mask (0-10) of RED
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)
    # upper mask (170-180) of RED
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    # join the masks
    mask = mask0 + mask1
    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)  
    # apply the mask
    output = cv2.bitwise_and(frame, frame, mask = mask)
    median = cv2.medianBlur(output,15)
    # show the images
    cv2.imshow("images", np.hstack([frame, img2, output, median]))

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
