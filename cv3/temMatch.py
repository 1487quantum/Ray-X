import cv2
import numpy as np
import imutils

img = cv2.imread('d.jpg')
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)	#Resize by 75%
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = hsv_img[:, :, 0], hsv_img[:, :, 1], hsv_img[:, :, 2]

img_gray=v

template = cv2.imread('tm1.jpg',0)
template = cv2.resize(template, (0,0), fx=0.5, fy=0.5)	#Resize by 75%
template = cv2.Canny(template, 50, 200)
cv2.imshow("eiwrh",template)
w, h = template.shape[::-1]

found = None

# loop over the scales of the image
for scale in np.linspace(0.2, 1.0, 20)[::-1]:
	# resize the image according to the scale, and keep track
	# of the ratio of the resizing
	resized = imutils.resize(img_gray, width = int(img_gray.shape[1] * scale))
	r = img_gray.shape[1] / float(resized.shape[1])
 
	# if the resized image is smaller than the template, then break
	# from the loop
	if resized.shape[0] < h or resized.shape[1] < w:
		break

	# detect edges in the resized, grayscale image and apply template
	# matching to find the template in the image
	edged = cv2.Canny(resized, 80, 200)
	result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
	(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

	# draw a bounding box around the detected region
	clone = np.dstack([edged, edged, edged])
	cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
	(maxLoc[0] + w, maxLoc[1] + h), (0, 0, 255), 2)
	cv2.imshow("Visualize", clone)
	cv2.waitKey(0)
 
	# if we have found a new maximum correlation value, then ipdate
	# the bookkeeping variable
	if found is None or maxVal > found[0]:
		found = (maxVal, maxLoc, r)

# unpack the bookkeeping varaible and compute the (x, y) coordinates
# of the bounding box based on the resized ratio
(_, maxLoc, r) = found
(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
(endX, endY) = (int((maxLoc[0] + w) * r), int((maxLoc[1] + h) * r))
 
# draw a bounding box around the detected result and display the image
cv2.rectangle(img, (startX, startY), (endX, endY), (0, 0, 255), 2)
cv2.imshow("Image", img)
cv2.waitKey(0)

'''
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
cv2.imshow("tt",template)


threshold = 0.5
loc = np.where( res >= threshold)

for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)

#cv2.imshow('Detected',img)
'''
cv2.waitKey(0)
