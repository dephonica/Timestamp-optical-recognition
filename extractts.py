import os
import sys
import math
import Image
import string

#timestampRoi = (25,32,330,50)
timestampRoi = (35,32,440,50)

symbolsInLine = 19
activeSymbols = (0,1,2,3,5,6,8,9,11,12,14,15,17,18)

currentSymNum = 0
currentTimestamp = ""

####################################################################
preTemplates = []
preTemplatesMap = []

def loadTemplates():
    with open("dict.txt") as dictFile:
        content = dictFile.readlines()

    for i in range(len(content)):
        items = string.split(content[i], "=")
        values = string.split(items[1], "-")

        for j in range(len(values)):
            value = values[j]

            nums = string.split(value, ",")
            numList = []
            for k in range(len(nums)):
                numList.append(int(nums[k]))

            preTemplatesMap.append(items[0])
            preTemplates.append(numList)

####################################################################
def matchSymbol(template):

    if (len(template) == 0):
        return (-100,-100)

    global preTemplates
    global preTemplatesMap

    weights = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for i in range(len(preTemplates)):
        for n in range(len(preTemplates[i])):
            if (preTemplates[i][n] in template):
                weights[i] = weights[i] + 1
            else:
                weights[i] = weights[i] - 1

    maxValue = max(weights)
    maxIndex = weights.index(maxValue)

    resultChar = -1;
    try:
        if maxIndex < len(preTemplatesMap):
            resultChar = preTemplatesMap[maxIndex]
    except:
        print "Index", maxIndex, "in", preTemplatesMap

    return (resultChar, maxValue)

##########################################################################

def thresholdImage(img, target, threshold):

    symWidth, symHeight = img.size

    pix = img.load()

    symLeft = 100
    symRight = 0
    symTop = 100
    symBottom = 0

    for y in range(symHeight):
        for x in range(symWidth):
            r, g, b = pix[x,y]

            dist = math.sqrt(math.pow(r - target[0], 2) + math.pow(g - target[1], 2) + math.pow(b - target[2], 2))

            if (dist > threshold):
                pix[x,y] = (0,0,0)
            else:
                pix[x,y] = (255,255,255)

                if (x < symLeft): 
                    symLeft = x

                if (x > symRight):
                    symRight = x

                if (y < symTop):
                    symTop = y

                if (y > symBottom):
                    symBottom = y

    return (symLeft, symTop, symRight, symBottom)

####################################################################

def getTemplate(imSym, target, threshold):

    symLeft, symTop, symRight, symBottom = thresholdImage(imSym, target, threshold)

    symRealWidth = (symRight - symLeft)
    symRealHeight = (symBottom - symTop)

    pix = imSym.load()

    template = []

    #print "real width:", symRealWidth, ", height:", symRealHeight

    if (symRealWidth > 3) and (symRealHeight > 3):

        # Draw 7 detection points
        detectPoints = ((symLeft + symRealWidth / 2, symTop), 
            (symLeft + symRealWidth / 2, 1 + symTop + symRealHeight / 4),
            (symLeft + symRealWidth / 2, symTop + symRealHeight / 2),
            (symLeft + symRealWidth / 2, symBottom - 1 - symRealHeight / 4),
            (symLeft + symRealWidth / 2, symTop + symRealHeight),
            (symLeft, 1 + symTop + symRealHeight / 4),
            (symLeft, symTop + symRealHeight / 2),
            (symLeft, symBottom - 1 - symRealHeight / 4),
            (symRight, 1 + symTop + symRealHeight / 4),
            (symRight, symTop + symRealHeight / 2),
            (symRight, symBottom - 1 - symRealHeight / 4),
            (symLeft, symTop),
            (symLeft, symBottom),
            (symRight, symTop),
            (symRight, symBottom))

        for p in range(15):
            x,y = detectPoints[p]

            isSet = 0

            for sy in range(-1,1):
                for sx in range(-1,1):
                    px = x + sx
                    py = y + sy

                    if (px < 0):
                        px = 0
                    if (px >= symRealWidth):
                        px = symRealWidth - 1
                    if (py < 0):
                        py = 0
                    if (py > symRealHeight):
                        py = symRealHeight - 1

                    if (pix[px, py] == (255,255,255)):
                        isSet = 1
                        pix[px, py] = (255,0,0)

                        template.append(p)
                    else:
                        pix[px,py] = (0,255,0)

    return template


