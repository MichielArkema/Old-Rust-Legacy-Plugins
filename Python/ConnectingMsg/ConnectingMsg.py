__name__ = 'Join Message'
__author__ = 'ice cold'
__version__ = '1.0.'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

class ConnectingMsg:
    sysname = None
    JoinMessage = None
    LeaveMessage = None
    StaffJoinMessage = None
    StaffLeaveMessage = None
    
    def On_PluginInit(self):
        Util.ConsoleLog( __name__ +" by " + __author__ + " Version: " + __version__ + " loaded.", False)
        ini = self.Config()
        self.JoinMessage = int(ini.GetSetting("Settings", "JoinMessage"))
        self.LeaveMessage = int(ini.GetSetting("Settings", "LeaveMessage"))
        self.StaffJoinMessage = int(ini.GetSetting("Settings", "StaffJoinMessage"))
        self.StaffLeaveMessage = int(ini.GetSetting("Settings", "StaffLeaveMessage"))
        self.sysname = ini.GetSetting("Settings", "sysname")

    def Config(self):
        if not Plugin.IniExists("Config"):
            ini = Plugin.CreateIni("Config")
            ini.AddSetting("Settings", "JoinMessage", "1")
            ini.AddSetting("Settings", "LeaveMessage", "1")
            ini.AddSetting("Settings", "StaffJoinMessage", "1")
            ini.AddSetting("Settings", "StaffLeaveMessage", "1")
            ini.AddSetting("Settings", "sysname", "ConnectedMsg") 
            ini.Save()
        return Plugin.GetIni("Config")

    def On_PlayerConnected(self, Player):
        if self.JoinMessage == 1:
            if Player.Admin and self.StaffJoinMessage == 1:
                Server.BroadcastFrom(self.sysname, "[Admin] " + Player.Name + " has joined the server!")
            else:
                Server.BroadcastFrom(self.sysname, Player.Name + " has joined the server")
        
    def On_PlayerDisconnected(self, Player):
        if self.LeaveMessage == 1:
            if Player.Admin and self.StaffLeaveMessage == 1:
                Server.BroadcastFrom(self.sysname, "[Admin]  " + Player.Name + " has left the server!")
            else:
                Server.BroadcastFrom(self.sysname, Player.Name + " has left the server")
