__title__ = 'SaveSpawnLoadout'
__author__ = 'ice cold'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

class SaveSpawnLoadout:
    GiveOnSpawn = None
    Enabled = None

    def On_PluginInit(self):
        ini = self.Settings()
        self.giveonspawn = int(ini.GetSetting("Settings", "GiveOnSpawn"))
        self.enabled = int(ini.GetSetting("Settings", "Enabled"))

    def Settings(self):
        if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.AddSetting("Settings", "GiveOnSpawn", "1")
            ini.AddSetting("Settings", "Enabled", "1")
            ini.AddSetting("Messages", "SaveMessage", "Your inventory has been succesfully saved")
            ini.AddSetting("Messages", "ReceiveMessage", "You have received your inventory loadout")
            ini.AddSetting("Notices", "SaveNotice", "Your inventory has been saved")
            ini.AddSetting("Notices", "ReceiveNotice", "Inventory received")
            ini.AddSetting("RestrictMessage", "ResM", "You cannot save your inventory when you have the followed items C4, Grenada, Supply signal")
            ini.AddSetting("InfoMessage", "info", "Type /ssl to get info about how to save your inventory")
            ini.Save()
        return Plugin.GetIni("Settings")

    def On_Command(self, Player, cmd, args):
        if cmd == "ssl":
            if self.enabled == 1:
                if self.giveonspawn == 1:
                    Player.Message("/saveinv saves your inventory so you receive it on spawn")
                else:
                    Player.Message("/saveinv saves your inventory")
                    Player.Message("/getinv Receives your saved inventory")
            else:
                Player.Message("Sorry this plugin is currently disabled please ask the owner of the server for more info")
        elif cmd == "saveinv":
            if self.enabled == 1:
                if not Player.Inventory.HasItem("Explosive Charge") and not Player.Inventory.HasItem("F1 Grenada") and not Player.Inventory.HasItem("Supply Signal") :
                    ini = self.Settings()
                    save = ini.GetSetting("Messages", "SaveMessage")
                    saven = ini.GetSetting("Notices", "SaveNotice")
                    Player.Message(save)
                    Player.Notice(saven)
                    self.saveInventory(Player)
                else:
                    ini = self.Settings()
                    m = ini.GetSetting("RestrictMessage", "ResM")
                    Player.Message(m)
            else:
                Player.Message("Sorry this plugin is currently disabled please ask the owner of the server for more info")
        elif cmd == "getinv":
            if self.enabled == 1:
                if self.giveonspawn == 0:
                    ini = self.Settings()
                    getm = ini.GetSetting("Messages", "ReceiveMessage")
                    getn = ini.GetSetting("Notices", "ReceiveNotice")
                    Player.Message(getm)
                    Player.Notice(getn)
                    self.getInventory(Player)
                else:
                    Player.Message("You wil receive your inventory when you spawn")
            else:
                Player.Message("Sorry this plugin is currently disabled please ask the owner of the server for more info")

    def On_PlayerSpawned(self, Player, SpawnEvent):
        if self.enabled == 1:
            if self.giveonspawn == 1:
                ini = self.Settings()
                getm = ini.GetSetting("Messages", "ReceiveMessage")
                getn = ini.GetSetting("Notices", "ReceiveNotice")
                Player.Message(getm)
                Player.Notice(getn)
                self.getInventory(Player)

    def On_PlayerConnected(self, Player):
        if self.enabled == 1:
            ini = self.Settings()
            info = ini.GetSetting("InfoMessage", "info")
            Player.Message(info)

    def On_PlayerDisconnected(self, Player):
        id = Player.SteamID
        if DataStore.ContainsKey("saveinventory", id):
            DataStore.Remove("saveinventory", id)


    # dretax his methods below

    def saveInventory(self, Player):
        Inventory = []
        id = Player.SteamID
        for Item in Player.Inventory.Items:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)
        for Item in Player.Inventory.ArmorItems:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)
        for Item in Player.Inventory.BarItems:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)

        DataStore.Add("saveinventory", id, Inventory)
        DataStore.Save()

    def getInventory(self, Player):
        id = Player.SteamID
        if DataStore.ContainsKey("saveinventory", id):
            Inventory = DataStore.Get("saveinventory", id)
            Player.Inventory.ClearAll()
            for dictionary in Inventory:
                if dictionary['name'] is not None:
                    Player.Inventory.AddItemTo(dictionary['name'], dictionary['slot'], dictionary['quantity'])
                else:
                    Player.MessageFrom("No Inventory found!")          
           
 






