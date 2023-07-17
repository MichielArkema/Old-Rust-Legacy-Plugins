__name__ = 'freezer'
__author__ = 'ice cold'
__version__ = '1.0.'
__title__ = 'This is a short version of my C# freezer  https://github.com/icecolderino/Ultimate-Freezer'

import clr
clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import Fougerite
import UnityEngine
from UnityEngine import *

class Freezer:
	
    yellow = "[color #FFFF00]"
    red = "[color #FF0000]"
    BanOnLeave = None

    def On_PluginInit(self):
    	Util.ConsoleLog( __title__ +" by " + __author__ + " Version: " + __version__ + " loaded.", False)
        ini = self.Settings()
        self.BanOnLeave = int(ini.GetSetting("Settings", "BanOnLeave"))

    def Settings(self):
         if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.AddSetting("Settings", "BanOnLeave", "1")
            ini.Save()
            return Plugin.GetIni("Settings")

    def GetPlayerName(self, namee):
        try:
            name = namee.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

    def CheckV(self, Player, args):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.join(" ", args))
            if p is not None:
                return p
            for pl in Server.Players:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            nargs = str(args).lower()
            p = self.GetPlayerName(nargs)
            if p is not None:
                return p
            for pl in Server.Players:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            if Player is not None:
                Player.MessageFrom("Freezer", "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            if Player is not None:
                Player.MessageFrom("Freezer", "Found [color#FF0000]" + str(count) +
                                   "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None


    def On_Command(self, Player, cmd, args):
        if cmd == "freeze":           
            if Player.Admin or Player.Moderator:
                if len(args) > 0:
                    playerr = self.CheckV(Player, args)
                    if playerr is None:
                        return
                    else:
                        if playerr.Admin or playerr.Moderator:
                            Player.MessageFrom("Freezer", "You cannot freeze staff Members")
                            return
                        else:
                            if not playerr.Admin or playerr.Moderator:
                                Player.MessageFrom("Freezer", yellow + playerr.Name + "Has been frozen")
                                playerr.SendCommand("input.bind Left None None")
                                playerr.SendCommand("input.bind Right None None")
                                playerr.SendCommand("input.bind Up None None")
                                playerr.SendCommand("input.bind Down None None")
                                playerr.MessageFrom("Freezer", yellow + "You have been frozen")
                                DataStore.Add("Frozen", playerr.SteamID, "1")
                                return
                            elif cmd == "unfreeze":
                                if Player.Admin or Player.Moderator:
                                    if len(args) > 0:
                                        playerr = self.CheckV(Player, args)
                                        if playerr is None:
                                            return
                                        else:
                                             Player.MessageFrom("Freezer", yellow + playerr.Name + "Has been unfrozen")
                                             playerr.SendCommand("input.bind Left A None")
                                             playerr.SendCommand("input.bind Right D None")
                                             playerr.SendCommand("input.bind Up W None")
                                             playerr.SendCommand("input.bind Down S None")
                                             playerr.MessageFrom("Freezer", yellow + "You have been unfrozen")
                                             DataStore.Remove("Frozen, playerr.SteamID")

    def On_PlayerConnected(self, Player):
        playerr = self.CheckV(Player, args)
        if DataStore.Get("Frozen", playerr.SteamID):
            playerr.SendCommand("input.bind Left None None")
            playerr.SendCommand("input.bind Right None None")
            playerr.SendCommand("input.bind Up None None")
            playerr.SendCommand("input.bind Down None None")
            playerr.MessageFrom("Freezer", yellow + "Omg you cannot bypass the Ultimate Freezer")
                                                                                                                                                      
    def On_PlayerDisconnected(self, Player):
        playerr = self.CheckV(Player, args)
        if self.BanOnLeave == 1:
            if DataStore.Get("Frozen", playerr.SteamID):
                Server.BanPlayer(playerr, " has been banned for leaving while being frozen")
                Server.BroadcastFrom("Freezer", playerr.Name + red + "Has been banned for leaving while being frozen")
