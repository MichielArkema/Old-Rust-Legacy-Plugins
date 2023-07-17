__title__ = 'Raidpvp_schedule'
__author__ = 'ice cold'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

sys = "Scheduler"

class Raidpvp_schedule:
    StartTime = None
    EndTime = None
    AntiRaid = None
    AntiPvp = None
    
    def On_PluginInit(self):
        ini = self.Settings()
        self.StartTime = int(ini.GetSetting("Schedule", "StartTime"))
        self.EndTime = int(ini.GetSetting("Schedule", "EndTime"))
        self.AntiRaid = int(ini.GetSetting("Settings", "AntiRaid"))
        self.AntiPvp = int(ini.GetSetting("Settings", "AntiPvp"))

    def Settings(self):
        if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.AddSetting("Schedule", "StartTime", "17")
            ini.AddSetting("Schedule", "EndTime", "5")
            ini.AddSetting("Settings", "AntiRaid", "1")
            ini.AddSetting("Settings", "AntiPvp", "1")
            ini.Save() 
        return Plugin.GetIni("Settings")



    def On_PlayerHurt(self, HurtEvent):
        if self.AntiPvp == 1:
            if HurtEvent.AttackerIsPlayer and HurtEvent.VictimIsPlayer:
                if World.Time >= self.StartTime or World.Time <= self.EndTime:
                    HurtEvent.DamageAmount = 0
                    HurtEvent.Attacker.Notice("✘", "You cannot kill until Server time = " + str(self.EndTime) + ": Time is now " + str(World.Time) + "", 15)
                    HurtEvent.Attacker.MessageFrom(sys, "You cannot Raid until server time = " + str(self.EndTime) + ": Time is now " + str(World.Time))
                    return
                else:
                    return

    def On_EntityHurt(self, HurtEvent):
        if self.AntiRaid == 1:
            if World.Time >= self.StartTime or World.Time <= self.EndTime:
                if HurtEvent.WeaponName == "Explosive Charge":
                    HurtEvent.DamageAmount = 0
                    HurtEvent.Attacker.Inventory.AddItem("Explosive Charge", 1)
                    HurtEvent.Attacker.Notice("✘", "You cannot raid until Server time = " + str(self.EndTime) + ": Time is now " + str(World.Time) + "", 15)
                    return
                elif HurtEvent.WeaponName == "F1 Grenade":
                      HurtEvent.DamageAmount = 0
                      HurtEvent.Attacker.Inventory.AddItem("F1 Grenade", 1)
                      HurtEvent.Attacker.Notice("✘", "You cannot raid until Server time = " + str(self.EndTime) + ": Time is now " + str(World.Time) + "", 15)
                      HurtEvent.Attacker.MessageFrom(sys, "You cannot Raid until server time = " + str(self.EndTime) + ": Time is now " + str(World.Time))
