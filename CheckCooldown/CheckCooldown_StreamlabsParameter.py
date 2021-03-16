#---------------------------
#   Import Libraries
#---------------------------
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "CoolDownParameter"
Website = "https://github.com/EinWesen"
Description = "$checkcooldown"
Creator = "EinWesen"
Version = "1.1.0.0"

#---------------------------
#   Script specic Information
#---------------------------
CHECKUSERCOOLDOWN = "$checkcooldown"
COOLDOWN = "$cooldown"

COOLDOWNTYPE_USER = 1;
COOLDOWNTYPE_GLOBAL = 2;
COOLDOWNTYPE_NOMOD_USER = 3;
COOLDOWNTYPE_NOMOD_GLOBAL = 4;

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    return

def parseMyParameters(text):
    # Very bad, but should work for most basic cases
    # - find the first bracketpair (for this param)
    # - split the contents in between by ","
    # - ignore first and last "
    end = text.index(")")
    params = (text[text.index("(")+2:end-1]).split("\",\"", 3);
    if len(params) == 4:
        result = {"type": int(params[0]), "name" : params[1], "cooldown": int(params[2]), "message" : params[3], "length": end+1}
        #Parent.Log(ScriptName, str(result))
        return result
    else:
        raise ValueError("Incorrect number of parameters")
#end def parseMyParameters

def hasCooldown(cooldownType, command, userid):

    if cooldownType == COOLDOWNTYPE_NOMOD_USER:
        if not Parent.HasPermission(userid, "Moderator", ""):
            return Parent.IsOnUserCooldown(ScriptName, command, userid)
        else:
            return False
    elif cooldownType == COOLDOWNTYPE_NOMOD_GLOBAL:
        if not Parent.HasPermission(userid, "Moderator", ""):
            return Parent.IsOnCooldown(ScriptName, command)
        else:
            return False
    elif cooldownType == COOLDOWNTYPE_USER:
        return Parent.IsOnUserCooldown(ScriptName, command, userid)
    elif cooldownType == COOLDOWNTYPE_GLOBAL:
        return Parent.IsOnCooldown(ScriptName, command)

def getCooldown(cooldownType, command, userid):
    if cooldownType == COOLDOWNTYPE_USER or cooldownType == COOLDOWNTYPE_NOMOD_USER:
        return Parent.GetUserCooldownDuration(ScriptName, command, userid)
    elif cooldownType == COOLDOWNTYPE_GLOBAL or cooldownType == COOLDOWNTYPE_NOMOD_GLOBAL:
        return Parent.GetCooldownDuration(ScriptName, command)

def addCooldown(cooldownType, command, userid,seconds):
    if cooldownType == COOLDOWNTYPE_USER or cooldownType == COOLDOWNTYPE_NOMOD_USER:
        return Parent.AddUserCooldown(ScriptName, command, userid, seconds)
    elif cooldownType == COOLDOWNTYPE_GLOBAL or cooldownType == COOLDOWNTYPE_NOMOD_GLOBAL:
        # The Method is called Parent.addCooldown (as in addition), but it actually only sets the cooldown
        # if the command is not on cooldown already, so we don't need to make sure it doesn't extend beyond the intended time.
        # But this also means we have to live with the fact, that in case of COOLDOWNTYPE_NOMOD_GLOBAL 
        # the use of a command by a mod which is currently on global cooldown 
        # will not prevent others from using the command a second later (if the cooldown has elabsed by then)
        return Parent.AddCooldown(ScriptName, command, seconds)

def Parse(parseString, userid, username, targetid, targetname, message):
    if parseString.startswith(CHECKUSERCOOLDOWN):

        #try:
            parsedValues = parseMyParameters(parseString)

            if hasCooldown(parsedValues["type"], parsedValues["name"], userid):
                return parsedValues["message"].replace(COOLDOWN, str(getCooldown(parsedValues["type"], parsedValues["name"], userid)))
            else:
                addCooldown(parsedValues["type"], parsedValues["name"], userid, parsedValues["cooldown"])
                return parseString[parsedValues["length"]:]
        #except:
        #    return "): Error :("

    #end if CHECKUSERCOOLDOWN

    return parseString