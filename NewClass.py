# Author: Evan Loughlin
# Date: 2019
# 
# C++ Code Generator
# NewClass.py: Generates a class of specified type from a given interface.
# Or, if generating an interface, writes a new interface file with the given INTERFACE_PATH as a filename.
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
from datetime import datetime

FIELDS = {
    "COPYRIGHT": "",
    "YEAR": datetime.now().strftime("%Y"),
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
    
    templateType = sys.argv[1]
    FIELDS["CLASS_NAME"] = sys.argv[2]
    FIELDS["COPYRIGHT"] = loadTemplate("copyright")

    #TODO: Update interface to accept a path, rather than raw filename.
    if(templateType == "interface"):
        interfaceTemplate = loadTemplate(templateType)
        completedTemplate = replaceFields(interfaceTemplate)
        FIELDS["FILE_NAME"] = FIELDS["CLASS_NAME"] + ".h" 
        writeToDisk(completedTemplate)

    elif (templateType == "class"):
        cxxTemplate = loadTemplate("class_cxx")
        completedCxx = replaceFields(cxxTemplate)
        FIELDS["FILE_NAME"] = FIELDS["CLASS_NAME"] + ".cxx"
        writeToDisk(completedCxx)

        headerTemplate = loadTemplate("class_header")
        completedHeader = replaceFields(headerTemplate)
        FIELDS["FILE_NAME"] = FIELDS["CLASS_NAME"] + ".h"
        writeToDisk(completedHeader)

def loadTemplate(templateType):
    template = ""
    filePath = templateFilepath(templateType)
    with open(filePath, "r") as openTemplate:
        template = openTemplate.read()
    return template

def templateFilepath(templateType):
    script_dir = os.path.dirname(__file__)
    rel_path = "templates/" + templateType + ".txt"
    return os.path.join(script_dir, rel_path)

def replaceFields(stringToFill):
    for fieldKey in FIELDS.keys():
        fieldToReplace = "{{" + fieldKey + "}}"
        stringToFill = stringToFill.replace(fieldToReplace, FIELDS[fieldKey])
    return stringToFill

def writeToDisk(stringToSave):
    with open(FIELDS["FILE_NAME"], "w+") as newFile:
        newFile.write(stringToSave)

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