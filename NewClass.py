# Author: Evan Loughlin
# Date: 2019
# 
# C++ Code Generator
# NewClass.py: Generates a class of specified type from a given interface.
# Or, if generating an interface, writes a new interface file with the given
# INTERFACE_PATH as a filename.
# 
# Usage:
#   python NewClass.py <CLASS_TYPE> <INTERFACE_PATH>
# 
# CLASS_TYPE   |                    Notes                    |
# ------------------------------------------------------------    
#   interface  |                   
#   class      |    In Progress (Generates .h and .cpp of concrete implementation)
#   test       |    In Progress (Requires testing framework to be in place)
#   mock       |    In Progress (Generates Mocks and SpyMocks)

import sys
import os
import ntpath
from datetime import datetime

FIELDS = {
    "TEMPLATE_TYPE": "",
    "COPYRIGHT": "",
    "YEAR": "",
    "CLASS_NAME": "",
    "FILE_NAME": "",
    "INTERFACE_NAME": ""
}

PREFIXES = {
    "INTERFACE" : "I_",
    "TEST" : "Test",
    "MOCK" : "Mock",
    "SPYMOCK" : "SpyMock",
    "STUB" : "Stub",
    "FAKE" : "Fake",
    "CLASS" : ""
}

EXTENSIONS = {
    "CPP_CLASS": ".cpp",
    "CPP_HEADER": ".h"
}

TEMPLATE_TYPES = ["INTERFACE", "CLASS"]

TEMPLATE_FILENAMES = {
    "INTERFACE" : "interface.txt",
    "CLASS_HEADER" : "class_header.txt",
    "CLASS_CPP" : "class_cpp.txt",
    "COPYRIGHT" : "copyright.txt"
}

class Interface:
    def __init__(self, path):
        self.functions = []
        self.signals = []
        self.includes = []

def main():
    if (sys.argv[1] == '--help'):
        printHelp()
    if (len (sys.argv) != 3):
        printUsageError()
    elif (sys.argv[1].upper() not in TEMPLATE_TYPES):
        printUsageError()
    
    initializeFields(sys.argv)

    if(FIELDS["TEMPLATE_TYPE"] == "INTERFACE"):
        createInterface()
        return

    if (FIELDS["TEMPLATE_TYPE"] == "CLASS"):
        createClass()

# -- Initialization ----------------------------------

def initializeFields(args):
    FIELDS["TEMPLATE_TYPE"] = args[1].upper()
    FIELDS["YEAR"] = datetime.now().strftime("%Y")
    filePath = os.path.abspath(args[2])
    initializeClassName(filePath, FIELDS["TEMPLATE_TYPE"])
    initializeInterfaceName(filePath, FIELDS["TEMPLATE_TYPE"])
    FIELDS["COPYRIGHT"] = loadTemplate("COPYRIGHT")

def initializeClassName(filePath, templateType):
    className = ntpath.basename(filePath)
    className = className.split(".")[0]
    if(templateType != "INTERFACE"):
        className = className.split(PREFIXES["INTERFACE"])[1]
        className = PREFIXES[templateType] + className
    else:
        className = PREFIXES["INTERFACE"] + className
    FIELDS["CLASS_NAME"] = className

def initializeInterfaceName(filePath, templateType):
    interfaceName = ntpath.basename(filePath)
    interfaceName = interfaceName.split(".")[0]
    if(templateType == "INTERFACE"):
        FIELDS["INTERFACE_NAME"] = FIELDS["CLASS_NAME"]
    else:
        FIELDS["INTERFACE_NAME"] = interfaceName

# -- File Creation ------------------------------------
def createInterface():
    interfaceTemplate = loadTemplate("INTERFACE")
    completedTemplate = replaceFields(interfaceTemplate)
    FIELDS["FILE_NAME"] = FIELDS["CLASS_NAME"] + EXTENSIONS["CPP_HEADER"]
    writeToDisk(completedTemplate)

def createClass():
    cppTemplate = loadTemplate("CLASS_CPP")
    completedCpp = replaceFields(cppTemplate)
    FIELDS["FILE_NAME"] = FIELDS["CLASS_NAME"] + EXTENSIONS["CPP_CLASS"]
    writeToDisk(completedCpp)

    headerTemplate = loadTemplate("CLASS_HEADER")
    completedHeader = replaceFields(headerTemplate)
    FIELDS["FILE_NAME"] = FIELDS["CLASS_NAME"] + EXTENSIONS["CPP_HEADER"]
    writeToDisk(completedHeader)

# -- I/O from Disk ----------------------------------
def loadTemplate(templateType):
    filePath = templateFilepath(templateType)
    with open(filePath, "r") as openTemplate:
        return openTemplate.read()

def templateFilepath(templateType):
    scriptDirectory = os.path.dirname(__file__)
    relativePath = "templates/" + TEMPLATE_FILENAMES[templateType]
    return os.path.join(scriptDirectory, relativePath)

def writeToDisk(stringToSave):
    with open(FIELDS["FILE_NAME"], "w+") as newFile:
        newFile.write(stringToSave)

# -- String Search and Replace ----------------------
def replaceFields(stringToFill):
    for fieldKey in FIELDS.keys():
        fieldToReplace = "{{" + fieldKey + "}}"
        stringToFill = stringToFill.replace(fieldToReplace, FIELDS[fieldKey])
    return stringToFill

# -- Print Statements -------------------------------
def printUsageError():
    print("NewClass.py: Invalid arguments. Try \"python NewClass.py --help\".\n")
    sys.exit()

def printHelp():
    print('''
    C++ Code Generator
        NewClass.py: Generates a class of specified type from a given interface.
        Or, if generating an interface, writes a new interface file with the 
        given INTERFACE_PATH as a filename.

    Usage:
        python NewClass.py <CLASS_TYPE> <INTERFACE_PATH>
        
        CLASS_TYPE   |                    Notes                    |
        ------------------------------------------------------------    
        interface  |                   
        class      |    In Progress
        test       |    In Progress
        mock       |    In Progress (Generates Mocks and SpyMocks)")
        ''')
    sys.exit()

if __name__ == "__main__":
    main()