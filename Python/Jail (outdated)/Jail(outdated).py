__title__ = 'Simple Jail'
__author__ = 'ice cold'
__version__ = '1.0'
import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re
#this plugin is outdated use this one > https://github.com/icecolderino/Jail


sysname = "Simple Jail"

class Jail:
    BanOnLeave = None
    bl = None


    def On_PluginInit(self):
        Util.ConsoleLog( __title__ +" by " + __author__ + " Version: " + __version__ + " loaded.", False)
        ini = self.Settings()
        self.BanOnLeave = int(ini.GetSetting("Settings", "BanOnLeave"))
        self.bl = int(ini.GetSetting("Settings", "blockloot"))

    def Settings(self):
        if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.AddSetting("Settings", "BanOnLeave", "0")
            ini.AddSetting("Settings", "blockloot", "1")
            ini.AddSetting("Messages", "SendMessage", "You are sended to jail")
            ini.AddSetting("Messages", "RemoveMsg", "You has been removed from jail Now you are free to go")
            ini.AddSetting("Messages", "NoLootMsg", "You cannot loot while in jail")
            ini.Save()
        return Plugin.GetIni("Settings")


    def On_LootUse(self, LootStartEvent):
        ini = self.Settings()
        pl = LootStartEvent.Player
        id = pl.SteamID
        msg = ini.GetSetting("Messages", "NoLootMsg")
        if self.bl == 1:
            if DataStore.Get("injail", id):
                try:
                   LootStartEvent.Cancel()
                   pl.MessageFrom(sysname, msg)
                except:
                      pass



    def On_Command(self, Player, cmd, args):
        if cmd == "jail":
            if Player.Admin or Player.Moderator:
                if len(args) == 0:
                    Player.MessageFrom(sysname, "Simple Jail by ice cold for Fougerite")
                    Player.MessageFrom(sysname, "/jail checkme - checks if you are in jail or not")
                    Player.MessageFrom(sysname, "/jail send <Name> - sends Player to the jail")
                    Player.MessageFrom(sysname, "/jail remove <Name> - Removes someone from jail")
                    Player.MessageFrom(sysname, "/jail addspawn - add the spawn to jail")
                    Player.MessageFrom(sysname, "/jail cleanspawn - Removes the spawn")
                else:
                    arg = args[0]
                    if arg == "send":
                        if Player.Admin:
                            playerr = self.CheckV(Player, args)
                            if playerr is None:
                                return
                            else:
                                ini = self.Settings()
                                msg = ini.GetSetting("Messages", "SendMessage")
                                playerr.RestrictCommand("home")
                                playerr.RestrictCommand("kit")
                                playerr.RestrictCommand("tpr")
                                playerr.RestrictCommand("tpa")
                                playerr.RestrictCommand("tpaccept")
                                DataStore.Add("lastloc", playerr.SteamID, playerr.Location)
                                jailspawn = DataStore.Get("JailSpawn", "Spawn")
                                Player.MessageFrom(sysname, "You have sended " + playerr.Name + " to jail")
                                playerr.SafeTeleportTo(jailspawn)
                                playerr.MessageFrom(sysname, msg)
                                Server.BroadcastFrom(sysname, playerr.Name + "[color red] Was sended to jail by [color green]" + Player.Name)
                                DataStore.Add("injail", playerr.SteamID, "1")                            
                                DataStore.Save()
                    elif arg == "remove":
                        if Player.Admin:
                            playerr = self.CheckV(Player, args)
                            if playerr is None:
                                return
                            else:
                                if DataStore.Get("injail", playerr.SteamID):
                                    ini = self.Settings()
                                    loc = DataStore.Get("lastloc", playerr.SteamID)
                                    msg = ini.GetSetting("Messages", "LeaveMsg")
                                    Server.BroadcastFrom(sysname, playerr.Name + "[color red] Was Removed from  jail by [color green]" + Player.Name)
                                    Player.MessageFrom(sysname, playerr.Name + " Was removed from the jail")
                                    playerr.MessageFrom(sysname, msg)
                                    DataStore.Remove("injail", playerr.SteamID)
                                    DataStore.Save()
                                    playerr.SafeTeleportTo(loc)
                                    playerr.UnRestrictCommand("home")
                                    playerr.UnRestrictCommand("kit")
                                    playerr.UnRestrictCommand("tpr")
                                    playerr.UnRestrictCommand("tpa")
                                else:
                                    Player.MessageFrom(sysname, playerr.Name + " is not a jail player")
                    elif arg == "addspawn":
                        if Player.Admin:
                           if not DataStore.Get("JailSpawn", "Spawn"):
                               DataStore.Add("JailSpawn", "Spawn", Player.Location)
                               Player.MessageFrom(sysname, "Spawn Has been set")
                               DataStore.Save()
                           else:
                               Player.MessageFrom(sysname, "The jail already has a spawn Type /jail cleanspawn to remove the spawn")
                    elif arg == "cleanspawn":
                        ini = self.Settings()
                        if Player.Admin:
                            if DataStore.ContainsKey("JailSpawn", "Spawn"):
                                DataStore.Flush("JailSpawn")
                                Player.MessageFrom(sysname, "The spawn has been removed")
                                DataStore.Save()
                    elif arg == "checkme":
                        if DataStore.Get("injail", Player.SteamID):
                            Player.MessageFrom(sysname, "IN JAIL: Dont steel candy's next time")
                            return
                        else:
                            Player.MessageFrom(sysname, "Good boy you are not in jail :)")

    def On_PlayerDisconnected(self, Player):
        if self.BanOnLeave == 1:
            if DataStore.Get("injail", Player.SteamID):
                Server.BanPlayer(Player, "Has been banned for leaving in jail")
                Server.BroadcastFrom(sysname, Player.Name + " has been banned for leaving while in jail")


    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.VictimIsPlayer and HurtEvent.AttackerIsPlayer and not HurtEvent.AttackerIsEntity and not HurtEvent.VictimIsEntity:
            if DataStore.Get("injail", HurtEvent.Victim.SteamID) or DataStore.Get("injail", HurtEvent.Attacker.SteamID):    
                HurtEvent.DamageAmount = 0
                HurtEvent.Attacker.MessageFrom(sysname, "You cannot kill people while in jail")
                HurtEvent.Victim.MessageFrom(sysname, "You cannot be killed in jail")

    def On_PlayerSpawned(self, Player, SpawnEvent):
        if DataStore.Get("injail", Player.SteamID):
            jailspawn = DataStore.Get("JailSpawn", "Spawn")
            Player.SafeTeleportTo(jailspawn)
            Player.RestrictCommand("home")
            Player.RestrictCommand("kit")
            Player.RestrictCommand("tpr")
            Player.RestrictCommand("tpa")
            Player.RestrictCommand("tpaccept")

    def On_EntityDeployed(self, Player, Entity, ActualPlacer):
        if DataStore.Get("injail", Player.SteamID):
            Entity.Destroy()
            Player.MessageFrom(sysname, "You cannot build while being in jail")


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
                Player.MessageFrom(sysname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            if Player is not None:
                Player.MessageFrom(sysname, "Found [color#FF0000]" + str(count) +
                                   "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None
