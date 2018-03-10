import numpy as np
import cv2
import math

#cap = cv2.VideoCapture('s.mp4')
cap = cv2.VideoCapture(0)
#Vid
vidScale = 0.5      #Img scale ratio
roiS = 0.25         #ROI start (x-axis)
roiE = 0.75         #ROI end (x-axis)

#Viz
vizClr = (255,255,255)
#Target cross param
cl = 10             #Cross length
crts = 0.5          #Cross ratio to image size

#Centre of gate
gc = 0

#List of Steer
lstS = []
d=0         #Counter for lstS

#Save vid out param
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#out = cv2.VideoWriter('test.avi', fourcc, 10, (640, 360),True)      #Out, codec, fps, res, use 3 clr channel bool

def main():
    while 1:
        ret, img = cap.read()
        img = cv2.resize(img, (0,0), fx=vidScale, fy=vidScale)
        height, width = img.shape[:2]			                       #Get Height, width of img

        #Set ROI start end loc
        rS = int(roiS*width)
        rE = int(roiE*width)

        #Set target cross w & h
        cw = int(crts*width)
        ch = int(crts*height)

        #Set the center of gate to be in the middle initially/if all fails
        gc=int(width/2)

        #Change to HSV colorspace
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)

        #Visualisation
        #Draw line overlay boundary for visualisation
        cv2.line(img, (rS, int(height/3)), (rS, int(2*height/3)), vizClr, 2, cv2.LINE_AA)		#x1,y1,x2,y2
        cv2.line(img, (rE, int(height/3)), (rE, int(2*height/3)), vizClr, 2, cv2.LINE_AA)
        #Target Cross
        cv2.line(img, (cw, ch-cl), (cw, ch+cl), vizClr, 1, cv2.LINE_AA)
        cv2.line(img, (cw-cl, ch), (cw+cl, ch), vizClr, 1, cv2.LINE_AA)

        #Make another copy of img
        imgDebug=img.copy()

        #Set ROI: roi = gray[y1:y2, x1:x2]
        vr = v[0:height,rS:rE]

        # noise removal
        kernelN = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(vr,cv2.MORPH_OPEN,kernelN, iterations = 4)

        #Erode and Enhance side bars (Emphasis kernel more on y-axis)
        kernelS = np.ones((3,9), np.uint8)
        img_es = cv2.erode(opening, kernelS, iterations=6)
        #Median Blur to ensure connectivity
        img_esB = cv2.medianBlur(img_es,15)
        #Upper range threshold: Set value above 170 to 0 (Used lightness value via imshow of dilated img to determine cutoff)
        th0, img_esBT = cv2.threshold(img_esB, 170, 0, cv2.THRESH_TRUNC)
        #cv2.imshow("UpperT",img_esBT)
        #Dilate img
        kernelD = np.ones((7,7), np.uint8)
        img_esBTD = cv2.dilate(img_esBT, kernelD, iterations=7)
        #cv2.imshow("Dilate",img_esBTD)

        #Now let's make it Binary: Binary thresholding (Set val below thres to max value)
        th1, img_esBTD = cv2.threshold(img_esBTD, 165, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        #cv2.imshow('Bin',img_esBTD)

        #Erode again
        kernelD = np.ones((1,1), np.uint8)
        img_esBTDe = cv2.erode(img_esBTD, kernelD, iterations=2)
        #cv2.imshow('Erode2',img_esBTDe)

        _, contours, _ = cv2.findContours(img_esBTDe,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        ctrList=[None]*len(contours)        #Initialise with NoneType, Get list of center loc of only X-axis
        l=0                                 #mntList Tracker
        for k, c in enumerate(contours):
            area = cv2.contourArea(c)

            if (area > 700)and(area < 20000):
                # compute the center of the contour
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                ctrList[l]=cX

                #Debug Image
            	#Draw the contour and center of the shape on the image (+rS to Compensate ROI x-axis offset)
                cv2.drawContours(imgDebug, [c], -1, (255, 0, 0), 2, offset=(rS,0))
                cv2.circle(imgDebug, (rS+cX, cY), 5, vizClr, -1)
                cv2.putText(imgDebug, "Center", (rS+cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, vizClr, 1)
                l+=1

        #ctrList = filter(lambda x: x is not None, ctrList) 
        ctrList = [x for x in ctrList if x is not None]  #Remove nonetype
        #print(ctrList)
        #Check whether point is within ROI
        for z in ctrList:
            if not((rS+cX>rS)and(rS+cX<rE)):
                ctrList.remove(z)
        #print ctrList
        #print(ctrList)
        if len(ctrList)>1:
            gc=sum(ctrList)/len(ctrList)
        elif len(ctrList)!=0:
            gc=ctrList[0]

        if not ctrList: #If empty
            gc=width/2-rS #Remove double offset

        #print gc
        lstS.append(gc)                                        #Add to list to calculate moving average of steer to use
        #Take moving average of 10 value to smooth gate centre
        tmpAvg = running_mean(lstS,10)
        if len(tmpAvg)>0:
            mavg = int(tmpAvg[len(tmpAvg)-1])
        else:
            mavg=int(width/2)
        #Motion strength (Range: +/-0<->100), Right-> blue, left -> red
        #Raw
        diffRC =width/2-(rS+gc)                                    #Diff from center & target
        diffRR = int(100*(float(diffRC)/((rS-rE)/2)))               #Get strength ratio to be applied
        #Smooth
        diffSC =width/2-(rS+mavg)                                    #Diff from center & target
        diffSR = int(100*(float(diffSC)/((rS-rE)/2)))               #Get strength ratio to be applied

        #Viz
        #Draw smooth target line (Have to compensate for ROI x-axis offset)
        cv2.line(img, (rS+mavg, int(height/3)), (rS+mavg, int(2*height/3)), (100, 255, 0), 2, cv2.LINE_AA)		#x1,y1,x2,y2
        cv2.putText(img, "Steer: "+str(diffSR), (rS, 70+int(2*height/3)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, vizClr, 1)  #Show smoothed target as final
        #print diffR
        #Draw gauge below
        if (diffSC>0):   #Right
            cv2.line(img, (int(rS+mavg), 20+int(2*height/3)), (int(width/2), 20+int(2*height/3)), (0, 0, 255), 3, cv2.LINE_AA)		    #x1,y1,x2,y2
        else:           #Left
            cv2.line(img, (int(rS+mavg), 20+int(2*height/3)), (int(width/2), 20+int(2*height/3)), (255, 0, 0), 3, cv2.LINE_AA)		    #x1,y1,x2,y2

        #For Debug
        cv2.putText(imgDebug, "Steer (R): "+str(diffRR), (rS, 40+int(2*height/3)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, vizClr, 1)
        cv2.putText(imgDebug, "Steer (S): "+str(diffSR), (rS, 70+int(2*height/3)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, vizClr, 1)

        #Target line
        #Draw raw target line (Have to compensate for ROI x-axis offset)
        cv2.line(imgDebug, (int(rS+gc), int(height/3)), (int(rS+gc), int(2*height/3)), (0, 100, 255), 2, cv2.LINE_AA)		#x1,y1,x2,y2
        cv2.putText(imgDebug, "T-Raw", (int(rS+gc) - 20, int(height/3) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, vizClr, 1)
        #Draw smooth target line (Have to compensate for ROI x-axis offset)
        cv2.line(imgDebug, (rS+mavg, int(height/3)), (rS+mavg, int(2*height/3)), (100, 255, 0), 2, cv2.LINE_AA)		#x1,y1,x2,y2
        cv2.putText(imgDebug, "T-Smooth", (rS+mavg - 20, int(2*height/3) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, vizClr, 1)


        #print ctrList,gc

        mavgOut = int((diffSR+100)/22)
        print(mavgOut)
            

        #cv2.imshow('Main',img)
        #cv2.imshow('Debug',imgDebug)
        cv2.imwrite("/home/odroid/Desktop/q.jpg",imgDebug)
        #out.write(imgDebug)              #Save main img frame
        #cv2.imshow('Edges',edges)
        #sfc = cv2.waitKey(0)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)

if __name__ == "__main__":
    main()

