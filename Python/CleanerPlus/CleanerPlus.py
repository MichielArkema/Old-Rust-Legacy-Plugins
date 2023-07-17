__title__ = 'Cleaner++'
__author__ = 'ice cold'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import UnityEngine
from UnityEngine import *
from Fougerite import Entity
import Fougerite

sys = "Cleaner++"
yellow = "[color #FFFF00]"
red = "[color #FF0000]"
green = "[color #009900]"

class CleanerPlus:
    autosackcleantime = None
    useautosackclean = None
    LootableObjects = None

    def On_PluginInit(self):
        ini = self.Settings()     
        self.useautosackclean = int(ini.GetSetting("Settings", "useautosackclean"))
        self.autosackcleantime = int(ini.GetSetting("Settings", "autosackcleantime"))
        self.LootableObject = Util.TryFindReturnType("LootableObject")
        if self.useautosackclean == 1:
            Plugin.CreateTimer("sackremover", self.autosackcleantime).Start()
        else:
            Plugin.Log("Timer", "Was disable not Failed")

    def Settings(self):
        if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.AddSetting("Settings", "useautosackclean", "1")
            ini.AddSetting("Settings", "autosackcleantime", "1800000")
            ini.Save()
        return Plugin.GetIni("Settings")

    def On_Command(self, Player, cmd, args):
        if cmd == "clean":
            if Player.Admin or Player.Moderator:
                if len(args) == 0:
                    Player.MessageFrom(sys, yellow + "Cleaner ++ by ice cold")
                    Player.MessageFrom(sys, green + "/clean sack " + yellow + "- cleans all loot sacks on the server " + red + "(Comes in handy to prevent lag)")
                    Player.MessageFrom(sys, green + "/clean shelters " + yellow + "-cleans all shelters from the server")
                    Player.MessageFrom(sys, green + "/clean campf " + yellow + "- cleans all campfires from the server")
                    Player.MessageFrom(sys, green + "/clean furn " + yellow + "- cleans are furnaces from the server")
                    Player.MessageFrom(sys, green + "/clean barr " + yellow + "- cleans all barricades from the server")
                    Player.MessageFrom(sys, green + "/clean sbag " + yellow + "- cleans all sleepingbags from the server")
                    Player.MessageFrom(sys, green + "/clean bed " + yellow + "- cleans all beds from the server")
                    Player.MessageFrom(sys, green + "/clean smallbox " + yellow + "- cleans all small boxes from the server")
                    Player.MessageFrom(sys, green + "/clean bigbox " + yellow + "- cleans all small boxes from the server")
                    return
                else:
                    arg = args[0]
                    if arg == "sack":
                        if Player.Admin or Player.Moderator:
                             self.LootableObjects = UnityEngine.Object.FindObjectsOfType(self.LootableObject)
                             for x in self.LootableObjects:
                                 if "lootsack" in x.name.lower():
                                     x._inventory.Clear()
                                     Util.DestroyObject(x.gameObject)
                    elif arg == "shelters":
                        if Player.Admin or Player.Moderator:
                            Server.BroadcastFrom(sys, yellow + "All shelters removed")
                            for x in World.Entities:
                                if x.Name == "Wood_Shelter":
                                    x.Destroy()
                    elif arg == "campf":
                        if Player.Admin or Player.Moderator:
                            for x in World.Entities:
                                if "camp" in x.Name.lower():
                                    x.Destroy()
                    elif arg == "furn":
                        if Player.Moderator or Player.Admin:
                            for x in World.Entities:
                                if x.Name == "Furnace":
                                    x.Destroy()
                    elif arg == "sbag":
                        if Player.Admin or Player.Moderator:
                            for x in World.Entities:
                               if x.Name == "Sleeping Bag":
                                   x.Destroy
                    elif arg == "bed":
                        if Player.Admin or Player.Moderator:
                            for x in World.Entities:
                                if  x.Name == "SingleBed":
                                    x.Destroy
                    elif arg == "smallbox":
                        if Player.Admin or Player.Moderator:
                            for x in World.Entities:
                                if x.Name == "WoodBox":
                                   x.Destroy
                    elif arg == "bigbox":
                        if Player.Admin or Player.Moderator:
                            for x in World.Entities:
                                 if x.Name == "WoodBoxLarge":
                                    x.Destroy
                



    def autosackcleantimeCallback(self, timer):
        for pl in Server.Players:
            pl.MessageFrom(sys, green + "Loot sacks " + yellow + "Removed")
            self.LootableObjects = UnityEngine.Object.FindObjectsOfType(self.LootableObject)
            for x in self.LootableObjects:
                if "lootsack" in x.name.lower():
                    x._inventory.Clear()
                    Util.DestroyObject(x.gameObject)




