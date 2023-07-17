__title__ = 'ping'
__author__ = 'ice cold'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

class Ping:
    
    def On_Command(self, Player, cmd, args):
        if cmd == "ping":
            Player.Notice("☢", "Your Ping is " + str(Player.Ping))
            Player.MessageFrom("Ping", "[color aqua]Your ping is[color yellow] " + str(Player.Ping))
            Player.InventoryNotice("Ping " + str(Player.Ping))