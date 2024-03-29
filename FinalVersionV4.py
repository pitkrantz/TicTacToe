import cv2
import numpy as np
from time import sleep

print("Starting...")

counter = 0

board = [
    # 0    1    2
    ["/", "/", "/"],    #row 0
    ["/", "/", "/"],    #row 1
    ["/", "/", "/"]     #row 2
]

cap = cv2.VideoCapture(1)
sleep(1.5)

class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.number = 1

def findRealCircles():
    print(realcircles)

def updateBoard():
    print(board)


def cleanInput(threshold = 200):

    if intersections is None:
        pass

    delete = []
    for i in range(1 , len(intersections)):

        if intersections[i - 1][0] - threshold < intersections[i][0] < intersections[i - 1][0] + threshold:
            if intersections[i - 1][1] - threshold < intersections[i][1] < intersections[i - 1][1] + threshold:
                delete.append(intersections[i])

    for element in delete:
        intersections.remove(element)

def deleteDuplicates(inter):
    inter.sort()
    for i in range(1, len(inter)-1):
        if inter[i] == inter[i-1]:
            inter.pop(i)
    
    if inter[0] == inter[1]:
        inter.pop(0)
    return inter

def mousePoints(event, x, y, flags, params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        if counter < 4:
            points[counter][0] = x
            points[counter][1] = y

            counter += 1
        elif counter == 4:
            counter = 0
        else:
            counter = 0

        #print(x,y)

def text(text, offset):
    cv2.putText(frame, str(text), (int(frame.shape[1]/2) - offset,int(frame.shape[0]/2)),cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,0), 5, cv2.LINE_AA)

def caption(active):

    if active:
        cv2.putText(frame, "ACTIVE", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "INACTIVE", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

def findIntersections(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    return x,y

    
#1920x1080 fir emmer 100 vum rand fort ze sinn
points = np.array([[100,100],[1820,100],[1820,980],[100,980]], np.int32)

detectedCircles = 0
frames = 0

wrongcircles = []
realcircles = []

while True:
    CirclesDuringFrame = []

    _, frame  = cap.read()
 
    cv2.setMouseCallback("Frame", mousePoints)

    blank = np.zeros(frame.shape[:2], dtype="uint8")
    polymask = cv2.fillPoly(blank, [points], 255)

    masked = cv2.bitwise_and(frame, frame, mask=polymask)

    for i in range(len(points)):
        if i < 3:
            lines = cv2.line(frame, (points[i][0], points[i][1]), (points[i+1][0], points[i+1][1]), (255, 220, 5), 2)
        else:
            lines = cv2.line(frame, (points[i][0], points[i][1]), (points[0][0], points[0][1]), (255, 220, 5), 2)
        rectangle = cv2.rectangle(frame, (int(points[i][0] - 10), int(points[i][1] - 10)), (int(points[i][0] + 10), int(points[i][1] + 10)), (255, 220, 5), -1)
    
    # Mask preview
    # cv2.imshow("Masked", masked)

    shadow = 40
    light = 100

    # Methode 1°: MASK mat luucht, ganz ofhängeg vun der belichtung

    lowerLimit = (shadow, shadow, shadow)
    upperLimit = (light, light, light)
    mask = cv2.inRange(masked, lowerLimit, upperLimit)

    # Methode 2°: Bessen besser mengen ech wei Methode 1°   !!!!AKTIV!!!!

    grayFrame = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (13, 13), 0)

    if counter == 4:
        caption(True)
        circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.2, 100, param1= 100, param2 = 45, minRadius = 20, maxRadius = 150)

        if circles is not None:
            detectedCircles += 1
            circles = np.uint16(np.around(circles))
            
            #realCircles = 

            for circle in circles[0, :]:
                newcircle = Circle(circle[0], circle[1], circle[2])
                CirclesDuringFrame.append(newcircle)
            

            for i in circles[0, :]:
                cv2.circle(frame, (i[0],i[1]), i[2], (0, 255, 0), 3)

        



        if frames < 10:
            for i in range(0,len(allcircles)):
                if allcircles[i].number < 8:
                    wrongcircles.append(allcircles[i])
                else:
                    realcircles.append(allcircles[i])
            # isCircle = False
            # if detectedCircles >= 8:
            #     isCircle = True
            #     #print(CirclesDuringFrames)
            # frames = 0
            # detectedCircles = 0
            # CirclesDuringFrames = []
            # print(isCircle)

        frames += 1

    else:
        caption(False)

    edges = cv2.Canny(grayFrame, 50, 150, apertureSize=3)

    #lines = cv2.HoughLinesP(edges, 1, np.pi/180, 200, maxLineGap = 100)

    #vertical = []
    #horizontal = []
    #intersections = []

    #if lines is not None:
    #    for line in lines:
    #        x1, y1, x2, y2 = line[0]

    #        if x2- 150 < x1 < x2 + 150:
    #            vertical.append([[x1, y1], [x2, y2]])
    #            cv2.line(frame, (x1, y1), (x2, y2), (255,0,0), 3)
    #        else:
    #            horizontal.append([[x1, y1], [x2, y2]])
    #            cv2.line(frame, (x1, y1), (x2, y2), (0,0,255), 3)
    
    #for i in range(len(vertical)):
    #    for j in range(len(horizontal)):
    #        #first start and endpoint
    #        A = vertical[i][0]
    #        B = vertical[i][1]
    #        #last start and endpoint
    #        C = horizontal[j][0]
    #        D = horizontal[j][1]

    #        try: 
    #            intersectionx, intersectiony = findIntersections((A,B),(C,D))
    #            intersections.append([int(intersectionx), int(intersectiony)])

    #        except:
    #            pass
    
    # sort array based on second element
    # array.sort(key=lambda x:x[1])
    
    #cleanInput(100)
        #intersections = deleteDuplicates(intersections)
        #intersections = simpleTest.CleanIntersections()
        #intersections = simpleTest.simplify()
    
    #print(intersections)
    #print("""

    
   #""")
    #for intersection in intersections:
    #    circle = cv2.circle(frame, (int(intersection[0]), int(intersection[1])), 10, (0,255,0), -1)

    #cv2.line(frame, (100,100), (200, 100), (215,66,245), 1)

    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()