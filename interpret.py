# ---------------------------------------- - -
#    Author: Nela Vlasakova (xvlasa14)
#      Date: 03/2020
# ---------------------------------------- - -

from interpreter.functions import *
from io import StringIO
import getopt
from sys import argv

# variables
inFile = "LETNI_SEMESTR/IPP/PROJ2/hold.src"     # input file
options = ""    # options from command line
arguments = ""  # source or input file
xml = ""        # opened xml file
inValue = ""    # input value
fileFlag = False
counter = 1
prev = 0

# argument validation
try:
    options, arguments = getopt.getopt(argv[1:], "h", ["help", "source=", "input="])
except getopt.GetoptError:
    error(ERROR_PARAM)

# going through arguments
for opt, arg in options:
    if opt == "-h" or opt == "--help":
        help()
    elif opt == "--source":
        inFile = arg
    elif opt == "--input":
        inValue = arg

#if source file or input value is not present
if inFile == "":
    tempFile = []
    iterator = True
    while iterator == True:
        try:
            line = input()
            if line:
                tempFile.append(line)
            else:
                break
        except EOFError as e:
            iterator = False
    inFile = '\n'.join(tempFile)
    fileFlag = True

# parsing input file
try:
    if fileFlag == True:
        inFile = StringIO(inFile)   # conversion to file type 
        xml = ET.parse(inFile)
    else:
        xml = ET.parse(inFile)
except ET.ParseError:
    error(ERROR_XML)

# checking if XML stuff is ok
xml = xml.getroot()
if xml.tag != "program" or xml.get('language') is None or xml.get('language').lower() != "ippcode20":
    error(ERROR_STRUCT)
for atr in xml.attrib:
    if atr not in ['language', 'name', 'description']:
        error(ERROR_STRUCT)
# going through the xml file
frames = framesObj()
for x in xml:
    # <instruction order="____" opcode="_____">
    instruction = x.attrib
    order = instruction.get('order')
    if order is None:
        error(ERROR_STRUCT)
    else:
        try:
            order = int(order)
        except ValueError:
            error(ERROR_STRUCT)
        if order < prev:
            error(ERROR_STRUCT)
    prev = order
    opcode = instruction.get('opcode')
    opcode = str(opcode).upper()
    if opcode is None:
        error(ERROR_STRUCT)
    else:
        iStack = fillStack(opcode, x, frames)    

for x in xml:
    mainCtrl(x, frames, inValue, iStack)
