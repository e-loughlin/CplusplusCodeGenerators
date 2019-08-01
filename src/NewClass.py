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
    "INTERFACE_NAME": "",
    "FUNCTION_DECLARATIONS" : "",
    "FUNCTION_DEFINITIONS" : "",
    "SIGNAL_DECLARATIONS" : "",
    "SIGNAL_DEFINITIONS" : ""
}

PREFIXES = {
    "INTERFACE" : "I",
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
    def __init__(self, pathToInterface):
        self.functions = []
        self.signals = []
        self.includes = []
        self.__rawStringLines = readFileLines(pathToInterface)
        self.__initialize(pathToInterface)
        self.printString()

    def __initialize(self, pathToInterface):
        self.__parseFunctions()
    
    def __parseFunctions(self):
        for line in self.__rawStringLines:
            if self.__isPureVirtualFunctionDeclaration(line):
                self.functions.append(Function(line))
    
    def __isPureVirtualFunctionDeclaration(self, line):
        line = line.split(" ")
        line = list(filter(lambda x: x != " " and len(x) > 0, line))
        return (line[0] == "virtual") and ("0;" in line[-1])

    def printString(self):
        print("Functions\n:")
        for function in self.functions:
            function.toString()

class ConcreteClass:
    def __init__(self, interface):
        self.interface = interface
        self.includes = ""
        self.concreteDeclarations = ""
        self.concreteDefinitions = ""
        self.__initialize()

    def __initialize(self):
        self.__createConcreteDeclarations()
        self.__createConcreteDefinitions()
        self.__createIncludes()
        return
    
    def __createConcreteDeclarations(self):
        for function in self.interface.functions:
            arguments = []
            for argument in function.arguments:
                arguments.append(argument.fullArgument)
            argumentsString = ", ".join(arguments)
            self.concreteDeclarations += ("    {0} {1}({2}) override;\n"\
                .format(function.returnType, function.functionName, argumentsString))
        print(self.concreteDeclarations)


    def __createConcreteDefinitions(self):
        #TODO: Implement
        return

    def __createIncludes(self):
        #TODO: Implement
        return

class Function:
    def __init__(self, virtualDeclaration):
        self.virtualDeclaration = virtualDeclaration
        self.returnType = ""
        self.functionName = ""
        self.arguments = []
        self.concreteDeclaration = ""
        self.concreteDefinition = ""
        self.isConstFunction = False
        self.initialize(virtualDeclaration)
    
    def initialize(self, virtualDeclaration):
        self.__parseVirtualDeclaration()
        self.__initializeConcreteDeclaration()
        self.__initializeConcreteDefinition()
        return

    #TODO: Current implementation won't work for return types like "QString &" or "const char *"
    #TODO: Need a way to determine if the function is const (isConstFunction)
    def __parseVirtualDeclaration(self):
        virtualDefList = self.virtualDeclaration.split(" ")
        virtualDefList = list(filter(lambda x: x != " ", virtualDefList))
        self.returnType = virtualDefList[virtualDefList.index("virtual") + 1]
        self.functionName = virtualDefList[virtualDefList.index(self.returnType) + 1].split("(")[0]
        rawArguments = self.virtualDeclaration.split("(")[1].split(")")[0].split(",")
        for arg in rawArguments:
            self.arguments.append(FunctionArgument(arg))
    
    def __initializeConcreteDeclaration(self):
        #TODO
        return 

    def __initializeConcreteDefinition(self):
        #TODO
        return

    def toString(self):
        print(self.virtualDeclaration)
        print(self.returnType)
        print(self.functionName)
        for arg in self.arguments:
            arg.toString()

class FunctionArgument:
    def __init__(self, rawArgument):
        self.rawArgument = rawArgument
        self.objectType = ""
        self.objectName = ""
        self.include = ""
        self.fullArgument = ""
        self.__initialize()

    def __initialize(self):
        self.__parseRawArgument()
        self.__parseInclude()
    
    def __parseRawArgument(self):
        argument = self.rawArgument.split(" ")
        objectTypeAndName = list(filter(lambda x: x != " " and len(x) > 0, argument))
        self.objectType = objectTypeAndName[0]
        self.objectName = objectTypeAndName[1]
        self.fullArgument = "{0} {1}".format(self.objectType, self.objectName)
    
    def __parseInclude(self):
        #TODO: Implement so that includes are properly captured. (Qt Objects are special cases)
        return
    
    def toString(self):
        print(self.objectType + " " + self.objectName)

def main():
    if (len(sys.argv) < 2):
        printUsageError()
    if (sys.argv[1] == '--help') or (sys.argv[1] == '-h'):
        printHelp()
    if (len (sys.argv) != 3):
        printUsageError()
    elif (sys.argv[1].upper() not in TEMPLATE_TYPES):
        printUsageError()
    
    initializeFields(sys.argv)

    # Case 1: Creating a new interface (sys.argv[2] is a new interface filename)
    if(FIELDS["TEMPLATE_TYPE"] == "INTERFACE"):
        createInterface()
        return

    # Case 2: Creating another class from an existing interface (sys.argv[2] is a path to an existing interface)
    pathToInterface = os.path.abspath(sys.argv[2])
    existingInterface = Interface(pathToInterface)

    #TODO: Utilize the instantiated class objects' functions to get declarations and definitions


    if (FIELDS["TEMPLATE_TYPE"] == "CLASS"):
        concreteClass = ConcreteClass(existingInterface)
        FIELDS["FUNCTION_DECLARATIONS"] = concreteClass.concreteDeclarations
        createClass()
        return
    
    if (FIELDS["TEMPLATE_TYPE"] == "MOCK"):
        createMock()
        return

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

def createMock():
    sys.path.append(os.path.dirname(__file__))
    from cpp import gmock_class
    gmock_class.__doc__ = gmock_class.__doc__.replace('gmock_class.py', __file__)
    gmock_class.main()

# -- I/O from Disk ----------------------------------
def loadTemplate(templateType):
    filePath = templateFilepath(templateType)
    return readFile(filePath)

def readFile(filePath):
    with open(filePath, "r") as openTemplate:
        return openTemplate.read()

def readFileLines(filePath):
    with open(filePath, "r") as openTemplate:
        return openTemplate.readlines()

def templateFilepath(templateType):
    scriptDirectory = os.path.dirname(__file__)
    relativePath = "../templates/" + TEMPLATE_FILENAMES[templateType]
    return os.path.join(scriptDirectory, relativePath)

def writeToDisk(stringToSave):
    with open(FIELDS["FILE_NAME"], "w+") as newFile:
        newFile.write(stringToSave)

# -- String Search and Replace ----------------------
def replaceFields(stringToFill):
    for fieldKey in FIELDS.keys():
        stringToFill = searchAndReplace(fieldKey, FIELDS[fieldKey], stringToFill)
    return stringToFill

def searchAndReplace(toSearch, toReplace, stringToUpdate):
    toSearch = "{{" + toSearch + "}}"
    return stringToUpdate.replace(toSearch, toReplace)

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