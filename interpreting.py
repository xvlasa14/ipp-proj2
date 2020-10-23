# ---------------------------------------- - -
#    Author: Nela Vlasakova (xvlasa14)
#      Date: 03/2020
# ---------------------------------------- - -
from interpreter.errors import *
import re, sys

newValue = None
position = []
sStack = []
# returns frame according to fFlag
def setFrame(frames, fFlag):
    if fFlag == "GF":
        return frames.GF
    elif fFlag == "TF":
        return frames.TF
    elif fFlag == "LF":
        return frames.LF
    else:
        error(ERROR_SEM)

# seraches for given variable in frame chosen by fFlag, returns if found or not
def existsIn(variable, frames, fFlag):
    tempFrame = setFrame(frames, fFlag)
    if tempFrame is None:
        error(ERROR_FRAME)
    for var in tempFrame:
        if var[0] == variable:
            return var
    error(ERROR_VAR)

   # return(variable in [a for b in tempFrame for a in b])

# searches given frame, for specifing thing, returns it's coordinates
def searchIndex(frame, search):
    c1 = 0
    c2 = 0
    x = 0
    while x < len(frame):
        try:
            c2 = frame[x].index(search)
            break
        except:
            pass
        x += 1
    c1 = x
    return c1, c2

def getValue(variable, frames, fFlag):
    if existsIn(variable, frames, fFlag):
        tmpFrame = setFrame(frames, fFlag)
        for var in tmpFrame:
            if var[1] == None and var[0] == variable:
                error(ERROR_VALUE)
        c1, c2 = searchIndex(tmpFrame, variable)
        return tmpFrame[c1][c2 + 1]
    else:
        error(ERROR_FRAME)
    
# returns value in hopefully correct type
def cvrtVal(valueInfo):
    if valueInfo[0] == "bool":
        if valueInfo[1] == "true":
            return True
        if valueInfo[1] == "false":
            return False
        else:
            error(ERROR_STRUCT)
    elif valueInfo[0] == "int":
        return int(valueInfo[1])
    elif valueInfo[0] == "string":
        return str(valueInfo[1])
    elif valueInfo[0] == "nil":
        return str(valueInfo[1])
    else:
        error(ERROR_STRUCT)

# determines if symbs (2) is var or not and returns it's value
def symbVal(symb1, symb2, frames):
    if symb1[0] == "var":
        val1 = getValue(symb1[1][1], frames, symb1[1][0])
    else:
        val1 = cvrtVal(symb1)
    if symb2 == None:
        return val1
    elif symb2[0] == "var":
        val2 = getValue(symb2[1][1], frames, symb2[1][0])
    else:
        val2 = cvrtVal(symb2)
    return val1, val2

