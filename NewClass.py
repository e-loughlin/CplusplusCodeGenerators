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
    "INTERFACE_SUFFIX": "",
    "TEMPLATE_TYPE": "",
    "COPYRIGHT": "",
    "YEAR": "",
    "FILE_PATH": "",
    "CLASS_NAME": "",
    "FILE_NAME": ""
}

TEMPLATE_TYPES = ["interface", "class"]

def main():
    if (sys.argv[1] == '--help'):
        printHelp()
    if (len (sys.argv) != 3):
        printUsageError()
    elif (sys.argv[1] not in TEMPLATE_TYPES):
        printUsageError()
    
    initializeFields(sys.argv)

    if(FIELDS["TEMPLATE_TYPE"] == "interface"):
        createInterface()

    elif (FIELDS["TEMPLATE_TYPE"] == "class"):
        createClass()

def initializeFields(args):
    templateType = args[1]
    FIELDS["INTERFACE_SUFFIX"] = "I"
    FIELDS["TEMPLATE_TYPE"] = args[1]
    FIELDS["YEAR"] = datetime.now().strftime("%Y")
    FIELDS["FILE_PATH"] = os.path.abspath(args[2])
    FIELDS["CLASS_NAME"] = classNameFromFilePath(FIELDS["FILE_PATH"])
    FIELDS["COPYRIGHT"] = loadTemplate("copyright")

# -- File Creation ------------------------------------
def createInterface():
    interfaceTemplate = loadTemplate("interface")
    completedTemplate = replaceFields(interfaceTemplate)
    FIELDS["FILE_NAME"] = FIELDS["CLASS_NAME"] + ".h" 
    writeToDisk(completedTemplate)

def createClass(interfacePath):
    cppTemplate = loadTemplate("class_cpp")
    completedCpp = replaceFields(cppTemplate)
    FIELDS["FILE_NAME"] = FIELDS["CLASS_NAME"] + ".cpp"
    writeToDisk(completedCpp)

    headerTemplate = loadTemplate("class_header")
    completedHeader = replaceFields(headerTemplate)
    FIELDS["FILE_NAME"] = FIELDS["CLASS_NAME"] + ".h"
    writeToDisk(completedHeader)

# -- I/O from Disk ----------------------------------
def loadTemplate(templateType):
    template = ""
    filePath = templateFilepath(templateType)
    with open(filePath, "r") as openTemplate:
        template = openTemplate.read()
    return template

def templateFilepath(templateType):
    scriptDirectory = os.path.dirname(__file__)
    relativePath = "templates/" + templateType + ".txt"
    return os.path.join(scriptDirectory, relativePath)

def classNameFromFilePath(filePath):
    className = ntpath.basename(filePath)
    className = className.split(".")[0]
    # TODO: Remove interface suffix from className
    return className

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