def getTemplate2(imSym, target, threshold):

    symLeft, symTop, symRight, symBottom = thresholdImage(imSym, target, threshold)

    symRealWidth = (symRight - symLeft)
    symRealHeight = (symBottom - symTop)

    pix = imSym.load()

    template = []

    #print "real width:", symRealWidth, ", height:", symRealHeight

    if (symRealWidth > 3) and (symRealHeight > 3):

        # Draw 7 detection points
        detectPoints = ((symLeft + symRealWidth / 2, symTop), 
            (symLeft + symRealWidth / 2, 1 + symTop + symRealHeight / 4),
            (symLeft + symRealWidth / 2, symTop + symRealHeight / 2),
            (symLeft + symRealWidth / 2, symBottom - 1 - symRealHeight / 4),
            (symLeft + symRealWidth / 2, symTop + symRealHeight),
            (symLeft, 1 + symTop + symRealHeight / 4),
            (symLeft, symTop + symRealHeight / 2),
            (symLeft, symBottom - 1 - symRealHeight / 4),
            (symRight, 1 + symTop + symRealHeight / 4),
            (symRight, symTop + symRealHeight / 2),
            (symRight, symBottom - 1 - symRealHeight / 4))

        for p in range(11):
            x,y = detectPoints[p]

            isSet = 0

            for sy in range(-1,1):
                for sx in range(-1,1):

#                    print sx, sy

                    px = x + sx
                    py = y + sy

                    if (px < symLeft):
                        px = symLeft
                    if (px > symRight):
                        px = symRight - 1
                    if (py < symTop):
                        py = symTop
                    if (py > symBottom):
                        py = symBottom - 1

                    if (pix[px, py] == (255,255,255)):
                        isSet = 1
                        pix[px,py] = (255,0,0)
                    else:
                        pix[px,py] = (0,255,0)

            if isSet == 1:
                template.append(p)
#                pix[x,y] = (255,0,0)
#            else:
#                pix[x,y] = (0,255,0)

    return template


###############################################################

def checkFile(fileName):
    im = Image.open(fileName)

    width, height = im.size

    imRoi = im.crop(timestampRoi)
    #imRoi.save("crop_" + fileName + ".bmp")

    # Crop symbols
    roiWidth, roiHeight = imRoi.size
    symbolWidth = roiWidth / symbolsInLine

    for s in range(symbolsInLine):
        symRoi = (s * symbolWidth, 0, (s + 1) * symbolWidth, roiHeight)
        imSym = imRoi.crop(symRoi)

        imSymNeg = imSym.copy()

        template = getTemplate2(imSym, [0,0,0], 60)
        symbol1, smlrty1 = matchSymbol(template)

        template = getTemplate2(imSymNeg, [255,255,255], 60)
        symbol2, smlrty2 = matchSymbol(template)

        #print "sim1: ", smlrty1, ", sim2: ", smlrty2

        symbol = symbol1
        if smlrty2 > smlrty1:
            symbol = symbol2

        global currentSymNum
        global currentTimestamp

        if (currentSymNum in activeSymbols):
            currentTimestamp = currentTimestamp + str(symbol)
        else:
            currentTimestamp = currentTimestamp + " "

        currentSymNum = currentSymNum + 1

    return

###

def main():
    checkFile(sys.argv[1]);

###################################################################

try:
    loadTemplates()
    main()

    print currentTimestamp

except:
    print "Error handled:", sys.exc_info()[0]
    raise
    sys.exit(100)
