# ---------------------------------------- - -
#    Author: Nela Vlasakova (xvlasa14)
#      Date: 20. 3. 2020
# ---------------------------------------- - -

import sys 

# E R R O R  C O D E S 
ERROR_PARAM = 10        # missing script parameter or forbidden parameter combination
ERROR_INFILE = 11       # error while opening input file (not existing, insufficent permissions)
ERROR_OUTFILE = 12      # error while opening output files
ERROR_INTERN = 99       # internal error 

ERROR_XML = 31          # bad XML format
ERROR_STRUCT = 32       # unexpected XML structure

ERROR_SEM = 52          # semantic error (usage of undefined label, variable redefinition)
ERROR_OPTYPE = 53       # bad operand types
ERROR_VAR = 54          # accessing nonexisting variable
ERROR_FRAME = 55        # frame doesn't exist
ERROR_VALUE = 56        # missing value
ERROR_OPVALUE = 57      # bad operand value (division by zero)
ERROR_STRING = 58       # error while working with strings

def error(errorFlag):
    errorCodes = {
        10: 'missing script parameter or forbidden parameter combination',
        11: 'error while opening input file (not existing, insufficent permissions)',
        12: 'error while opening output files',
        99: 'internal error',
        31: 'bad XML format',
        32: 'unexpected XML structure',
        52: 'semantic error (usage of undefined label, variable redefinition)',
        53: 'bad operand types',
        54: 'accessing nonexisting variable',
        55: 'frame does not exist',
        56: 'missing value',
        57: 'bad operand value (division by zero)',
        58: 'error while working with strings'
    }
    message = errorCodes.get(errorFlag,"Oppsie")
    print(message, file=sys.stderr)
    exit(errorFlag)