# executes all functions 
def doThis(iStack, instruction, frames, inValue, labelList):
    if instruction[0] == "MOVE":
        # arg1 (var(1)) control
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            # finding where to put the new value
            frame1 = setFrame(frames, instruction[1][1][0])
            cX, cY = searchIndex(frame1, instruction[1][1][1])
            # if arg2 is also var
            if instruction[2][0] == "var":
                # arg2 (var2) control
                frame2 = setFrame(frames, instruction[2][1][0])
                if existsIn(instruction[2][1][1], frames, instruction[1][1][0]):
                    # finding what to put in var1
                    cA, cB = searchIndex(frame2, instruction[2][1][1])
                    newValue = frame2[cA][cB + 1]
                else:
                    error(ERROR_VAR)
            #if arg2 is some value
            else:
                newValue = cvrtVal(instruction[2])
            # moving the new found value
            frame1[cX][cY + 1] = newValue    
        else:
            error(ERROR_VAR)

    elif instruction[0] == "BREAK":
        print("FRAMES: ", file=sys.stderr)
        print("\t", frames.GF, file=sys.stderr)
        print("\t", frames.LF, file=sys.stderr)
        print("\t", frames.TF, file=sys.stderr)
        print("\t", frames.fStack, file=sys.stderr)
        pass

    elif instruction[0] == "CREATEFRAME":
        frames.TF = []

    elif instruction[0] == "PUSHFRAME":
        if frames.TF == None:
            error(ERROR_FRAME)

        frames.fStack.append(frames.TF)   # move TF to stack of frames
        frames.LF = frames.TF 
        frames.TF = None

    elif instruction[0] == "POPFRAME":
        if frames.fStack == []:
            error(ERROR_FRAME)

        frames.TF = frames.fStack[-1]
        frames.fStack.pop(-1)
        try:
            frames.LF = frames.fStack[-1]
        except IndexError:
            frames.LF = None
        # TO DO POPNUTI

    elif instruction[0] == "DEFVAR":
        if instruction[1][1][0] == "GF":
            if instruction[1][1][1] not in [a for b in frames.GF for a in b]:
                tempFrame = []
                tempFrame.append(instruction[1][1][1])
                tempFrame.append(None)
                frames.GF.append(tempFrame)
            else:
                error(ERROR_SEM)
        elif instruction[1][1][0] == "TF":
            if frames.TF == None:
                error(ERROR_FRAME)
            if instruction[1][1][1] not in [a for b in frames.TF for a in b]:
                tempFrame = []
                tempFrame.append(instruction[1][1][1])
                tempFrame.append(None)
                frames.TF.append(tempFrame)
            else:
                error(ERROR_SEM)
        elif instruction[1][1][0] == "LF":
            if frames.LF == None:
                error(ERROR_FRAME)
            if instruction[1][1][1] not in [a for b in frames.LF for a in b]:
                tempFrame = []
                tempFrame.append(instruction[1][1][1])
                tempFrame.append(None)
                frames.LF.append(tempFrame)
            else:
                error(ERROR_SEM)
    
    elif instruction[0] == "CALL":
        tempInstr = ['LABEL', ['label', instruction[1][1]]]
        if tempInstr in iStack:
            position.append(iStack.index(instruction))

            newLoop = iStack.index(tempInstr)
            return newLoop
        pass

    elif instruction[0] == "RETURN":
        if len(position) == 0:
            error(ERROR_VALUE)
        else:
            newLoop = position[-1]
            position.pop(-1)
            return newLoop

    elif instruction[0] == "PUSHS":
        if instruction[1][0] == "var":
            if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
                symbVal(instruction[1], None, frames)
            else:
                ERROR(ERROR_VAR)
        else:
            sStack.append(cvrtVal(instruction[1]))

    elif instruction[0] == "POPS":
        if not sStack:
            error(ERROR_VALUE)
        else:
            if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
                cX, cY = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                setFrame(frames, instruction[1][1][0])[cX][cY + 1] = sStack[-1]
                sStack.pop(-1)
            else:
                error(ERROR_VALUE)

        pass

    elif instruction[0] == "ADD":
        # if variable that will hold the result exists
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            val1, val2 = symbVal(instruction[2], instruction[3], frames)

            if val1 == None or val2 == None:
                error(ERROR_VAR)

            if isinstance(val1, int) and isinstance(val2, int) and not isinstance(val1, bool) and not isinstance(val2, bool):
                x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                setFrame(frames, instruction[1][1][0])[x][y + 1] = int(val2) + int(val1)
            else:
                error(ERROR_OPTYPE)
        else:
                error(ERROR_OPTYPE)

    elif instruction[0] == "SUB":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            val1, val2 = symbVal(instruction[2], instruction[3], frames)

            if val1 == None or val2 == None:
                error(ERROR_VAR)

            if isinstance(val1, int) and isinstance(val2, int) and not isinstance(val1, bool) and not isinstance(val2, bool):
                x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                setFrame(frames, instruction[1][1][0])[x][y + 1] = int(val2) - int(val1)
        else:
            error(ERROR_OPTYPE)

    elif instruction[0] == "MUL":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            val1, val2 = symbVal(instruction[2], instruction[3], frames)

            if val1 == None or val2 == None:
                error(ERROR_VAR)

            if isinstance(val1, int) and isinstance(val2, int) and not isinstance(val1, bool) and not isinstance(val2, bool):
                x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                setFrame(frames, instruction[1][1][0])[x][y + 1] = int(val2) * int(val1)
            else:
                error(ERROR_OPTYPE)
        else:
            error(ERROR_VAR)

    elif instruction[0] == "IDIV":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            val1, val2 = symbVal(instruction[2], instruction[3], frames)
            if val1 == None or val2 == None:
                error(ERROR_VAR)

            if val2 == 0:
                error(ERROR_OPVALUE)

            if isinstance(val1, int) and isinstance(val2, int) and not isinstance(val1, bool) and not isinstance(val2, bool):
                x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                setFrame(frames, instruction[1][1][0])[x][y + 1] = int(val1) // int(val2)
            else:
                error(ERROR_OPTYPE)
        else:
            error(ERROR_VAR)

    elif instruction[0] == "LT":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            val1, val2 = symbVal(instruction[2], instruction[3], frames)

            if val1 == None or val2 == None:
                error(ERROR_VAR)

            if val1 == "nil" or val2 == "nil":
                error(ERROR_OPTYPE)

            if type(val1) == type(val2):
                x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                if val1 < val2:
                    setFrame(frames, instruction[1][1][0])[x][y + 1] = True
                else:
                    setFrame(frames, instruction[1][1][0])[x][y + 1] = False
            else:
                error(ERROR_OPTYPE)
        else:
            error(ERROR_VAR)

    elif instruction[0] == "GT":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            val1, val2 = symbVal(instruction[2], instruction[3], frames)

            if val1 == None or val2 == None:
                error(ERROR_VAR)

            if val1 == "nil" or val2 == "nil":
                error(ERROR_OPTYPE)

            if type(val1) == type(val2):
                x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                if val1 > val2:
                    setFrame(frames, instruction[1][1][0])[x][y + 1] = True
                else:
                    setFrame(frames, instruction[1][1][0])[x][y + 1] = False
            else:
                error(ERROR_OPTYPE)
        else:
            error(ERROR_VAR)

    elif instruction[0] == "EQ":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            val1, val2 = symbVal(instruction[2], instruction[3], frames)

            if val1 == None or val2 == None:
                error(ERROR_VAR)

            if type(val1) != type(val2) and val1 != "nil" and val2 != "nil":
                error(ERROR_OPTYPE)

            if type(val1) == type(val2):
                if isinstance(val1, int) and not isinstance(val1, bool):
                    val1 = int(val1)
                    val2 = int(val2)

            x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
            if val1 == "nil" or val2 == "nil":
                setFrame(frames, instruction[1][1][0])[x][y + 1] = val1 == val2
            if val1 == val2:
                setFrame(frames, instruction[1][1][0])[x][y + 1] = True
            else:
                setFrame(frames, instruction[1][1][0])[x][y + 1] = False
        else:
            error(ERROR_VAR)

    elif instruction[0] == "AND":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            val1, val2 = symbVal(instruction[2], instruction[3], frames)

            if val1 == None or val2 == None:
                error(ERROR_VAR)

            if isinstance(val1, bool) and isinstance(val2, bool):
                x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                setFrame(frames, instruction[1][1][0])[x][y + 1] = val1 and val2
            else:
                error(ERROR_OPTYPE)
        else:
            error(ERROR_VAR)

    elif instruction[0] == "OR":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            val1, val2 = symbVal(instruction[2], instruction[3], frames)

            if val1 == None or val2 == None:
                error(ERROR_VAR)

            if isinstance(val1, bool) and isinstance(val2, bool):
                x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                setFrame(frames, instruction[1][1][0])[x][y + 1] = val1 or val2
            else:
                error(ERROR_OPTYPE)
        else:
            error(ERROR_VAR)

    elif instruction[0] == "NOT":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            if instruction[2][0] == "var":
                val1 = getValue(instruction[2][1][1], frames, instruction[2][1][0])
            else:
                val1 = cvrtVal(instruction[2])

            if val1 == None:
                error(ERROR_VAR)

            if isinstance(val1, bool):
                x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                setFrame(frames, instruction[1][1][0])[x][y + 1] = not val1
            else:
                error(ERROR_OPTYPE)
        else:
            error(ERROR_VAR)

    elif instruction[0] == "INT2CHAR":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            if instruction[2][0] == "var":
                val1 = getValue(instruction[2][1][1], frames, instruction[2][1][0])
            else:
                val1 = cvrtVal(instruction[2])
        
            if val1 == None:
                error(ERROR_VAR)

            if isinstance(val1, int):
                x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                try:
                    setFrame(frames, instruction[1][1][0])[x][y + 1] = chr(val1)
                except ValueError:
                    error(ERROR_STRING)
            else:
                error(ERROR_OPTYPE)
        else:
            error(ERROR_VAR)

    elif instruction[0] == "STRI2INT":
        try:
            # STRI2INT GF@a string@abcd int@2
            if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
                if instruction[2][0] == "var":
                    val1 = getValue(instruction[2][1][1], frames, instruction[2][1][0])
                else:
                    val1 = cvrtVal(instruction[2])
                if instruction[3][0] == "var":
                    val1 = getValue(instruction[3][1][1], frames, instruction[3][1][0])
                else:
                    val2 = cvrtVal(instruction[3])


                if val1 == None or val2 == None:
                    error(ERROR_VAR)
                if not isinstance(val2, int):
                    error(ERROR_OPTYPE)
                elif isinstance(val2, bool):
                    error(ERROR_OPTYPE)
                if val2 < 0:
                    error(ERROR_STRING)
                if isinstance(val1, str):
                    if str(val1) in ("nil"):
                        error(ERROR_OPTYPE)

                    replace = val1[int(val2)]
                    x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                    setFrame(frames, instruction[1][1][0])[x][y + 1] = ord(replace)
                else:
                    error(ERROR_OPTYPE)
            else:
                error(ERROR_VAR)

        except IndexError:
            error(ERROR_STRING)

    elif instruction[0] == "READ":
        if inValue == "":
            try:
                inValue = input()
            except (KeyboardInterrupt, EOFError):
                inValue = "nil"
        if instruction[2][1] == "int":
            if re.search(r"^[0-9]+$", inValue):
                inValue = int(inValue)
            else:
                inValue = "nil"
        elif instruction[2][1] == "string":
            if re.search(r"^(\s*|\w*|)*(\s*|\w*)$", inValue):
                inValue = str(inValue)
            else:
                inValue = "nil"
        elif instruction[2][1] == "bool":
            if inValue.lower() == "true":
                inValue = True
            else:
                inValue = False
        else:
            inValue = "nil"

        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            tmpFrame = setFrame(frames, instruction[1][1][0])
            cX, cY = searchIndex(tmpFrame, instruction[1][1][1])
            tmpFrame[cX][cY + 1] = inValue
        else:
            error(ERROR_VAR)
        pass

    elif instruction[0] == "WRITE":
        if instruction[1][0] == "var":
            val = getValue(instruction[1][1][1], frames, instruction[1][1][0])
            if val == None:
                error(ERROR_VALUE)
            if val == "nil":
                val = "nil"
            if val == True:
                val = "true"
            if val == False:
                val = "false"
        elif instruction[1][0] == "bool":
            if instruction[1][1].lower() == "true":
                val = "true"
            if instruction[1][1].lower() == "false":
                val = "false"
        elif instruction[1][0] == "nil":
            val = ''
        else:
            val = str(instruction[1][1])
        
        if val == None:
            error(ERROR_OPTYPE)

        print(val, end="")

    elif instruction[0] == "CONCAT":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            val1, val2 = symbVal(instruction[2], instruction[3], frames)

            if val1 == None or val2 == None:
                error(ERROR_OPTYPE)

            if val1 == "nil" or val2 == "nil":
                error(ERROR_OPTYPE)

            if isinstance(val1, str) and isinstance(val2, str):
                x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                setFrame(frames, instruction[1][1][0])[x][y + 1] = val1 + val2
            else:
                error(ERROR_OPTYPE)
        else:
            error(ERROR_VAR)

    elif instruction[0] == "STRLEN":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            val1 = symbVal(instruction[2], None, frames)
            if isinstance(val1, str):
                x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                setFrame(frames, instruction[1][1][0])[x][y + 1] = len(val1)
            else:
                error(ERROR_OPTYPE)
        else:
            error(ERROR_VAR)
        pass

    elif instruction[0] == "GETCHAR":
        """ do var ulozi char z symb1 v pozici symb2"""
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            s = symbVal(instruction[2], None, frames)
            pos = symbVal(instruction[3], None, frames)

            if s == None or pos == None:
                error(ERROR_VAR)

            if isinstance(s, str) and isinstance(pos, int):
                x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
                setFrame(frames, instruction[1][1][0])[x][y + 1] = s[pos]
        else:
            error(ERROR_VAR)
            pass

    elif instruction[0] == "SETCHAR":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            """ zmeni znak retezce v var na pozici symb1 na symb2"""
            s, pos = symbVal(instruction[1], instruction[2], frames)
            repS = symbVal(instruction[3], None, frames)

            if s == None or pos == None or repS == None:
                error(ERROR_VAR)

            if not isinstance(s, str) or not isinstance(pos, int) or not isinstance(repS, str) or isinstance(pos, bool):
                error(ERROR_OPTYPE)

            if len(s) <= pos or pos < 0 or len(repS) == 0:
                error(ERROR_STRING)

            tempS = list(s)
            tempS[pos] = repS[0]
            s = ''.join(tempS)

            x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
            setFrame(frames, instruction[1][1][0])[x][y + 1] = s
        else:
            error(ERROR_VAR)

    elif instruction[0] == "TYPE":
        if existsIn(instruction[1][1][1], frames, instruction[1][1][0]):
            symb = symbVal(instruction[2], None, frames)
            if symb == True or symb == False:
                thisType = "bool"
            elif symb == "nil":
                thisType = "nil"
            elif isinstance(symb, str):
                thisType = "string"
            
            elif isinstance(symb, int):
                thisType = "int"

            elif isinstance(symb, bool):
                thisType = "bool"

            else:
                thisType = ""
            x, y = searchIndex(setFrame(frames, instruction[1][1][0]), instruction[1][1][1])
            setFrame(frames, instruction[1][1][0])[x][y + 1] = thisType
        else:
            error(ERROR_VAR)
            
    elif instruction[0] == "LABEL":
        pass

    elif instruction[0] == "JUMP":
        if instruction[1][1] not in labelList:
            error(ERROR_SEM)
        tempInstr = ['LABEL', ['label', instruction[1][1]]]
        if tempInstr in iStack:
            newLoop = iStack.index(tempInstr)
            return newLoop
        else:
            error(ERROR_SEM)

    elif instruction[0] == "JUMPIFEQ":
        # getting val1 and val2 
        if instruction[2][0] == "var":
            val1 = getValue(instruction[2][1][1], frames, instruction[2][1][0])
        else:
            val1 = cvrtVal(instruction[2])

        if instruction[3][0] == "var":
            val2 = getValue(instruction[3][1][1], frames, instruction[3][1][0])
        else:
            val2 = cvrtVal(instruction[3])

        if instruction[1][1] not in labelList:
            error(ERROR_SEM)

        if type(val1) == type(val2) or str(val1) in ("nil") or str(val2) in ("nil"):
        #jumping if val1 is equal to val2
            if val1 == val2:

                tempInstr = ['LABEL', ['label', instruction[1][1]]]
                if tempInstr in iStack:
                    newLoop = iStack.index(tempInstr)
                    return newLoop
                else:
                    error(ERROR_SEM)
        else:
            error(ERROR_OPTYPE)

    elif instruction[0] == "JUMPIFNEQ":
        # getting val1 and val2 
        if instruction[2][0] == "var":
            val1 = getValue(instruction[2][1][1], frames, instruction[2][1][0])
        else:
            val1 = cvrtVal(instruction[2])

        if instruction[3][0] == "var":
            val2 = getValue(instruction[3][1][1], frames, instruction[3][1][0])
        else:
            val2 = cvrtVal(instruction[3])

        if instruction[1][1] not in labelList:
            error(ERROR_SEM)

        if type(val1) == type(val2) or str(val1) in ("nil") or str(val2) in ("nil"):
        #jumping if val1 is equal to val2
            if val1 != val2:

                tempInstr = ['LABEL', ['label', instruction[1][1]]]
                newLoop = iStack.index(tempInstr)
                return newLoop
        else:
            error(ERROR_OPTYPE)

    elif instruction[0] == "EXIT":
        retC = symbVal(instruction[1], None, frames)
        if isinstance(retC, int) and not isinstance(retC, bool):
            if retC >= 0 and retC <= 49:
                exit(retC)
            else:
                error(ERROR_OPVALUE)
        else:
            error(ERROR_OPTYPE)

    elif instruction[0] == "DPRINT":
        if instruction[1][0] == "var":
            val = getValue(instruction[1][1][1], frames, instruction[1][1][0])
            if val == "nil":
                val = ""
        elif instruction[1][0] == "bool":
            if instruction[1][1].lower() == "true":
                val = "true"
            if instruction[1][1].lower() == "false":
                val = "false"
        elif instruction[1][0] == "nil":
                val = ""
        else:
            val = instruction[1][1]
        
        if val == None:
            error(ERROR_OPTYPE)

        print(val, file=sys.stderr)

    else:
        error(ERROR_INTERN)

