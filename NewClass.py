import sys
import os
from datetime import datetime



FIELDS = {
    "COPYRIGHT": "",
    "YEAR": datetime.now().strftime("%Y"),
    "CLASS_NAME": "",
    "FILE_NAME": ""
}

def main():
    if (len (sys.argv) != 2) and (len (sys.argv) != 3):
        sys.stderr.write("NewClass.py: Invalid arguments. Try NewClass.py --help.\n")
    
    templateType = sys.argv[1]
    FIELDS["CLASS_NAME"] = sys.argv[2]
    FIELDS["COPYRIGHT"] = loadTemplate("copyright")

    if(templateType == "interface"):
        rawTemplate = loadTemplate(templateType)
        completedTemplate = replaceFields(rawTemplate)
        FIELDS["FILE_NAME"] = "I_" + FIELDS["CLASS_NAME"] + ".h"
        writeToDisk(completedTemplate)

def loadTemplate(templateType):
    templateLines = []
    filePath = templateFilepath(templateType)
    with open(filePath, "r") as openTemplate:
        templateLines = openTemplate.read()
    return templateLines

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

if __name__ == "__main__":
    main()