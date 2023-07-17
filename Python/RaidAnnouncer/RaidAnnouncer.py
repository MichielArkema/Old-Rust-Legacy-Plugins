__title__ = 'RaidAnnouncer'
__author__ = 'ice cold'
__version__ = '1.3.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

yellow = "[color #FFFF00]"
red = "[color #FF0000]"
green = "[color #009900]"
orange = "[color orange]"
silver = "[color silver]"

class RaidAnnouncer: 
    ShowGrenada = None
    ShowC4 = None
    TimeFlush = None
    C4RaidMessage = None
    GrenadaRaidMessage = None
    ChatName = None
    OfflineRaidMessage = None
    OnlineRaidMessage = None


    d = {
        "Hacker Valley South": "5907,-1848",
        "Hacker Mountain South": "5268,-1961",
        "Hacker Valley Middle": "5268,-2700",
        "Hacker Mountain North": "4529,-2274",
        "Hacker Valley North": "4416,-2813",
        "Wasteland North": "3208,-4191",
        "Wasteland South": "6433,-2374",
        "Wasteland East": "4942,-2061",
        "Wasteland West": "3827,-5682",
        "Sweden": "3677,-4617",
        "Everust Mountain": "5005,-3226",
        "North Everust Mountain": "4316,-3439",
        "South Everust Mountain": "5907,-2700",
        "Metal Valley": "6825,-3038",
        "Metal Mountain": "7185,-3339",
        "Metal Hill": "5055,-5256",
        "Resource Mountain": "5268,-3665",
        "Resource Valley": "5531,-3552",
        "Resource Hole": "6942,-3502",
        "Resource Road": "6659,-3527",
        "Beach": "5494,-5770",
        "Beach Mountain": "5108,-5875",
        "Coast Valley": "5501,-5286",
        "Coast Mountain": "5750,-4677",
        "Coast Resource": "6120,-4930",
        "Secret Mountain": "6709,-4730",
        "Secret Valley": "7085,-4617",
        "Factory Radtown": "6446,-4667",
        "Small Radtown": "6120,-3452",
        "Big Radtown": "5218,-4800",
        "Hangar": "6809,-4304",
        "Tanks": "6859,-3865",
        "Civilian Forest": "6659,-4028",
        "Civilian Mountain": "6346,-4028",
        "Civilian Road": "6120,-4404",
        "Ballzack Mountain": "4316,-5682",
        "Ballzack Valley": "4720,-5660",
        "Spain Valley": "4742,-5143",
        "Portugal Mountain": "4203,-4570",
        "Portugal": "4579,-4637",
        "Lone Tree Mountain": "4842,-4354",
        "Forest": "5368,-4434",
        "Rad-Town Valley": "5907,-3400",
        "Next Valley": "4955,-3900",
        "Silk Valley": "5674,-4048",
        "French Valley": "5995,-3978",
        "Ecko Valley": "7085,-3815",
        "Ecko Mountain": "7348,-4100",
        "Zombie Hill": "6396,-3428"
    }   

    Vector2s = {

    }

    def On_PluginInit(self):
         for x in self.d.keys():
             v = self.d[x].split(',')
             self.Vector2s[Util.CreateVector2(float(v[0]), float(v[1]))] = x
         self.d.clear()
         ini = self.Settings()
         self.ShowGrenada = int(ini.GetSetting("Settings", "ShowGrenada"))
         self.ShowC4 = int(ini.GetSetting("Settings", "ShowC4"))
         self.TimeFlush = int(ini.GetSetting("Settings", "Timer")) * 60000
         self.C4RaidMessage = ini.GetSetting("Message", "C4RaidMessage")
         self.GrenadaRaidMessage = ini.GetSetting("Message", "GrenadaRaidMessage")
         self.ChatName = ini.GetSetting("Settings", "ChatName")
         self.OfflineRaidMessage = ini.GetSetting("Message", "OfflineRaidMessage")
         self.OnlineRaidMessage = ini.GetSetting("Messages", "OnlineRaidMessage")
         Plugin.CreateTimer("RaidFlushTimer", self.TimeFlush).Start()

    def Settings(self):
        if not Plugin.IniExists("Settings"):
             ini = Plugin.CreateIni("Settings")
             ini.AddSetting("Settings", "ChatName", "RaidAnnouncer")
             ini.AddSetting("Settings", "ShowGrenada", "1")
             ini.AddSetting("Settings", "ShowC4", "1")
             ini.AddSetting("Settings", "Timer", "30")
             ini.AddSetting("Message", "C4RaidMessage", "{RAIDER} is now raiding {BaseOwner} with Explosive Charge on {ENTITYNAME} Near: {LOC}")
             ini.AddSetting("Message", "GrenadaRaidMessage", "{RAIDER} is now raiding {BaseOwner} with Grenada on {ENTITYNAME} Near: {LOC}")
             ini.AddSetting("Message", "OfflineRaidMessage", "[color red]Offline raid")
             ini.AddSetting("Message", "OnlineRaidMessage", "[color #009900]Online raid")
             ini.Save() 
        return Plugin.GetIni("Settings")


    def On_EntityDestroyed(self, DestroyEvent):
         if DestroyEvent.Attacker is not None and DestroyEvent.Entity is not None and not DestroyEvent.IsDecay and DestroyEvent.DamageType is not None:        
             if DestroyEvent.WeaponName == "Explosive Charge" and not DataStore.Get("C4Raiding", DestroyEvent.Attacker.SteamID) and self.ShowC4 == 1:
                 if not Server.HasRustPP:
                     return
                 Raider = DestroyEvent.Attacker
                 closest = float(999999999)
                 loc = Util.CreateVector2(Raider.X, Raider.Z)
                 v = None
                 for x in self.Vector2s.keys():
                     dist = Util.GetVector2sDistance(loc, x)
                     if dist < closest:
                         v = x
                         closest = dist
                 Raider = DestroyEvent.Attacker.Name
                 RaiderID = DestroyEvent.Attacker.SteamID
                 OwnerID = DestroyEvent.Entity.OwnerID
                 ent = DestroyEvent.Entity.Name
                 creator = DestroyEvent.Entity.Creator
                 dict = Server.GetRustPPAPI().Cache
                 if dict.ContainsKey(long(OwnerID)):
                     name = dict[long(OwnerID)] 
                     m = self.C4RaidMessage
                     m = m.Replace("{RAIDER}", Raider)
                     m = m.Replace("{BaseOwner}", name)
                     m = m.Replace("{ENTITYNAME}", ent)
                     m = m.Replace("{LOC}", self.Vector2s[v])
                     Server.BroadcastFrom(self.ChatName, m)                
                     DataStore.Add("C4Raiding", RaiderID, "1")
                     if self.Online(creator):
                         m = self.OnlineRaidMessage
                         Server.BroadcastFrom(self.ChatName, m)
                     else:
                         m = self.OfflineRaidMessage
                         Server.BroadcastFrom(self.ChatName, m)


                     return
             elif DestroyEvent.WeaponName == "F1 Grenade" and not DataStore.Get("GrenadaRaiding", DestroyEvent.Attacker.SteamID) and self.ShowGrenada == 1:
                 if not Server.HasRustPP:
                     return
                 Raider = DestroyEvent.Attacker
                 closest = float(999999999)
                 loc = Util.CreateVector2(Raider.X, Raider.Z)
                 v = None
                 for x in self.Vector2s.keys():
                     dist = Util.GetVector2sDistance(loc, x)
                     if dist < closest:
                         v = x
                         closest = dist                       
                 Raider = DestroyEvent.Attacker.Name
                 RaiderID = DestroyEvent.Attacker.SteamID
                 OwnerID = DestroyEvent.Entity.OwnerID
                 ent = DestroyEvent.Entity.Name
                 creator = DestroyEvent.Entity.Creator
                 dict = Server.GetRustPPAPI().Cache
                 if dict.ContainsKey(long(OwnerID)):
                     name = dict[long(OwnerID)]
                     m = self.GrenadaRaidMessage
                     m = m.Replace("{RAIDER}", Raider)
                     m = m.Replace("{BaseOwner}", name)
                     m = m.Replace("{ENTITYNAME}", ent)
                     m = m.Replace("{LOC}", self.Vector2s[v])
                     Server.BroadcastFrom(self.ChatName, m)                
                     DataStore.Add("GrenadaRaiding", RaiderID, "1")
                     if self.Online(creator):
                         m = self.OnlineRaidMessage
                         Server.BroadcastFrom(self.ChatName, m)
                     else:
                         m = self.OfflineRaidMessage
                         Server.BroadcastFrom(self.ChatName, m)


    def Online(self, Player):
        if Player.IsOnline:
            return True
        return False


    def On_Command(self, Player, cmd, args):
        if cmd == "raidannouncer":
            if Player.Admin:
                Player.MessageFrom(self.ChatName,  "RaidAnnouncer by ice cold")
                Player.MessageFrom(self.ChatName,  green + "/raidsflush - " + yellow + "Flushes all raids from all players")
                return
        elif cmd == "raidsflush":
            if Player.Admin:
                DataStore.Flush("C4Raiding")
                DataStore.Flush("GrenadaRaiding")
                DataStore.Save()
                Player.MessageFrom(self.ChatName, red + "All raids Are been flushed")
                return
            else:
                Player.MessageFrom(self.ChatName, red + "You are not allowed to flush the raids DataBase")


    def On_PlayerDisconnected(self, Player):
        if DataStore.ContainsKey("C4Raiding", Player.SteamID) or DataStore.ContainsKey("GrenadaRaiding", Player.SteamID):
            DataStore.Remove("C4Raiding", Player.SteamID)
            DataStore.Remove("GrenadaRaiding", Player.SteamID)

    def RaidFlushTimerCallback(self, timer):
        DataStore.Flush("C4Raiding")
        DataStore.Flush("GrenadaRaiding")
        timer.Kill()
        Plugin.CreateTimer("RaidFlushTimer", self.TimeFlush).Start()


    def GetIt(self, Entity):
        try:
            if Entity.IsDeployableObject():
                return Entity.Object.ownerID
            if Entity.IsStructure():
                return Entity.Object._master.ownerID
        except:
            return None
