__title__ = 'The best plugin for sending random messages/popups'
_author__ = 'ice cold'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re
try:
    import random
except ImportError:
    raise ImportError("Failed to import Random!")


class AutoBroadcaster:
    RegisteredMessages = None
    RegisteredNotices = None
    EnableMessage = None
    EnabledNotices = None
    ChatName = None
    Timer1 = None
    Timer2 = None

    def On_PluginInit(self):
        ini = self.Settings()
        self.Messages()
        self.Notices()
        self.ChatName = ini.GetSetting("Settings", "ChatName")
        self.RegisteredMessages = int(ini.GetSetting("Message", "Registered"))
        self.RegisteredNotices = int(ini.GetSetting("Notice", "Registered"))
        self.EnableMessage = int(ini.GetSetting("Message", "Enable"))
        self.EnabledNotices = int(ini.GetSetting("Notice", "Enable"))
        self.Timer1 = int(ini.GetSetting("Message", "Timer")) * 1000
        self.Timer2 = int(ini.GetSetting("Notice", "Timer")) * 1000
        try:
            if self.EnableMessage == 1:
                Plugin.CreateTimer("Timer1", self.Timer1).Start()
                Util.Log("[Messages Timer] started on " + str(self.Timer1) + " ms")
            if self.EnabledNotices == 1:
                Plugin.CreateTimer("Timer2", self.Timer2).Start()
                Util.Log("[Notices Timer] started on " + str(self.Timer2) + " ms")             
        except:
            Util.Log("Something went wrong with calling timers!")

    def Settings(self):
        if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.AddSetting("Settings", "ChatName", "AutoBroadcaster")
            ini.AddSetting("Message", "Registered", "3")
            ini.AddSetting("Message", "Enable", "1")
            ini.AddSetting("Message", "Timer", "30")
            ini.AddSetting("Notice", "Registered", "3")
            ini.AddSetting("Notice", "Enable", "1")
            ini.AddSetting("Notice", "Timer", "30")
            ini.Save()
        return Plugin.GetIni("Settings")


    def Messages(self):
        if not Plugin.IniExists("Messages"):
            ini = Plugin.CreateIni("Messages")
            ini.AddSetting("Messages", "0", "Welcome to the server")
            ini.AddSetting("Messages", "1", "Please read the rules by typing /rules")
            ini.AddSetting("Messages", "2", "Dont be toxic")
            ini.Save()
        return Plugin.GetIni("Messages")

    def Notices(self):
        if not Plugin.IniExists("Notices"):
            ini = Plugin.CreateIni("Notices")
            ini.AddSetting("Notices", "0", "Welcome to the server")
            ini.AddSetting("Notices", "1", "To see all the commands type /help")
            ini.AddSetting("Notices", "2", "Please respect other players")
            ini.Save()
        return Plugin.GetIni("Notices")

    def Timer1Callback(self, timer):
        timer.Kill()
        ini = self.Messages()
        num = self.RegisteredMessages
        r = random.randrange(num)
        msg = ini.GetSetting("Messages", str(r))
        Server.BroadcastFrom(self.ChatName, msg)
        Plugin.CreateTimer("Timer1", self.Timer1).Start()

    def Timer2Callback(self, timer):
         timer.Kill()
         ini = self.Notices()
         num = self.RegisteredNotices
         r = random.randrange(num)
         msg = ini.GetSetting("Notices", str(r))
         Server.BroadcastNotice(msg)
         Plugin.CreateTimer("Timer2", self.Timer2).Start()





