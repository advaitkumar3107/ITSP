import cv2
import numpy as np
import math

kernel = np.ones((5,5), np.uint8)

img = cv2.imread("ac281d65-09dc-4a6f-8ea0-1a3591b9b7d7.jpg")
img2 = img.copy()
img3 = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret1, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Otsu's threshold gives better result compared to simple binary.
erode = cv2.erode(otsu, kernel, iterations = 1)
#We have obtained a binary image with white lines between paraghraphs, large font letters and over some portions of images.

#We use probabilistic Hough transform to detect white lines between paraghraphs. Large images and other whitespaces contribute as 'noise'.
board1 = np.zeros(erode.shape, np.uint8)
lines = cv2.HoughLinesP(erode, 1, np.pi/180, int(min(erode.shape)/10), minLineLength = int(min(erode.shape)/10), maxLineGap = 5)
for line in lines: # 335 lines
	x1,y1,x2,y2 = line[0]
	cv2.line(img, (x1,y1), (x2,y2), (0, 0, 255), 1)	#To see where have lines been detected.
	cv2.line(board1, (x1,y1), (x2,y2), 255, 1)
close1 = cv2.morphologyEx(board1, cv2.MORPH_CLOSE, kernel)	#Several lines close to each other are merged into one band.

'''
Repeating the above process again with one parameter changed helps eliminate noise at all places except near large images
Lines obtained in the following code are drawn extended till the edges.
'''
i = 0
board2 = np.zeros(erode.shape, np.uint8)
lines = cv2.HoughLinesP(board1, 1, np.pi/180, int(min(erode.shape)/10), minLineLength = int(min(erode.shape)/3), maxLineGap = 5)
for line in lines: # 56 lines
	i+=1
	x1,y1,x2,y2 = line[0]
	theta = math.atan2(y2-y1, x2-x1)
	sin = math.sin(theta)
	cos = math.cos(theta)
	x1+=int(1000*cos)
	y1+=int(1000*sin)
	x2-=int(1000*cos)
	y2-=int(1000*sin)
	cv2.line(img2, (x1,y1), (x2,y2), (0, 0, 255), 1)	#To see where have lines been detected and drawn
	cv2.line(board2, (x1,y1), (x2,y2), 255, 1)	#This drawing on a black background wmight be required in later operations like finding contours.
close2 = cv2.morphologyEx(board2, cv2.MORPH_CLOSE, kernel)	#Several lines close to each other are merged into one band.
print(i)

#Printing intermediate results which we want to analyze.
cv2.namedWindow("Board1", cv2.WINDOW_NORMAL)
cv2.imshow("Board1", img)
cv2.namedWindow("Closed 1", cv2.WINDOW_NORMAL)
cv2.imshow("Closed 1", close1)
cv2.namedWindow("Board2", cv2.WINDOW_NORMAL)
cv2.imshow("Board2", img2)
cv2.namedWindow("Closed 2", cv2.WINDOW_NORMAL)
cv2.imshow("Closed 2", close2)

#Respond, only when escape key is pressed, by closing all output windows.
while True:
	k = cv2.waitKey(0)
	if k==27:		#esc
		cv2.destroyAllWindows()
		exit()