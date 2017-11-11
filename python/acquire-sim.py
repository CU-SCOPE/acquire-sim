import numpy as np
import cv2
import csv

# Insert string for video or 0 for webcam
#cap = cv2.VideoCapture('../../media/input.avi')
cap = cv2.VideoCapture(0)

##############################################################
# Variables
# videoTime is the time of the actual video in seconds
# cx,cy are the x and y position of the centroid

cx = 0
cy = 0
videoTime = 0

##############################################################
# Parameters for BackgroundSubtractorMOG
# history is the length of the history
# nmixtures is the number of gaussian mixtures
# backgroundRatio is the background ratio
# noiseSigma is the noise strength

history = 30
nmixtures = 7
backgroundRatio = .6
noiseSigma = 12
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(history,nmixtures,backgroundRatio,noiseSigma)

while(1):
    ret, frame = cap.read()

    videoTime = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) / cap.get(cv2.CAP_PROP_FPS)   

    # Apply the BackgroundSubtractorMOG to given frame
    fgmask = fgbg.apply(frame)

    ##############################################################
    # Dilate
    # Increases the size of pixels detected x5 for better contour detection

    fgmask = cv2.dilate(fgmask, None, iterations=5)
    
    ##############################################################
    # Contours
    # Joins all continuous points along boundary having same color or intensity
    # cv2.findContours(source image, contour retrieval mode, contour approximation method)
    # RETR_EXTERNAL used to select only extreme outer contours
    # CHAIN_APPROX_SIMPLE removes redundant boundary points in order to save memory
    
    cnts = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    ##############################################################
    # Centroid
    # With contours, find the centroid with moments
    # cv2.moments(c) generates the moments for the contour
    # M['m00'], M['m10'], and M['m01'] define the centroid
    
    if len(cnts) > 0:
        # Iterate through contours (use max to reduce runtime)
        for c in cnts:
            # Compute the centroid
            M = cv2.moments(c)
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
    
        # Draw contours and centroid
        cv2.drawContours(frame, [c], -1, (0,255,0), 2)
        cv2.circle(frame, (cx,cy), 5, (0, 0, 255), -1)

    ##############################################################
    # File Output
    # Writes a CSV with Centroid locations
    
    with open('centroid.csv', 'ab') as csvfile:
        centroid = csv.writer(csvfile)
        centroid.writerow([videoTime,cx,cy])

    ##############################################################
    # Display Output
    # Shows the output for Background Subtraction and Centroid Location

    cv2.imshow('Background Subtraction',fgmask)  
    cv2.imshow('Centroid Location',frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()   