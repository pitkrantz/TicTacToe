import serial
import multiprocessing
import ctypes
from time import sleep
from math import sqrt

#really M4S(degree) but 90 is 180 haven't changed that yet
#PIN 11
#!!!!!!! M4 S100 -> HIGH
# M5 -> LOW

board = [
    # 0    1    2
    ["/", "/", "/"],    #row 0
    ["/", "/", "/"],    #row 1
    ["/", "/", "/"]     #row 2
]
# array with center points of all squares in order to know how to draw everything
boardcoords = [
    [[0,0], [0,0], [0,0]],
    [[0,0], [0,0], [0,0]],
    [[0,0], [0,0], [0,0]]
]

InstructionsArr = []

# myArray = multiprocessing.Array(ctypes.c_wchar_p, [""])

diagonal = 420
# squareLength = diagonal/sqrt(2)
squareLength = 297
# this approach uses a temporary gcode file, which might not be the best for your harddrive (SSD) 
# so I might implement a version where you just save them in a long string or an array or something stored in memory -> done is used right now
# robotPort = "/dev/cu.usbserial-A10JYZY0" i don't know when this port was used but I'm keeping it here so I have it stored 
# robotPort = "/dev/tty.usbmodem212301"
# robotPort = "/dev/tty.usbmodem212101"
# robotPort = "/dev/tty.usbmodem112301"
ports = ["/dev/tty.usbmodem212301", "/dev/tty.usbmodem212101", "/dev/tty.usbmodem112301"]
# robotPort = "/dev/tty.usbmodem212301"

def getPort():
    for port in ports:
        try:
             print("Checking port " + port)
             connectedPort = serial.Serial(port, 115200)
             print("The correct port is " + port)
             return connectedPort
        except Exception as e:
             print(e)
             pass
    
    print("Serial Error")
        
# Idea --> use an object for the bot functions to keep everything sorted well 
# class Bot:
#     def __init__(self, symbol):
#         self.symbol = symbol
#     def minimax(self)

class SerialManager:
    def __init__(self):
        # self.ser = serial.Serial(robotPort, 115200)
        self.ser = getPort()
        sleep(1)
        response = self.ser.readline()
        if response == b"\r\n":
            response = self.ser.readline()
        print(response)
        print("Connected")
        # self.ser.write(b'G28 \r\n')
        # output = self.ser.readline()
        # if output == b"ok\r\n":
        #     print("ok") 
        #     pass
        # else:
        #     print("Error")
        #     return
    
    def executeArr(self):
        global InstructionsArr
        #I think I will use this method in order to not put to much strain on the SSd by creating and deleting files + speed
        array = InstructionsArr
        print("executing")
        i = 0
        for line in array:
            print(line)
            # if line(0) == "S":
            #     sleep(int(line.strip("S")))
            self.ser.write(bytes(line, "utf-8"))
            output = self.ser.readline()
            print(output)
            i += 1
            print("Line number: " + str(i))
            # sleep(0.1)
        print("done")
        InstructionsArr = []


        # I'm now implementing a custom sleep function because G4 makes problems
        # so I will parse the lines and make sure the first letter isn't M nor G nor $
        # and create S for sleep followed by an int in seconds the waittime which should be done
        # This will be used to tell the robot how long it should wait for the pen to switch states, which still has to be mesured when the hardware is done.



        #!!!!! Always close a file before reading it somewhere else, because this saves the acutal data
    # def executeFile(self):
    #     currentFile = open("Instructions.gcode", "r")
    #     instructions = currentFile.readlines()

    #     print("file is being read")
    #     print(len(instructions))
    #     #print(instructions)
    #     #print(bytes(instructions[2], "utf-8"))
    #     for i in range(0, (len(instructions))):
    #         print(i)
    #         print(bytes(instructions[i], "utf-8"))
    #         self.ser.write(bytes(instructions[i], "utf-8"))
    #         output = self.ser.readline()
    #         if output == b"ok\r\n":
    #             print("ok")
    #         else:
    #             print(output)     
    #         sleep(0.2) 

        
        # print("deleting file")
        # os.remove("Instructions.gcode")
    
    def closeSerial(self):
        self.ser.close()

class GcodeGenerator:
    
    def lineTest(self):
        global InstructionsArr
        # file = open("Instructions.gcode", "w")
        InstructionsArr.append("G0 X100 Y100\r\n") # move the pen of to the middle a bit
        InstructionsArr.append("M4 S100\r\n") #pen down
        # InstructionsArr.append("G4 P1000\r\n")
        
        
        
        # own instruction to add delay  might have to use other letter rather than S
        # InstructionsArr.append("S1\r\n")



