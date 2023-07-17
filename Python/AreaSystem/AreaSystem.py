__title__ = 'AreaSystem choose your own areas in the map to being blocker from building'
__author__ = 'ice cold'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

class AreaSystem:
    UseNoPvpAreas = None
    UseNoBuildingAreas = None
    BuildingBlockedAreas = None
    BattleBlockedAreas = None
    NoBuildingNotice = None
    NoBattlePopup = None

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

    EntityList = {

    }   


    def On_PluginInit(self):
        for x in self.d.keys():
            v = self.d[x].split(',')
            self.Vector2s[Util.CreateVector2(float(v[0]), float(v[1]))] = x
        self.d.clear()
        ini = self.Areas()
        ini2 = self.Settings()
        self.UseNoBuildingAreas = int(ini2.GetSetting("Settings", "UseNoBuildingAreas"))
        self.UseNoPvpAreas = int(ini2.GetSetting("Settings", "UseNoBattleAreas"))
        self.NoBuildingNotice = ini2.GetSetting("Messages", "NoBuildingNotice")
        self.NoBattlePopup = ini2.GetSetting("Message", "NoBattlePopup")
        enum = ini.EnumSection("BlockedBuildingAreas")
        enum2 = ini.EnumSection("BattleBlockedAreas")
        self.BattleBlockedAreas = Plugin.CreateList()
        self.BuildingBlockedAreas = Plugin.CreateList()
        for x in enum:
            self.BuildingBlockedAreas.Add(ini.GetSetting("BuildingBlockedAreas", x))
        for k in enum2:
            self.BattleBlockedAreas.Add(ini.GetSetting("BattleBlockedAreas", k))

        EntityList['WoodFoundation'] = "Wood Foundation"
        EntityList['WoodDoorFrame'] = "Wood Doorway"
        EntityList['WoodDoor'] = "Wood Door"
        EntityList['WoodPillar'] = "Wood Pillar"
        EntityList['WoodWall'] = "Wood Wall"
        EntityList['WoodCeiling'] = "Wood Ceiling"
        EntityList['WoodWindowFrame'] = "Wood Window"
        EntityList['WoodStairs'] = "Wood Stairs"
        EntityList['WoodRamp'] = "Wood Ramp"
        EntityList['WoodSpikeWall'] = "Spike Wall"
        EntityList['LargeWoodSpikeWall'] = "Large Spike Wall"
        EntityList['WoodBox'] = "Wood Storage Box"
        EntityList['WoodBoxLarge'] = "Large Wood Storage"
        EntityList['WoodGate'] = "Wood Gate"
        EntityList['WoodGateway'] = "Wood Gateway"
        EntityList['WoodenDoor'] = "Wood Door"
        EntityList['Wood_Shelter'] = "Wood Shelter"
        EntityList['MetalWall'] = "Metal Wall"
        EntityList['MetalCeiling'] = "Metal Ceiling"
        EntityList['MetalDoorFrame'] = "Metal Doorway"
        EntityList['MetalPillar'] = "Metal Pillar"
        EntityList['MetalFoundation'] = "Metal Foundation"
        EntityList['MetalStairs'] = "Metal Stairs"
        EntityList['MetalRamp'] = "Metal Ramp"
        EntityList['MetalWindowFrame'] = "Metal Window"
        EntityList['MetalDoor'] = "Metal Door"
        EntityList['SmallStash'] = "Small Stash"
        EntityList['Campfire'] = "Camp fire"
        EntityList['Furnace'] = "Furnace"
        EntityList['Workbench'] = "Workbench"
        EntityList['Wood Barricade'] = "Wood Barricade"
        EntityList['RepairBench'] = "Repair Bench"
        EntityList['SleepingBagA'] = "Sleeping Bag"
        EntityList['SingleBed'] = "Bed"


    def Areas(self):
        if not Plugin.IniExists("BlockedAreas"):
            ini = Plugin.CreateIni("BlockedAreas")
            ini.AddSetting("BuildingBlockedAreas", "1", "AreaName")
            ini.AddSetting("BattleBlockedAreas", "1", "AreaName")
            ini.Save()
        return Plugin.GetIni("BlockedAreas")


    def Settings(self):
        if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.AddSetting("Settings", "UseNoBattleAreas", "1")
            ini.AddSetting("Settings", "UseNoBuildingAreas", "1")
            ini.AddSetting("Messages", "NoBattlePopup", "{Area} is an Battle free zone you cant pvp/raid here")
            ini.AddSetting("Messages", "NoBuildingNotice", "{Area} is an building free zone")
            ini.AddSetting()
            ini.Save()
        return Plugin.GetIni("Settings")

    def On_EntityDeployed(self, Player, Entity, ActualPlacer):
        entityname = Entity.Name
        placer = ActualPlacer
        closest = float(999999999)
        loc = Util.CreateVector2(placer.X, placer.Z)
        v = None
        for x in self.Vector2s.keys():
            dist = Util.GetVector2sDistance(loc, x)
            if dist < closest:
                v = x
                closest = dist
        for area in self.BuildingBlockedAreas:
            if self.Vector2s[v] == area:
                Entity.Destroy()
                p = self.NoBattlePopup
                p = p.Replace("{Area}", self.Vector2s[v])
                placer.Notice(p)
                if entityname in EntityList.keys():
                    HurtEvent.Attacker.Inventory.AddItem(EntityList[entityname])

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.AttackerIsPlayer and not HurtEvent.AttackerIsEntity:
            attacker = HurtEvent.Attacker
            closest = float(999999999)
            loc = Util.CreateVector2(attacker.X, attacker.Z)
            v = None
            for x in self.Vector2s.keys():
                dist = Util.GetVector2sDistance(loc, x)
                if dist < closest:
                    v = x
                    closest = dist
            for area in self.BattleBlockedAreas:
                if self.Vector2s[v] == area:
                    p = self.NoBattlePopup
                    p = p.Replace("{Area}", self.Vector2s[v])
                    attacker.Notice(p)
        elif HurtEvent.VictimIsPlayer:
            victim = HurtEvent.Victim
            closest = float(999999999)
            loc = Util.CreateVector2(victim.X, victim.Z)
            v = None
            for x in self.Vector2s.keys():
                dist = Util.GetVector2sDistance(loc, x)
                if dist < closest:
                    v = x
                    closest = dist
            for area in self.BattleBlockedAreas:
                if self.Vector2s[v] == area:
                    p = self.NoBattlePopup
                    p = p.Replace("{Area}", self.Vector2s[v])
                    victim.Notice(p)






