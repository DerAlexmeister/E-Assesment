import random
from string import ascii_highercase
import uuid
  
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
    remaininggates = gatecount
    remainingdepth = depth

    for ind in range(depth):
        if ind is not (depth - 1):
            num = random.choice(range(1, remaininggates-remainingdepth))
        else:
            num = remaininggates
        remaininggates -= num
        remainingdepth -= 1

        gateforeachdepth.append(num)

    return gateforeachdepth

def getGates(count):
    gates = ["AND", "NAND", "OR", "XOR", "NOT", "NOR", "XNOR"]
    chosengates = []
    for _ in range(count):
        chosengates.append(random.choice(gates))
    
    return chosengates

def gateinputcount(gate):
    number = 2
    if gate == "NOT": number = 1
    return number

def creategatecircuit(input, gates, gateforeachdepth):
    circuit = []
    unusedinput = {}

    for x in input:
        gateid = uuid.uuid1()
        createdgate = Gate(gateid, x , 0, input[x])
        circuit.append(createdgate)
        unusedinput[gateid] = input[x]
    
    for ind, x in enumerate (gateforeachdepth):
        for _ in range(x):
            
            inputconnection = {}

            currentgate = random.choice(gates)
            gateinputcount = gateinputcount(currentgate)
                
            for _  in range(gateinputcount):
                if ind == (len(gateforeachdepth) - 1) and len(unusedinput) is not 0:
                    inputgateid = random.choice(list(unusedinput))
                    inputconnection[inputgateid] = unusedinput[inputgateid]
                    unusedinput.pop(inputgateid)   
                else:
                    inputgate = random.choice(circuit)
                    inputconnection[inputgate.id] = inputgate.output
                    if inputgate.depth == 0:
                        unusedinput.pop(inputgate.id)          

            inputvalues = list(inputconnection.values())
            if gateinputcount == 1:
                output = GATEINST[currentgate](inputvalues[0])
            else:
                output = GATEINST[currentgate](inputvalues[0], inputvalues[1])
            gate = Gate(uuid.uuid1(), currentgate, ind+1, output, inputconnection)
            
            gates.pop(currentgate) 
            circuit.append(gate)           
    return circuit

def resultgatecheck(circuit):
    for ind, x in enumerate (circuit):
        for y in circuit:
            if x.id == y.inputconnection[0] or x.id == y.inputconnection[len(y.inputcollection)]:
                circuit[ind].resultgate = False
    return circuit

def createcircuit(dif):
    depth, gatecount = difficulty(dif)
    gateforeachdepth = calcgateforeachdepth(depth, gatecount)
    input = generateinput(random.choice(range(2, 1+gateforeachdepth[0])))
    gates = getGates(gatecount)
    gatecircuit = creategatecircuit(input, gates, gateforeachdepth)
    resultgatecheck(gatecircuit)
    return gatecircuit

class Gate():

    def __init__(self, id, gatetype, depth, output, inputconnection={}, resultgate=True):
        self.id = id
        self.gatetype = gatetype
        self.depth = depth
        self.output = output #Output Value
        self.inputconnection = inputconnection  #Child-Gatter
        self.resultgate = resultgate

GATEINST = {
    "AND": andfunc,
    "NAND": nandfunc,
    "OR": orfunc,
    "XOR": xorfunc,
    "NOT": notfunc,
    "NOR": norfunc,
    "XNOR": xnorfunc
}