#### !!!!!! The F with the G1 command is used for the feed rate, which I think has to be specified for it to work -> otherwise error, unknown feed rate

        InstructionsArr.append("G1 X20 F3000\r\n")
        InstructionsArr.append("G1 Y20 F3000\r\n")
        InstructionsArr.append("M5\r\n")
        # print("Testline File created")
        # file.close()

    def penDown(self):
        global InstructionsArr
        #print("Starting Pen Down")
        #file = open("Instructions.gcode", "w")
        InstructionsArr.append("M4 S0\r\n") 
        # InstructionsArr.append("G4 P300\r\n")
        # InstructionsArr.append("M4 S0\r\n")
        # InstructionsArr.append("M5\r\n")

    def penUp(self):
        global InstructionsArr
        # InstructionsArr.append("M4 S0\r\n")
        InstructionsArr.append("M4 S90\r\n")
        # InstructionsArr.append("G4 P300\r\n")

    def calibrate(self):
        global InstructionsArr
        print("calibrating...")
        # file = open("Instructions.gcode", "w")
        InstructionsArr.append("G28\r\n")
        # InstructionsArr.append("G0\r\n")
        # print("Calibration File created")
        # file.close() 

    def drawPoint(self, x, y):
        global InstructionsArr
        InstructionsArr.append("G0 X" + str(x) + " Y" + str(y) +"\r\n")
        self.penDown()
        self.penUp()

    def offsetCalibration(self):
        global InstructionsArr
        print("Offset, calibrating")
        self.drawPoint(10, 10)


    def cross(self, row, cloumn): 
        global InstructionsArr

        # will have to look into the coordinates once the hardware is done
        centerPoint = boardcoords[row][cloumn] 

        print("Cross")
        # this function draws a cross starting TL to BR -> BL to TR
        half_squareLength = squareLength/2
        InstructionsArr.append("G0 X" + str(centerPoint[0] - half_squareLength)+ " Y" + str(centerPoint[1] + half_squareLength) + "\r\n")
        InstructionsArr.append("M4 S100\r\n") # set pen down
        InstructionsArr.append("G1 X" + str(centerPoint[0] + (half_squareLength)) + " Y" + str(centerPoint[1] - half_squareLength) + "\r\n")
        InstructionsArr.append("M5\r\n") # lift pen move to lower left corner 
        InstructionsArr.append("G0 X" + str(centerPoint[0] - half_squareLength) + " Y" + str(centerPoint[1] - half_squareLength) + "\r\n")
        InstructionsArr.append("M4 S100\r\n")# set pen down
        InstructionsArr.append("G1 X" + str(centerPoint[0]+ half_squareLength) + " Y" + str(centerPoint[1] + half_squareLength) + "\r\n")
        InstructionsArr.append("M5\r\n") # lift pen up
        InstructionsArr.append("G0 X0 Y0" + "\r\n") 
    
    def drawPlayingField():
        global InstructionsArr
        print("Setting up...")

class player:
    def __init__(self, symbol):
        self.symbol = symbol

ai = player("X") 
human = player("O")

def checkDraw():
    freespaces = 0
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == "/":
                freespaces += 1
    if freespaces == 0 :
        return True
    else:
        return False

def checkWinner():
    if board[0][0] == board[0][1] and board[0][1] == board[0][2] and board[0][2] == "X":
        return "X"
    if board[0][0] == board[0][1] and board[0][1] == board[0][2] and board[0][2] == "O":
        return "O"

    if board[1][0] == board[1][1] and board[1][1] == board[1][2] and board[1][2] == "X":
        return "X"
    if board[1][0] == board[1][1] and board[1][1] == board[1][2] and board[1][2] == "O":
        return "O"
        
    if board[2][0] == board[2][1] and board[2][1] == board[2][2] and board[2][2] == "X":
        return "X"
    if board[2][0] == board[2][1] and board[2][1] == board[2][2] and board[2][2] == "O":
        return "O"

    
    if board[0][0] == board[1][0] and board[1][0] == board[2][0] and board[2][0] == "X":
        return "X"
    if board[0][0] == board[1][0] and board[1][0] == board[2][0] and board[2][0] == "O":
        return "O"

    if board[0][1] == board[1][1] and board[1][1] == board[2][1] and board[2][1] == "X":
        return "X"
    if board[0][1] == board[1][1] and board[1][1] == board[2][1] and board[2][1] == "O":
        return "O"
        
    if board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[2][2] == "X":
        return "X"
    if board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[2][2] == "O":
        return "O"

    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[2][2] == "X":
        return "X"
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[2][2] == "O":
        return "O"

    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[2][0] == "X":
        return "X"
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[2][0] == "O":
        return "O"

    if checkDraw():
        return 0
    return None

def bestMove():
    bestScore = -800
    move = [0, 0]
    for i in range(0,3):
        for j in range(0,3):
            if(board[i][j] == "/"):
                board[i][j] = ai.symbol
                score = minimax(board, False)
                board[i][j] = "/"
                if(score > bestScore):
                    bestScore = score
                    move = [i, j]
                
    board[move[0]][move[1]] = ai.symbol
    return move

def minimax(playingboard, isMaximizing):
    result = checkWinner()
    if result != None:
        if result == ai.symbol:
            return 1
        elif result == human.symbol:
            return -1
        if result == 0:
            return 0
    
    if (isMaximizing):
        bestScore = -800
        for i in range(0,3):
            for j in range(0,3):
                if(playingboard[i][j] == "/"):
                    playingboard[i][j] = ai.symbol
                    score = minimax(playingboard, False)
                    playingboard[i][j] = "/"
                    if (score > bestScore):
                        bestScore = score
        return bestScore

    else:
        bestScore = 800
        for i in range(0,3):
            for j in range(0,3):
                if(playingboard[i][j] == "/"):
                    playingboard[i][j] = human.symbol
                    score = minimax(playingboard, True)
                    playingboard[i][j] = "/"
                    if (score < bestScore):
                        bestScore = score
        return bestScore