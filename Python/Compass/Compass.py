__title__ = 'Allows a player to check his/her direction'
__author__ = 'ice cold'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

class Compass:
    Message = None

    def On_PluginInit(self):
        ini = self.Compass()
        self.Message = ini.GetSetting("Compass", "Message")

    def Compass(self):
    	if not Plugin.IniExists("Compass"):
    		com = Plugin.CreateIni("Compass")
    		com.AddSetting("Compass", "Message", "You are facing {direction}")
    		com.Save()
    	return Plugin.GetIni("Compass")

    def On_Command(self, Player, cmd, args):
    	if cmd == "compass":	
    		character = Player.PlayerClient.controllable.GetComponent("Character")
    		rot = character.eyesRotation.eulerAngles.y
    		direction = None

    		if rot > 337.5 or rot < 22.5:
    			direction = "North"
    		elif rot > 22.5 and rot < 67.5:	
    			direction = "North-East"
    		elif rot > 67.5 and rot < 112.5:
    			direction = "East"
    		elif rot > 112.5 and rot < 157.5:
    			direction = "South-East"
    		elif rot > 157.5 and rot < 202.5:   		   				
    		    direction = "South" 
    		elif rot > 202.5 and rot < 247.5:
    			direction = "South-West"
    		elif rot > 247.5 and rot < 292.5:
    			direction = "West"
    		elif rot > 292.5 and rot < 337.5:
    			direction = "North-West"

    		m = self.Message
    		m = m.Replace("{direction}", direction)
    		Player.MessageFrom("Compass", m)
