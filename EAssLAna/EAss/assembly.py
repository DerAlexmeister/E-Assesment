from ast import operator
import re
from unittest import expectedFailure

INST = ['MOV', 'ADD', 'SUB',] #'JMP', 'JNZ']

def addfunc(command, state):
    return state

def subfunc(command, state):
    return state

def movfunc(command, state):
    return state

def parser(programm):
    try:
        instructionssets = []
        for index, command in enumerate(str(programm).split('\n')):
            command_split = command.split('')
            if len(command_split) == 2:
                return MiniAssembler(error="Synatxerror in line {}!".format(index))
            instruction, operators = command_split[0], command_split[1]
            if instruction not in INST:
                return MiniAssembler(error="Unknown command")
            operators = operators.split(',')
            if (oplen := len(operators)) is None and oplen != 2 or oplen != 3:
                if oplen is None:
                    return MiniAssembler(error="Synatxerror in line {}!".format(index))
                elif oplen < 2:
                    return MiniAssembler(error="There is a operator missing!")
                elif oplen > 3:
                    return MiniAssembler(error="There are more then 3 operators!")
                else:
                    return MiniAssembler(error="Unknown error in the operators!")
            else:
                instructionssets.append((instruction, *operators)) 
        return MiniAssembler(instructions=instructionssets)
    except Exception as error:
        print(error)
        return MiniAssembler(error=str(error))

class MiniAssembler():

    def __init__(self, instructions=[], error=None):
        self.instructions = instructions
        self.error = error

    def getCode(self):
        return self.instructions

    def eval(self):
        try:
            state = {}
            for command in self.instructions:
                state = OPINST[command[0]](command, state)
        except Exception as error:
            self.error = error
            return self.error

    def hasError(self):
        return self.error is not None

    def getError(self):
        return self.error


OPINST = {
    "ADD": addfunc,
    "SUB": subfunc,
    "MOV": movfunc
}