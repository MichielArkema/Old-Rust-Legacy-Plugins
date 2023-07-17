__title__ = 'ShelterBlock'
__author__ = 'ice cold'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

    
class ShelterBlock:
    def On_PluginInit(self):
        Util.ConsoleLog("ShelterBlocker by " + __author__ + " Version: " + __version__ + " loaded.", False)

		
    def On_EntityDeployed(self, Player, Entity, ActualPlacer):
        if Entity.Name == "Wood_Shelter":
            Entity.Destroy()
            ActualPlacer.Inventory.AddItem("Wood Shelter")
            ActualPlacer.InventoryNotice("1 x Wood Shelter")
            ActualPlacer.Notice("✘", "To prevent lag we have disabled shelters!")
