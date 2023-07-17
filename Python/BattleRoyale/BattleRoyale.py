__title__ = 'BattleRoyale'
__author__ = 'ice cold'
__version__ = '1.0 Beta'

import clr
clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import UnityEngine
from UnityEngine import *
from Fougerite import Entity
import Fougerite


sys = "BattleRoyale"


class BattleRoyale:

    AirDropTimer = None
    PlayTime = None
    WaitTime = None
    LootableObjects = None

    def On_PluginInit(self):
        Plugin.CreateTimer("WaitTime", 2000).Start()
        DataStore.Flush("Playing")
        DataStore.Save()
        Util.ConsoleLog( __title__ +" by " + __author__ + " Version: " + __version__ + " loaded.", False)
        ini = self.BattleRoyale()
        self.AirDropTimer = int(ini.GetSetting("Settings", "AirDropTimer"))
        self.PlayTime = int(ini.GetSetting("Settings", "PlayTime"))
        self.WaitTime = int(ini.GetSetting("Settings", "WaitTime"))   
        self.LootableObject = Util.TryFindReturnType("LootableObject")
        if DataStore.ContainsKey("Lobby", "set"):
            for pl in Server.Players:
                home = DataStore.Get("Lobby", "set")
                pl.TeleportTo(home)
                pl.Inventory.ClearAll()
                pl.Notice("☢", "Everyone has sended to the lobby The game wil start in 2 minutes")
                DataStore.Add("lobby", pl.SteamID)
                DataStore.Save()

    def BattleRoyale(self):
        if not Plugin.IniExists("BattleRoyale"):
            ini = Plugin.CreateIni("BattleRoyale")
            ini.AddSetting("Settings", "AirDropTimer", "600000")
            ini.AddSetting("Settings", "PlayTime", "3600000")
            ini.AddSetting("Settings", "WaitTime", "120000")
            ini.AddSetting("Messages", "StartMsg", "START!! Kill or be killed")
            ini.AddSetting("Messages", "EndMsg", "Battle royale has been ended")
            ini.AddSetting("Notices", "StartNotice", "FIGHT!!!!   live and let die babe")
            ini.AddSetting("Notices", "EndNotice", "The bloody Massacre has ended")
            ini.Save()
        return Plugin.GetIni("BattleRoyale")
     
    def On_Command(self, Player, cmd, args):
        if cmd == "br":
            if Player.Admin:
                Player.MessageFrom(sys, __title__ + " by ice cold")
                Player.MessageFrom(sys, "/brsetlobby - here people wil spawn when they die or connect while plugin is running")
                Player.MessageFrom(sys, "/brabout - shows info about BattleRoyale")
                return
            else:
                Player.MessageFrom(sys, "You cannot use this Command")
                return              
        elif cmd == "brsetlobby":
            if Player.Admin:
                Player.MessageFrom(sys, "Lobby set")
                DataStore.Add("Lobby", "set", Player.Location)
                DataStore.Save()
                return
        elif cmd == "brabout":
            Player.MessageFrom(sys, "Battle Royale created by ice cold")
            Player.MessageFrom(sys, "This plugin is designed to let people pvp to eachother and finding loot that wil be speared around the map")
            Player.MessageFrom(sys, "When the match starts everyone wil get teleport in rad town valley and they need the loot")
            return
        elif cmd == "brlootcheck":
            if Player.Admin:
                World.Spawn("WeaponLootBox", 5797, 397, -3439)
                World.Spawn("MedicalLootBox", 5797, 397, -3439)
                World.Spawn("SupplyCrate", 5716, 406, -3400)
                World.Spawn("BoxLoot", 5716, 406, -3400)
                World.Spawn("SupplyCrate", 5716, 406, -3400)
                World.Spawn("MedicalLootBox", 5716, 406, -3400)
                World.Spawn("SupplyCrate", 5716, 406, -3400)
                World.Spawn("AmmoLootBox", 6140, 383, -3429)
                World.Spawn("SupplyCrate", 6377, 393, -3393)
                World.Spawn("WeaponLootBox", 6611, 358, -3398)
                World.Spawn("SupplyCrate", 6766, 367, -3443)
                World.Spawn("SupplyCrate", 6670, 353, -3862)
                World.Spawn("AmmoLootBox", 6832, 340, -4226)
                World.Spawn("BoxLoot", 6816, 342, -4209)
                World.Spawn("MedicalLootBox", 6739, 346, -4113)
                World.Spawn("WeaponLootBox", 6616, 356, -4186)
                World.Spawn("BoxLoot", 6637, 353, -4246)
                World.Spawn("AmmoLootBox", 6631, 363, -4333)
                World.Spawn("BoxLoot", 6762, 330, -4391)
                World.Spawn("WeaponLootBox", 6407, 360, -4612)
                World.Spawn("MedicalLootBox", 6351, 360, -4684)
                World.Spawn("SupplyCrate", 6292, 364, -4804)
                World.Spawn("AmmoLootBox", 6031, 391, -4441)
                World.Spawn("WeaponLootBox", 6110, 385, -4417)
                World.Spawn("AmmoLootBox", 6158, 378, -4360)
                World.Spawn("MedicalLootBox", 5702, 414, -4247)
                World.Spawn("WeaponLootBox", 5764, 409, -4292)
                World.Spawn("SupplyCrate", 5206, 371, -4778)
                World.Spawn("BoxLoot", 5239, 371, -4796)
                World.Spawn("MedicalLootBox", 5215, 370, -4851)
                World.Spawn("MedicalLootBox", 4544, 478, -4387)
                World.Spawn("BoxLoot", 4552, 477, -4381)
                World.Spawn("WeaponLootBox", 6047, 385, -3584)
                World.Spawn("BoxLoot", 6079, 375, -3524)
                World.Spawn("MedicalLootBox", 6020, 391, -3782)
                return
        elif cmd == "cleanwalls":
            if Player.Admin:
                for x in World.Entities:
                    if x.Name == "Wood Wall":
                        x.Destroy()
                        return
        elif cmd == "cleanloot":
            if Player.Admin:
                self.LootableObjects = UnityEngine.Object.FindObjectsOfType(self.LootableObject)
                for x in self.LootableObjects:
                    if "lootsack" or "MedicalLootBox" or "BoxLoot" or "WeaponLootBox" or "AmmoLootBox" or "SupplyCrate" in x.name.lower():
                         x._inventory.Clear()
                         Util.DestroyObject(x.gameObject)


    def On_PlayerSpawned(self, Player, SpawnEvent):
        if not DataStore.ContainsKey("Playing", Player.SteamID):
            lobby = DataStore.Get("Lobby", "set")
            Player.TeleportTo(lobby) 
            DataStore.Add("lobby", Player.SteamID)
            


    def WaitTimeCallback(self, timer):
        timer.Kill()
        Plugin.CreateTimer("AirDrop", self.AirDropTimer).Start()
        Plugin.CreateTimer("PlayTime", self.PlayTime).Start()
        ini = self.BattleRoyale()
        startmessage = ini.GetSetting("Messages", "StartMsg")
        startnotice = ini.GetSetting("Notices", "StartNotice")
        World.Spawn("WeaponLootBox", 5797, 397, -3439)
        World.Spawn("MedicalLootBox", 5797, 397, -3439)
        World.Spawn("SupplyCrate", 5716, 406, -3400)
        World.Spawn("BoxLoot", 5716, 406, -3400)
        World.Spawn("SupplyCrate", 5716, 406, -3400)
        World.Spawn("MedicalLootBox", 5716, 406, -3400)
        World.Spawn("SupplyCrate", 5716, 406, -3400)
        World.Spawn("AmmoLootBox", 6140, 383, -3429)
        World.Spawn("SupplyCrate", 6377, 393, -3393)
        World.Spawn("WeaponLootBox", 6611, 358, -3398)
        World.Spawn("SupplyCrate", 6766, 367, -3443)
        World.Spawn("SupplyCrate", 6670, 353, -3862)
        World.Spawn("AmmoLootBox", 6832, 340, -4226)
        World.Spawn("BoxLoot", 6816, 342, -4209)
        World.Spawn("MedicalLootBox", 6739, 346, -4113)
        World.Spawn("WeaponLootBox", 6616, 356, -4186)
        World.Spawn("BoxLoot", 6637, 353, -4246)
        World.Spawn("AmmoLootBox", 6631, 363, -4333)
        World.Spawn("BoxLoot", 6762, 330, -4391)
        World.Spawn("WeaponLootBox", 6407, 360, -4612)
        World.Spawn("MedicalLootBox", 6351, 360, -4684)
        World.Spawn("SupplyCrate", 6292, 364, -4804)
        World.Spawn("AmmoLootBox", 6031, 391, -4441)
        World.Spawn("WeaponLootBox", 6110, 385, -4417)
        World.Spawn("AmmoLootBox", 6158, 378, -4360)
        World.Spawn("MedicalLootBox", 5702, 414, -4247)
        World.Spawn("WeaponLootBox", 5764, 409, -4292)
        World.Spawn("SupplyCrate", 5206, 371, -4778)
        World.Spawn("BoxLoot", 5239, 371, -4796)
        World.Spawn("MedicalLootBox", 5215, 370, -4851)
        World.Spawn("MedicalLootBox", 4544, 478, -4387)
        World.Spawn("BoxLoot", 4552, 477, -4381)
        World.Spawn("WeaponLootBox", 6047, 385, -3584)
        World.Spawn("BoxLoot", 6079, 375, -3524)
        World.Spawn("MedicalLootBox", 6020, 391, -3782)
        for pl in Server.Players:
            pl.TeleportTo(6110, 385, -4417)
            pl.Notice("☢", startnotice, 20)
            pl.MessageFrom(sys, startmessage)
            pl.Inventory.AddItem("Rock", 1)
            pl.Inventory.AddItem("Bandage", 3)
            DataStore.Add("Playing", pl.SteamID)
            DataStore.Remove("lobby", pl.SteamID)

    def AirDropCallBack(self, timer):
        World.AirDrop()
        timer.Kill()
        Plugin.CreateTimer("AirDrop", self.AirDropTimer).Start()
        for pl in Server.Players:
            pl.Notice("✈", "Airdrop Incomming")

    def PlayTimeCallBack(self, timer):
        timer.Kill()
        Plugin.CreateTimer("WaitTime", self.WaitTime).Start()
        DataStore.Flush("Playing")
        DataStore.Save()
        endmessage = ini.GetSetting("Messages", "EndMsg")
        endnotice =  ini.GetSetting("Notices", "EndNotice")
        lobby = DataStore.Get("Lobby", "set")
        for pl in Server.Players:
            if DataStore.Get("Playing", pl.SteamID):
                pl.TeleportTo(lobby)
                pl.Inventory.ClearAll()
                pl.Notice("☢", endnotice, 20)
                pl.MessageFrom(sys, endmessage)
        for x in World.Entities:
             if x.Name == ";struct_wood_wall":
                 x.Destroy()
       


    def On_PlayerKilled(self, DeathEvent):
        if DeathEvent.VictimIsPlayer and DeathEvent.AttackerIsPlayer:
            attacker = DeathEvent.Attacker.Name
            victim = DeathEvent.Victim.Name
            weapon = str(DeathEvent.Weapon.Name)
            vid = DeathEvent.Victim.SteamID
            Server.BroadcastFrom(sys, attacker + " Has Destroyed " + victim + " With a " + weapon)
            DataStore.Remove("Playing", vid)

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.VictimIsPlayer and HurtEvent.AttackerIsPlayer:
            if DataStore.ContainsKey("lobby", HurtEvent.Victim.SteamID) or DataStore.ContainsKey("lobby", HurtEvent.Attacker.SteamID):
                HurtEvent.DamageAmount = 0
                HurtEvent.Attacker.MessageFrom(sys, "You cannot kill while in lobby")

    def On_EntityDeployed(self, Player, Entity, ActualPlacer):
        if Entity.Name == "Wood Barricade":
            DataStore.Add("barloc", "loc", Entity.Location)
            loc = DataStore.Get("barloc", "loc")
            Entity.Destroy()
            World.Spawn(";struct_wood_wall", loc)
