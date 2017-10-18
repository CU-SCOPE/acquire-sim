import numpy as np
import cv2
from collections import deque
import csv

time_thresh = 0.5;

#insert string for video or 0 for webcam
cap = cv2.VideoCapture('input.avi')

#initialize cx and cy for displaying centroid
cy = 0
cx = 0

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

#declare parameters for background subtractor
history = 30
nGauss = 7
bgThresh = .1
noise = 2
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(history,nGauss,bgThresh,noise)

pts = deque(maxlen=32)

outvid = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (int(cap.get(3)),int(cap.get(4))))

while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    try:
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    except:
        print "error with morphology"    
    
    fgmask = cv2.dilate(fgmask, None, iterations=2)

    cnts = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if(int(M["m00"]) != 0):
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    pts.appendleft(center)

    # loop over the set of tracked points
    for i in xrange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(32 / float(i + 1)) * 2.5)
        #cv2.line(fgmask, pts[i - 1], pts[i], (0, 0, 255), thickness)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    lengthfps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    currentframe = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    fps = cap.get(cv2.CAP_PROP_FPS)
    videotime = currentframe / fps

    cy = int(cap.get(4))-cy
    cv2.putText(frame, str(videotime) + " Centroid: (" + str(cx) + ", " + str(cy) + ")", (10, 510), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    

    if(videotime > time_thresh):
        with open('centroid.csv', 'ab') as csvfile:
            centroid = csv.writer(csvfile)
            centroid.writerow([time_thresh,cx,cy])
        time_thresh+=0.5
    
    # Write the frame into the file 'output.avi'
    outvid.write(frame)

    cv2.imshow('Centroid Location',frame)
    cv2.imshow('Background Subtraction',fgmask)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
outvid.release()
cv2.destroyAllWindows()

