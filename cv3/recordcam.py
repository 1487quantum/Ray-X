import cv2

cap = cv2.VideoCapture(0)

'''
use timeout to set time duration for recording
for this script: $ timeout [duration] python recordcam.py
e.g.: $ timeout 30 python recordcam.py     # Record for ~30s
Note: the recording of opencv would be around half the timeout

'''
#Save vid out param
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('test.avi', fourcc, 29, (640, 480),True)      #Out, codec, fps, res, use 3 clr channel bool


# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
   
    #cv2.imshow('Input', frame)
    out.write(frame)
    c = cv2.waitKey(1)
    if c == 27:
        break

out.release()
cap.release()
cv2.destroyAllWindows()
