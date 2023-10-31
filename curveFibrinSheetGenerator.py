from math import pi, cos, sin,  radians
from tkinter.filedialog import asksaveasfile

def leftThetaStart(thetaList, leftStartTheta, endingTheta, thetaIncrement):
    currentTheta = round(leftStartTheta, 2)
    while(currentTheta > endingTheta):
        thetaList.append(currentTheta)
        currentTheta = round(currentTheta - thetaIncrement,2)
    return thetaList

def rightThetaStart(thetaList, rightStartTheta,endingTheata, thetaIncrement):
    currentTheta = round(rightStartTheta, 2)
    while(currentTheta < endingTheata):
        thetaList.append(currentTheta)
        currentTheta = round(currentTheta + thetaIncrement,2)
    return thetaList

def rodPopulationGenerator(radiusPriorityBoolean, value, totalDegree, rodSpacing, nozzleID):
    if radiusPriorityBoolean == 1:
        radius = value
        arcPerimeter = float((totalDegree/360) * 2 * pi * radius)
        numberOfRods = int(arcPerimeter-nozzleID)/rodSpacing
        
    elif radiusPriorityBoolean == 0:
        arcParameter = value

    return

def arcThetaGenerator(leftTheta, rightTheta, thetaIncrements):

    leftStartTheta  = leftTheta - (thetaIncrements/2)
    rightStartTheta = rightTheta + (thetaIncrements/2)
    thetaArray      = []

    if (leftTheta > 90 > rightTheta):
        #starting from left side
        thetaArray = leftThetaStart(thetaArray, leftStartTheta, 90, thetaIncrements)
        #starting from right side
        thetaArray = rightThetaStart(thetaArray,rightStartTheta, 90, thetaIncrements)
        thetaArray.append(90)

    elif (leftTheta and rightTheta > 90):
        thetaArray = leftThetaStart(thetaArray, leftStartTheta, rightStartTheta, thetaIncrements)
    
    elif (leftTheta and rightTheta < 90):
        thetaArray = rightThetaStart(thetaArray, rightStartTheta, leftStartTheta, thetaIncrements)
        

    #print(thetaArray)

    return thetaArray

def thetaToYZCoordinate(thetaList, arcRadius):
    zyListOTuples = []
    
    for theta in thetaList:
            currentRadian = radians(theta)
            z = round((sin(currentRadian) * arcRadius), 4)
            y = round((cos(currentRadian) * arcRadius), 4)
            zyListOTuples.append((y, z))
    return zyListOTuples

def gcodeGenerator(listOfArcTuples, sheetLength, gCodeMode):
    gCodeList = []
    direction = 1
    

    if(gCodeMode == "G90"):

        gCodeList.append("G90\n")

        for coordinate in listOfArcTuples:
            Y = "Y" + str(coordinate[0])
            Z = "Z" + str(coordinate[1])
            gCode = "G1 " + Y + Z

    elif(gCodeMode == "G91"):

        gCodeList.append("G91\n")

        X = str(sheetLength*direction)

        gCodeList.append("G0"+" Y"+str(listOfArcTuples[0][0])+" Z"+str(listOfArcTuples[0][1])+"\n"+"G1"+" X"+X+"\n")

        for index, coordinateTuple in enumerate(listOfArcTuples):

            if (index < len(listOfArcTuples) - 1):
                
                relativeY = (float(listOfArcTuples[index+1][0]) - float(listOfArcTuples[index][0]))
                relativeZ = (float(listOfArcTuples[index+1][1]) - float(listOfArcTuples[index][1])) 

                relativeY = round(relativeY,4)
                relativeZ = round(relativeZ,4)

                direction*= -1
                X         = str(sheetLength*direction)

                gCodeList.append("G0" + " Y"+str(relativeY)+" Z"+str(relativeZ) +" F50"+"\n"+"G1"+" X"+X+" F300"+"\n")
    else:
        print("gCodeMode is no beuno")

    return gCodeList

def saveGCode(gCodeList):
    file = asksaveasfile(filetypes=[("text file",".txt")],
                        defaultextension=".txt",
                        mode='w')
    if file:
        file.writelines(gCodeList)
    else:
        print("file saving hell")

    return

def main():
    
    leftDegree         = 180 #Degrees in standard cartisian coordiate system
    rightDegree        = 0
    arcLength         = 10 #in mm
    nozzleDiameter    = 0.1 #in mm
    spacingPercentage = 80 #in %
    extrusionAxis     = "C"

    rodCenterSpacing = (spacingPercentage/100) * nozzleDiameter #in mm
    totalDegree       = abs(leftDegree - rightDegree)
    #arcRadius        = arcLength / ((totalDegree/360)*2*pi) # radius = arcLength / [(Degree/360) * 2 * pi]
    numberOfRods     = int((arcLength - nozzleDiameter) / rodCenterSpacing)
    thetaIncrements  = round((totalDegree / numberOfRods),2)

    #print(thetaIncrements)

    thetaList = arcThetaGenerator(leftDegree,rightDegree,thetaIncrements)
    zyList = thetaToYZCoordinate(thetaList, arcRadius)
    
    gCode = gcodeGenerator(zyList, 10, "G91")
    saveGCode(gCode)

    #print(*gCode, sep="\n")

    return

if __name__ == "__main__":
    main()