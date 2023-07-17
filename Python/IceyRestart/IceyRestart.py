__title__ = 'Automatic server restart system which rust++ support'
__author__ = 'ice cold'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re
try:
    clr.AddReferenceByPartialName("RustPP")
    import RustPP
    rustpp = Server.GetRustPPAPI()
    rcp = RustPP.Commands
except:
    Util.Log("Failed to load RustPP module (module is not in server)")



class IceyRestart:
    Timer = None
    Message = None
    Notice = None
    NoPerm = None

    def On_PluginInit(self):
        ini = self.Settings()
        self.Timer = int(ini.GetSetting("Settings", "Hours")) * 3600000
        self.Message = ini.GetSetting("Settings", "Message")
        self.Notice = ini.GetSetting("Settings", "Notice")
        self.NoPerm = ini.GetSetting("Settings", "NoPerm")
        try:    
            Plugin.CreateTimer("restart", self.Timer).Start()
        except:
            Util.Log("Something went wrong while starting the timer")

    def Settings(self):
        if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.AddSetting("Settings", "Hours", "3")
            ini.AddSetting("Settings", "Message", "Autorestart countdown started")
            ini.AddSetting("Settings", "Notice", "AutoRestart countdown started")
            ini.AddSetting("Settings", "NoPerm", "You dont have permissions to use this command")
            ini.Save()
        return Plugin.GetIni("Settings")

        
    def restartCallback(self, timer):
        timer.Kill()
        Server.BroadcastFrom("iceyRestart", self.Message)
        Server.BroadcastNotice(self.Notice)
        rcp.ShutDownCommand.StartShutdown();


    def On_Command(self, Player, cmd, args):
        if cmd == "startcountdown":
            if Player.Admin:
                Server.BroadcastFrom("iceyRestart", self.Message)
                Server.BroadcastNotice(self.Notice)
                rcp.ShutDownCommand.StartShutdown();
                Server.RunServerCommand("fougerite.save")
            else:
                Player.Notice(self.NoPerm)
        elif cmd == "restarthelp":
            if Player.Admin or Player.Moderator:
                Player.MessageFrom("IceyRestart", "/startcountdown - force start the countdown to restart")
                Player.MessageFrom("IceyRestart", "/restarttimer - kills and restart the timer")
                Player.MessageFrom("IceyRestart", "/checkrestarttimer - check if the timer is running or not")
            else:
                Player.Notice(self.NoPerm)
        elif cmd == "restarttimer":
            if Player.Admin or Player.Moderator:
                if Plugin.GetTimer("restart") is not None:
                    Plugin.KillTimer("restart")
                    Plugin.CreateTimer("restart", self.Timer).Start()
                    Player.MessageFrom("IceyRestart", "Timer killed and restarted")
                else: #this should never happen but just since we start the timer on pluginInit
                    Player.MessageFrom("IceyRestart", "ERROR: the timer was None restarting the timer now..!")
                    Plugin.CreateTimer("restart", self.Timer).Start()
                    Player.MessageFrom("IceyRestart", "Timer started")
        elif cmd == "checkrestarttimer":
            if Player.Admin or Player.Moderator:
                if Plugin.GetTimer("restart") is not None:
                    Player.Notice("restart timer is running")
                else:
                    Player.Notice("Wut the timer isnt running type /restarttimer")
            else:
                Player.Notice(self.NoPerm)
                    

