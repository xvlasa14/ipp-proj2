# ---------------------------------------- - -
#    Author: Nela Vlasakova (xvlasa14)
#      Date: 03/2020
# ---------------------------------------- - -

from interpreter.errors import *
from interpreter.interpreting import *
import xml.etree.ElementTree as ET
import sys, re

looped = None
iStack = []
labelList = []
# ------------- O B J E C T S ------------ - -
class instrObj:
        def __init__(self, varType, varName):
                self.arg = []
                self.arg.append(varType)
                self.arg.append(varName)

        @staticmethod
        def fill(opcode, x):
                instruction = []
                instruction.append(opcode.upper())
                for y in x:       
                        var = instrObj(y.attrib.get('type'), y.text)
                        instruction.append(var.arg)
                return instruction

class framesObj:
        def __init__(self):
                self.fStack = []
                self.GF = []
                self.TF = None
                self.LF = None      

# ----------- F U N C T I O N S ---------- - -
def argCount(opcode, instruction):
        if opcode in ["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"]:
                if len(instruction) == 1:
                        return len(instruction)
                else:
                        error(ERROR_STRUCT)
        elif opcode in ["DEFVAR", "POPS", "LABEL", "JUMP", "CALL", "PUSHS", "WRITE", "EXIT", "DPRINT"]:
                if len(instruction) == 2:
                        return len(instruction)
                else:
                        error(ERROR_STRUCT)
        elif opcode in ["MOVE", "NOT", "INT2CHAR", "STRLEN", "TYPE", "READ", ]:
                if len(instruction) == 3:
                        return len(instruction)
                else:
                        error(ERROR_STRUCT)
        elif opcode in ["LT", "GT", "EQ", "AND", "OR", "STRI2INT", "CONCAT", "GETCHAR", "SETCHAR", "ADD", "SUB", "MUL", "IDIV", "JUMPIFEQ", "JUMPIFNEQ"]:
                if len(instruction) == 4:
                        return len(instruction)
                else:
                        error(ERROR_STRUCT)
        else:
                error(ERROR_STRUCT)

def varCheck(instruction, count):
        variable = instruction[count]
        if variable[0] == "var":
                if re.search(r"^(GF|LF|TF)@[\D]+(_|-|\$|&|%|\*|!|\?|[a-zA-Z0-9]*)*$", str(variable[1])):
                        instruction[count][1] = re.split('@', instruction[count][1])
                        pass
                else:
                        error(ERROR_STRUCT)

        elif variable[0] == "int":
                if re.search(r"^(-){0,1}[0-9]+$", str(variable[1])):
                        pass
                else:
                        error(ERROR_STRUCT)
        elif variable[0] == "string":
                if re.search(r"^(\s|.*)(\s|.*)$", str(variable[1])):
                        if re.search(r"(\\[0-9]{3})", str(variable[1])):
                                esc = re.findall(r"(\\[0-9]{3})", str(variable[1]))
                                escGroup = set(esc)
                                escAll = list(escGroup)

                                for x in escAll:
                                        variable[1] = str(variable[1]).replace(x, chr(int(x[1:])))
                        else:
                                pass
                else:
                        error(ERROR_STRUCT)
        elif variable[0] == "bool":
                if re.search(r"^(true|false)$", str(variable[1])):
                        pass
                else:
                        error(ERROR_STRUCT)
        elif variable[0] == "type":
                if re.search(r"^(int|bool|string)$", str(variable[1])):
                        pass
                else:
                        error(ERROR_STRUCT)

        elif variable[0] == "nil":
                if re.search(r"^nil$", str(variable[1])):
                        pass
                else:
                        error(ERROR_STRUCT)
        elif variable[0] == "label":
                if re.search(r"^(_|-|\$|&|%|\*|!|\?|[a-zA-Z])(_|-|\$|&|%|\*|!|\?|[a-zA-Z0-9])*$", str(variable[1])):
                        pass
                else:
                        error(ERROR_STRUCT)
        else:
                error(ERROR_STRUCT)

def fillStack(opcode, x, frames):
        count = 1
        instruction = instrObj.fill(opcode, x)
        length = argCount(opcode, instruction) - 1 
        # var ____ ____
        while count <= length:
                varCheck(instruction, count)
                count = count + 1

        iStack.append(instruction)
                
        return iStack
        
def mainCtrl(x, frames, inValue, iStack): 
        opcode = iStack[0][0]
        count = 1
        instruction = instrObj.fill(opcode, x)
        length = argCount(opcode, instruction) - 1
        # var ____ ____
        while count <= length:
                varCheck(instruction, count)
                count = count + 1

        for instruction in iStack:
                if instruction[0] == "LABEL":
                        for lab in labelList:
                                if lab == instruction[1][1]:
                                        error(ERROR_SEM)
                        labelList.append(instruction[1][1])


        iterator = 0
        while iStack[iterator] in iStack:
                looped = doThis(iStack, iStack[iterator], frames, inValue, labelList)
                if looped is not None:
                        iterator = looped + 1
                else:
                        iterator += 1
                
                if iterator == len(iStack):
                        exit(0)

def help():
        print("""
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                                < WHAT IS THIS SORCERY? >
                Program loads XML file, interprets it and generates output.
                If one of the following parameters isn't present, the desired
                                data is loaded from stdin.
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                --source=file   source XML file
                --input=file    input intended for interpretation itself
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                --help          prints this help message
                -h             also prints this help message

        """)
        exit(0)