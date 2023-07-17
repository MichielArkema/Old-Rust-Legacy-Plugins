__title__ = 'firstjoin message'
__author__ = 'ice cold'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

class FirstJoin:
	def On_PluginInit(self):
		self.Database()

	def Database(self):
		if not Plugin.IniExists("Database"):
			ini = Plugin.CreateIni("Database")
			ini.Save()
		return Plugin.GetIni("Database")

	def On_PlayerConnected(self, Player):
		ini = self.Database()
		if ini.GetSetting("Joined", Player.SteamID) is None:
			Server.Broadcast(Player.Name + "[color 	#bf3eff] Has joined the server for the first time")
			ini.AddSetting("Joined", Player.SteamID, "1")
			ini.Save()
