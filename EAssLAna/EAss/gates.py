import random
from schemdraw.parsing import logicparse
import uuid
import os

from django.conf import settings


def andfunc(a, b):
    if (a == 1) and (b == 1):
        return 1
    else:
        return 0

def nandfunc(a, b):
    if (a == 1) and (b == 1):
        return 0
    else:
        return 1

def orfunc(a, b):
    if (a == 1) or (b == 1):
        return 1
    else:
        return 0

def xorfunc(a, b):
    if a != b:
        return 1
    else:
        return 0

def norfunc(a, b):
    if(a == 0) and (b == 0):
        return 1
    elif(a == 0) and (b == 1):
        return 0
    elif(a == 1) and (b == 0):
        return 0
    elif(a == 1) and (b == 1):
        return 0

def xnorfunc(a, b):
    if a == b:
        return 1
    else:
        return 0

def getgate():
    gates = [" and ", " nand ", " or ", " xor ", " nor ", " xnor "]    
    return random.choice(gates)

def gateforeachdepth(pdepth):
    result = []
    for x in range(pdepth):
        if x == 0:
            result.insert(0, 1)
        else:
            val = result[0]
            result.insert(0, random.randint(val, (val * 2)))
    return result

def difficultytodepth(diff):
    depth = 1
    if diff == "Easy":
        depth = 1
    if diff == "Medium":
        depth = 2
    if diff == "Hard":
        depth = 3
    if diff == "Insane":
        depth = 4
    return depth    

def nextchar(currentchar, firsttime):
    if currentchar == "a" and firsttime:
        return currentchar, False
    return chr(ord(currentchar) + 1), False

def creategatecircuit(depth, gatecount):

    currentchar = "a" 
    circuitfunction = ""
    imgpath = ""
    result = 0
    av = []
    avcopy = []
    avresult = []
    avresultcopy = []
    input = ""
    firsttime = True

    for x in range(depth):   
        if x == 0:
            for _ in range(gatecount[x]):
                gate = getgate()
                currentchar, firsttime = nextchar(currentchar, firsttime)
                input1 = (currentchar, random.randint(0, 1))
                currentchar, _ = nextchar(currentchar, firsttime)
                input2 = (currentchar, random.randint(0, 1))
                input += input1[0] + "=" + str(input1[1]) + ";"
                input += input2[0] + "=" + str(input2[1]) + ";"
                av.append('(' + str(input1[0]) + gate + str(input2[0]) + ')')
                avresult.append(GATEINST[gate](input1[1], input2[1]))
        else: 
            for _ in range(gatecount[x]): 
                if len(av) == 1:
                    currentchar, _ = nextchar(currentchar, firsttime)
                    input1 = (currentchar, random.randint(0, 1))
                    input += input1[0] + "=" + str(input1[1]) + ";"
                    gate = getgate()
                    avcopy.append('(' + av[0] + gate + str(input1[0]) + ')')
                    av.pop(0)
                    avresultcopy.append(GATEINST[gate](avresult[0], input1[1]))
                    avresult.pop(0)
                else:
                    ind1 = random.randint(0, len(av)-1)
                    term1 = av[ind1]
                    result1 = avresult[ind1]
                    av.pop(ind1)
                    avresult.pop(ind1)
                    ind2 = random.randint(0, len(av)-1)
                    term2 = av[ind2]
                    result2 = avresult[ind2]
                    av.pop(ind2)
                    avresult.pop(ind2)
                    gate = getgate()
                    avcopy.append('(' + term1 + gate + term2 + ')')                 
                    avresultcopy.append(GATEINST[gate](result1, result2))                                      
                if len(av) == 0:
                    av = avcopy.copy()
                    avcopy.clear()  
                    avresult = avresultcopy.copy()
                    avresultcopy.clear()  
    d = logicparse(av[0], outlabel='$result$')
    input = input[:-1]
    circuitfunction = av[0]
    result = avresult[0]
    t = uuid.uuid4()
    imgpath = "static/imgs/" + "image-" + str(t) + ".svg"
    simgpath = os.path.join(settings.BASE_DIR , imgpath)
    imgpath = "/static/imgs/" + "image-" + str(t) + ".svg"
    d.save(simgpath)            
    return imgpath, result, circuitfunction, input

def createcircuit(diff):
    pdepth = difficultytodepth(diff)
    gatecount = gateforeachdepth(pdepth)
    imgpath, result, circuitfunction, input = creategatecircuit(pdepth, gatecount)
    return imgpath, result, circuitfunction, input

GATEINST = {
    " and ": andfunc,
    " nand ": nandfunc,
    " or ": orfunc,
    " xor ": xorfunc,
    " nor ": norfunc,
    " xnor ": xnorfunc
}