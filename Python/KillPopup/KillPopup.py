__title__ = 'KillPopup'
__author__ = 'ice cold'
__version__ = '1.1.4'
__title__ = 'New Commands to enable/disable the popups'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

class KillPopup:
    Enable = None
    NpcKill = None

    def On_PluginInit(self):
        Util.ConsoleLog( __title__ +" by " + __author__ + " Version: " + __version__ + " loaded.", False)
        ini = self.Settings()
        self.NpcKill = int(ini.GetSetting("Settings", "NpcKill"))
        self.Enable = int(ini.GetSetting("Settings", "Enable"))

    def Settings(self):
        if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.AddSetting("Settings", "NpcKill", "1")
            ini.AddSetting("Settings", "Enable", "1")
            ini.Save()               
        return Plugin.GetIni("Settings")

    def On_Command(self, Player, cmd, args):
        if cmd == "popon":
            DataStore.Add("pop", Player.SteamID, "1")
            Player.Notice("✔", "KillPopup is now Enabled")
            return
        elif cmd == "popoff":
            DataStore.Remove("pop", Player.SteamID)
            Player.Notice("✔", "KillPopup is now Disabled")

    def On_PlayerKilled(self, DeathEvent):
        if self.Enable == 1:
            if DataStore.Get("pop", DeathEvent.Attacker.SteamID):
                if DeathEvent.VictimIsPlayer and DeathEvent.AttackerIsPlayer:
                    DeathEvent.Attacker.Notice("☠", "You killed " + DeathEvent.Victim.Name)

    def On_NPCKilled(self, DeathEvent):
        if self.NpcKill == 1:
            if DataStore.Get("pop", DeathEvent.Attacker.SteamID):
                DeathEvent.Attacker.Notice("☠", "You killed a " + DeathEvent.Victim.Name)


