__title__ = 'Allows players to share their doors with other players'
__author__ = 'ice cold'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

class DoorShare:

    def On_PluginInit(self):
        Util.ConsoleLog("Doorshare system by ice cold loaded")

    def DoorShare(self):
        if not Plugin.IniExists("doorshare"):
            ini = Plugin.CreateIni("doorshare")
            ini.Save()
        return Plugin.GetIni("doorshare")

    def IsShared(self, id, tid):
        ini = self.DoorShare()
        if ini.GetSetting(str(id), str(tid)) is not None:
            return True
        return False

    def On_Command(self, Player, cmd, args):
        ini = self.DoorShare()
        if cmd == "share":
            playerr = self.CheckV(Player, args)
            if len(args) == 0:
                Player.Notice("Syntax: /share name")
                return
            if playerr is None:
                return
            else:
                ini.AddSetting(Player.SteamID, playerr.SteamID, playerr.Name)
                ini.Save()
                Player.Notice("All doors shared with " + playerr.Name)
        elif cmd == "unshare":
            if len(args) == 0:
                Player.Notice("Syntax: /unshare name")
                return       
            else:
                enum = ini.EnumSection(Player.SteamID)
                text = self.argsToText(args)
                for id in enum:
                     s = ini.GetSetting(Player.SteamID, id)
                     if s in text or s == text:
                         ini.DeleteSetting(Player.SteamID, id)
                         ini.Save()
                         Player.Notice("All doors unshared with " + s)
                         return
                else:
                    Player.Notice("You are not sharing doors with " + text)

    def On_DoorUse(self, Player, DoorUseEvent):
        if Player is None:
            return
        id = Player.SteamID
        OwnerID = self.GetIt(DoorUseEvent.Entity)
        if OwnerID is None:
            return
        if self.IsShared(OwnerID, id):
            DoorUseEvent.Open = True

    
    def argsToText(self, args):
        text = str.join(" ", args)
        return text

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
            Player.MessageFrom("DoorShare", "Couldn't find " + str.join(" ", args) + " !")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom("DoorShare", "Found " + str(count)
                               + " player with similar name. Use more correct name!")
            return None

    def GetIt(self, Entity):
        try:
            if Entity.IsDeployableObject():
                return str(Entity.Object.ownerID)
            if Entity.IsStructure():
                return str(Entity.Object._master.ownerID)
        except:
            return None
