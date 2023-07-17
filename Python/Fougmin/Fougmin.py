__title__ = 'Fougmin recreateion of the oxmin plugin on oxide 1.1.8 now in an faster and better engine'
__author__ = 'ice cold'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import sys

path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")
try:
    import random
except ImportError:
    raise ImportError("Failed to import random! Download the lib!")

sysn = "Fougmin"

class Fougmin:
    ShowConnectedMessage = None
    ShowDisconnectedMessage = None
    

    def On_PluginInit(self):
        ini = self.Fougmin()
        self.AllowedList()
        self.FougminBans()      
        self.ShowConnectedMessage = int(ini.GetSetting("Fougmin", "showconnectedmessage"))
        self.ShowDisconnectedMessage = int(ini.GetSetting("Fougmin", "showdisconnectedmessage"))       

    def Fougmin(self):
        if not Plugin.IniExists("Fougmin"):
            fm = Plugin.CreateIni("Fougmin")
            fm.AddSetting("Fougmin", "showconnectedmessage", "1")
            fm.AddSetting("Fougmin", "showdisconnectedmessage", "1")
            fm.AddSetting("Messages", "welcomenotice", "Welcome this server is modded by Fougmin 1.0")
            fm.Save()
        return Plugin.GetIni("Fougmin")
   

    def AllowedList(self):
        if not Plugin.IniExists("AllowedList"):
            al = Plugin.CreateIni("AllowedList")
            al.Save()
        return Plugin.GetIni("AllowedList")

    def FougminBans(self):
        if not Plugin.IniExists("FougminBans"):
            fb = Plugin.CreateIni("FougminBans")
            fb.Save()
        return Plugin.GetIni("FougminBans")

   # this wil check if you user has permissions or not
    def Allowed(self, Player):
        al = self.AllowedList()
        if al.GetSetting("allowed", Player.SteamID) is not None:
            return True
        return False
    #checks on player connecting if hes banned or not

    def IsFougBanned(self, Player):
        fb = self.FougminBans()
        if fb.GetSetting("hasban", Player.SteamID) is not None or fb.GetSetting("hasipban", Player.IP) is not None:
            return True
        return False



    def On_PlayerConnected(self, Player):
        id = Player.SteamID
        name = Player.Name
        ini = self.Fougmin()
        m = ini.GetSetting("Messages", "welcomenotice")
        Player.Notice(m)
        if self.IsFougBanned(Player):
            Player.MessageFrom(sysn, "You are banned (Kicked)")
            Player.Disconnect()
            Server.BroadcastFrom(sysn, Player.Name + " Tried to join but is banned")
        elif self.ShowConnectedMessage == 1:         
              Server.BroadcastFrom(sysn, name + " Has joined the game")
                    
    def On_PlayerDisconnected(self, Player):
        if self.ShowDisconnectedMessage == 1:
            Server.BroadcastFrom(sysn, name + " Has left the game")



    def On_Command(self, Player, cmd, args):
        if cmd == "fougmin":
            if Player.Admin or self.Allowed(Player):
                Player.MessageFrom(sysn, "/clean FullName >= Removes that entity from the server")
                Player.MessageFrom(sysn, "/kick Name >= kicks player from the server")
                Player.MessageFrom(sysn, "/ban Namee >= bans the player from the server")
                Player.MessageFrom(sysn, "/prod >= turn prod on/off")
                Player.MessageFrom(sysn, "/airdrop Number >= spawn the number of airdrops")
                Player.MessageFrom(sysn, "/tp Name >= teleports you to that player")
                Player.MessageFrom(sysn, "/bring Name >= teleport a player to you")
                Player.MessageFrom(sysn, "/removeadmin >= turns you into admin remove")
                Player.MessageFrom(sysn, "/giveperm Name >= allowes the player to use fougmin commands")
                Player.MessageFrom(sysn, "/removeperm FullName >= remove the player from the permissions list")
        elif cmd == "kick":
            if Player.Admin or self.Allowed(Player):
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                else:
                    name1 = playerr.Name
                    playerr.Notice("You have been kicked")
                    playerr.Disconnect()
                    Server.BroadcastNotice(name1 + " has been kicked from the server")               
        elif cmd == "prod":
            if Player.Admin or self.Allowed(Player):
                id = Player.SteamID
                if not DataStore.ContainsKey("Fougminprod", id):
                    Player.Notice("Prod enabled")
                    DataStore.Add("Fougminprod", id, "on")
                else:
                    id = Player.SteamID
                    Player.Notice("Prod disabled")
                    DataStore.Remove("Fougminprod", id)
        elif cmd == "airdrop":
            if Player.Admin or self.Allowed(Player):
                if len(args) != 1:
                    Player.Notice("Wrong syntax use /airdrop number")
                elif len(args) == 1:
                    arg = args[0]
                    World.Airdrop(int(arg))
                    Player.Notice(arg + " Airdorps spawned")
        elif cmd == "tp":
            if Player.Admin or self.Allowed(Player):
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                else:
                    name = Player.Name
                    name1 = playerr.Name
                    playerr.Notice(name + " teleported to you")
                    Player.Notice("You teleported to " + name1)
                    Player.TeleportTo(playerr.Location)
        elif cmd == "bring":
            if Player.Admin or self.Allowed(Player):
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                else:
                    name = Player.Name
                    name1 = playerr.Name
                    playerr.Notice("You teleported to " + name)
                    Player.Notice("You brought " + name1 + " to you")
                    playerr.TeleportTo(Player.Location)
        elif cmd == "removeadmin":
            if Player.Admin or self.Allowed(Player):
                id = Player.SteamID
                if DataStore.ContainsKey("Fougminremove", id):
                    Player.Notice("Admin remove disabled")
                    DataStore.Remove("Fougminremove", id)
                else:
                    id = Player.SteamID
                    Player.Notice("Remove enabled")
                    DataStore.Add("Fougminremove", id, "on")  
        elif cmd == "ban":
            if Player.Admin or self.Allowed(Player):
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                else:
                    fb = self.FougminBans()
                    if fb.GetSetting("hasban", playerr.SteamID) is not None or fb.GetSetting("hasipban", playerr.IP) is not None:
                        Player.Notice("!", "Wut the player " + playerr.Name + " is banned but still playing report this to ice cold", 15)
                    else:
                        fb = self.FougminBans()
                        fb.AddSetting("hasban", playerr.SteamID)
                        fb.AddSetting("hasipban", playerr.IP)
                        fb.Save()
                        playerr.Notice("You have now the flag banned")
                        playerr.Disconnect()
                        Server.BroadcastNotice(playerr.Name + " Has been permanently banned from the server")
        elif cmd == "giveperm":
            if Player.Admin:
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                else:
                    al = self.AllowedList()
                    if al.GetSetting("allowed", playerr.SteamID) is None:
                        al.AddSetting("allowed", playerr.SteamID)
                        al.Save()
                        Player.Notice(playerr.Name + " Has been added to the list")
                        playerr.Notice("You have now the Fougmin permissions")
                    else:
                        Player.Notice(playerr.Name + " Is already in the list")
        elif cmd == "removeperm":
            if Player.Admin:
                if len(args) != 1:
                    Player.Notice("Wrong syntax use /removeperm ID")
                elif len(args) == 1:
                      arg = str(args[0])
                      aj = self.AllowedList()
                      if aj.GetSetting("allowed", arg) is not None:
                          aj.DeleteSetting("allowed", arg)
                          aj.Save()
                          Player.Notice(arg + " Has been removed from the list")
                      else:
                          Player.Notice(arg + " Is not found")
        elif cmd == "clean":
            if Player.Admin or self.Allowed(Player):
                if len(args) != 1:
                    Player.Notice("Wrong syntax use /clean EntityName")
                elif len(args) == 1:
                    ent = 0
                    arg = args[0]
                    for x in World.Entities:
                        if x.Name == arg:
                            x.Destroy()
                            ent += 1
                    Player.Notice(str(ent) + " " + arg + " Removed")
        elif cmd == "time":
            if Player.Admin or self.Allowed(Player):
                if len(args) != 1:
                    Player.Notice("Wrong syntax use /time number")
                elif len(args) == 1:
                    arg = args[0]
                    World.Time = int(arg)    
        elif cmd == "entities":
            if Player.Admin or self.Allowed(Player):
                c = 0
                for x in World.Entities:
                    c += 1
                Player.Notice(str(c) + " Entities found on the server")
                

    def On_EntityHurt(self, HurtEvent):
        id = HurtEvent.Attacker.SteamID
        if DataStore.ContainsKey("Fougminremove", id):
            if HurtEvent.Attacker.Admin:
                if HurtEvent.Entity.Name is not None:
                    loc = str(HurtEvent.Entity.Location)
                    weapon = str(HurtEvent.WeaponName)
                    HurtEvent.Entity.Destroy()
        elif HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay:
            if not HurtEvent.AttackerIsPlayer:
                return
            id = HurtEvent.Attacker.SteamID
            OwnerID = HurtEvent.Entity.OwnerID
            if DataStore.ContainsKey("Fougminprod", id):
                gun = HurtEvent.WeaponName
                if gun == "Shotgun":
                    return
                HurtEvent.DamageAmount = 0
                if not Server.HasRustPP:
                    return
                dict = Server.GetRustPPAPI().Cache
                if dict.ContainsKey(long(OwnerID)):
                    name = dict[long(OwnerID)]
                    attacker = HurtEvent.Attacker
                    hp = HurtEvent.Entity.Health
                    attacker.MessageFrom(sysn, "********************************Entity information********************************")
                    attacker.MessageFrom(sysn, "Owner " + name + ".")
                    attacker.MessageFrom(sysn, "Entity health " + str(hp))
                    attacker.MessageFrom(sysn, "Name " + HurtEvent.Entity.Name)
                    attacker.MessageFrom(sysn, "********************************Entity information********************************")
                else:
                    attacker.MessageFrom(sysn, "********************************Entity information********************************")
                    Attacker.MessageFrom(sysn, "Owner " + OwnerID + ".")
                    attacker.MessageFrom(sysn, "Entity health " + str(hp))
                    attacker.MessageFrom(sysn, "Name " + HurtEvent.Entity.Name)
                    attacker.MessageFrom(sysn, "********************************Entity information********************************")




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
                Player.MessageFrom(sysn, "Couldn't find " + str.join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            if Player is not None:
                Player.MessageFrom(sysn, "Found " + str(count) +
                                   "player with similar name. Use more correct name!")
            return None

