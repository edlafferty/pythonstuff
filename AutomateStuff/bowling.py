# Take bowling scores as input and display as properly formatted bowling notation

scoreList = []
frameStr = ""

scores = input("What are your scores? Please enter as one long string: ")
print(scores)
cleanScores = ' '.join(scores.split())
print(cleanScores)
scoreList = list(reversed((cleanScores.split(" "))))

def processFrame(frame, ball1, ball2):
    frameStr = ""
    print(str(frame) + ": " + str(ball1) + ": " + str(ball2) + ":")
    if frame != 10:
        if int(ball1) == 10:
            frameStr = "X "
        elif int(ball1) == 0:
            ball1 = "-"
            if int(ball2) == 10:
                frameStr = "-/"
            else:
                frameStr = "-" + str(ball2) + " "
        elif int(ball2) == 0:
            frameStr = str(ball1) + "- "
        elif int(ball1) + int(ball2) == 10:
            frameStr = str(ball1) + "/ "
        else:
            frameStr = str(ball1) + str(ball2) + " "
    else:
        global scoreList
        ball3 = ""
        if int(ball1) == 10:
            ball1 = "X"
            ball2 = int(scoreList.pop())
        elif int(ball1) == 0:
                ball1 = "-"    
        if int(ball2) == 10:
            ball2 = "X"
        elif int(ball2) == 0:
            ball2 = "-"
        if len(scoreList) > 0:
            ball3 = int(scoreList.pop())
            if int(ball3) == 10:
                ball3 = "X"
            elif int(ball3) == 0:
                ball3 = "-"
        if int(ball2) + int(ball3) == 10:
            ball2 = "/"
            ball3 = ""
        frameStr = str(ball1) + str(ball2) + str(ball3)
    return frameStr

frame = 1
while (frame <= 10):
    ball1 = ""
    ball2 = ""
    ball3 = ""
    ball1 = int(scoreList.pop())
#    print(scoreList)
#    print("Ball 1: " + str(ball1))
    if ball1 < 10:
        ball2 = int(scoreList.pop())
#        print("Ball 2: " + str(ball2))
    frameStr = frameStr + processFrame(frame,ball1,ball2)
    print("Current frames: " + frameStr)
    if len(scoreList) == 0:
        print("Game ended earlier than ten frames.")
        break
    frame += 1