import random
from string import ascii_highercase

def andfunc(a,b):
    if (a == 1) and (b == 1):
        return 1
    else:
        return 0

def nandfunc (a, b):
    if (a == 1) and (b == 1):
        return 0
    else:
        return 1

def orfunc(a, b):
    if (a == 1) or (b == 1):
        return 1
    else:
        return 0

def xorfunc (a, b):
    if a != b:
        return 1
    else:
        return 0

def notfunc(a):
    return not a

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

def generateinput(max):
    input = {}
    for _ in range(max):
        for letter in ascii_highercase:
            input[letter] = random.uniform(0, 1)
    return input

def difficulty(dif):
    depth, gatecount = 3, 5
    if dif == "easy":
        depth = 3
        gatecount = random.choice(range(5, 7))
    elif dif == "medium":
        depth = 4
        gatecount = random.choice(range(5, 7))
    elif dif == "medium":
        depth = 5
        gatecount = random.choice(range(5, 7))
    return depth, gatecount

def calcgateforeachdepth(depth, gatecount):
    gateforeachdepth = []
    remainingdepth = depth - 1
    count = gatecount
    restcount = gatecount

    for ind in range(depth):
        count = count - remainingdepth 
        if ind < (depth - 1):
            num = random.choice(range(1, count))
        else:
            num = restcount
        remainingdepth -= 1
        restcount = restcount - num

        gateforeachdepth.append(num)

    return gateforeachdepth

def getGates(count):
    gates = ["AND", "NAND", "OR", "XOR", "NOT", "NOR", "XNOR"]
    chosengates = []
    for _ in range(count):
        chosengates.append(random.choice(gates))
    return chosengates

def createcircuit(dif):
    depth, gatecount = difficulty(dif)
    gateforeachdepth = calcgateforeachdepth(depth, gatecount)
    input = generateinput(random.choice(range(2, gateforeachdepth[0])))
    gates = getGates(gatecount)

    
    
    circuit = {}
    return circuit

class Gate():

    def __init__(self, id, inputconnection={}, outputconnection={}):
        self.id = id
        self.inputconnection = inputconnection
        self.outputconnection = outputconnection 

GATEINST = {
    "AND": andfunc,
    "NAND": nandfunc,
    "OR": orfunc,
    "XOR": xorfunc,
    "NOT": notfunc,
    "NOR": norfunc,
    "XNOR": xnorfunc
}