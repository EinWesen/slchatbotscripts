#---------------------------
#   Import Libraries
#---------------------------
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#Custom
import re
import codecs

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "ReadAllLines"
Website = "https://github.com/EinWesen"
Description = "$readalllines"
Creator = "EinWesen"
Version = "1.0.1.0"

#---------------------------
#   Script specic Information
#---------------------------
READ_ALL_LINES = "$readalllines"
paramRegEx = re.compile("\\"+READ_ALL_LINES+"\(\"(.*)\" *, *\"(.*)\"\)")

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    return

def readAllLinesFromFile(filepath):
    file1 = None
    Lines = None
    try:
        #files written with $savefile seem to be UTF-8 encoded, and thats what we expect to read here
        file1 = codecs.open(filepath, "r", "utf-8-sig")        
    except Exception as fe:
        raise
    else:
        Lines = [line.strip() for line in file1.readlines() if len(line.strip()) > 0]
        file1.close()
        return Lines
#end def

def Parse(parseString, userid, username, targetid, targetname, message):
    if READ_ALL_LINES in parseString:

        try:
            parseString = paramRegEx.sub(lambda m : m.group(2).join(readAllLinesFromFile(m.group(1))), parseString)
        except Exception as e:
            parseString = "Fehler bei " + READ_ALL_LINES + ": " + str(e)

    #end if READ_ALL_LINES

    return parseString
