__title__ = 'HitMarker'
__author__ = 'ice cold'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class HitMarker:
    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.VictimIsPlayer and HurtEvent.AttackerIsPlayer: # if hurteven blablbla wil make sure the attacker is a player and not a animal
		    HurtEvent.Attacker.InventoryNotice("You hit " + HurtEvent.Victim.Name)
