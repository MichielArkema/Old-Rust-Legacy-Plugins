__title__ = 'AdminMode'
__author__ = 'ice cold'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

sysname = "AdminOn"
green = "[color green]"
red = "[color red]"

class AdminMode:
    Broadcast = None
    BMessage = None
    BMessage2 = None
    AllowMods = None
    InstaInvis = None

    def On_PluginInit(self):
        ini = self.AdminConfig()
        self.AdminHelp()
        self.StaffList()
        self.Broadcast = int(ini.GetSetting("Options", "Broadcast"))  
        self.AllowMods = int(ini.GetSetting("Options", "AllowMods"))
        self.InstaInvis = int(ini.GetSetting("Options", "InstaInvis"))
        self.BMessage2 = ini.GetSetting("Options", "BMessage2")
        self.BMessage = ini.GetSetting("Options", "BMessage")


    def AdminConfig(self):
        if not Plugin.IniExists("AdminConfig"):
            ini = Plugin.CreateIni("AdminConfig")
            ini.AddSetting("Options", "Broadcast", "1")
            ini.AddSetting("Options", "AllowMods", "0")
            ini.AddSetting("Options", "InstaInvis", "1")
            ini.AddSetting("Options", "BMessage", "{0} is now in admin mode")
            ini.AddSetting("Options", "BMessage2", "{0} is now out of admin mode")    
            ini.AddSetting("Items", "Uber Hunting Bow", "1")
            ini.AddSetting("Items", "Uber Hatchet", "1")
            ini.AddSetting("Items", "Arrow", "40")
            ini.AddSetting("Items", "Large Medkit", "20")
            ini.Save()
        return Plugin.GetIni("AdminConfig")

    def AdminHelp(self):
        if not Plugin.IniExists("AdminHelp"):
            helper = Plugin.CreateIni("AdminHelp")
            helper.AddSetting("Help", "1", "HELP1")
            helper.AddSetting("Help", "2", "HELP2")
            helper.AddSetting("Help", "3", "HELP3")
            helper.Save()
        return Plugin.GetIni("AdminHelp")

    def StaffList(self):
        if not Plugin.IniExists("StaffList"):
            helper = Plugin.CreateIni("StaffList")
            helper.AddSetting("Staff", "1", "STAFF1")
            helper.AddSetting("Staff", "2", "STAFF2")
            helper.AddSetting("Staff", "3", "STAFF3")
            helper.Save()
        return Plugin.GetIni("StaffList")


        
    def On_Command(self, Player, cmd, args):
        if cmd == "adminon":
            if Player.Admin or Player.Moderator and self.AllowMods == 1:
                self.recordInventory(Player)
                self.giveadmintools(Player)
                if self.Broadcast == 1:
                    m = self.BMessage
                    m = m.Replace("{0}", Player.Name)
                    Server.BroadcastFrom("AdminMode", m)
                Player.Notice("Admin mode on")
            else:
                Player.Message("You dont have permissions to use this command")
        elif cmd == "adminoff":
              if Player.Admin or Player.Moderator and self.AllowMods == 1:
                  Player.Notice("Admin mode off")
                  self.returnInventory(Player)
                  if self.Broadcast == 1:
                      m = self.BMessage2
                      m = m.Replace("{0}", Player.Name)
                      Server.BroadcastFrom("AdminMode", m)
              else:
                  Player.Message("You dont have permissions to use this command")
        elif cmd == "changename":
            if Player.Admin or Player.Moderator and self.AllowMods == 1:
                if len(args) == 0:
                    Player.Notice("Syntax use /changename Name")
                    Player.Name = "SERVER CONSOLE"
                    return
                text = self.argsToText(args)
                Player.Name = text
        elif cmd == "adminhelp":
            if Player.Admin or Player.Moderator and self.AllowMods == 1:
                helper = self.AdminHelp()
                enum = helper.EnumSection("Help")
                for list in enum:
                    l = helper.GetSetting("Help", list)
                    Player.MessageFrom("AdminHelp", l)
        elif cmd == "staff":
            staff = self.StaffList()
            enum = staff.EnumSection("Staff")
            for list in enum:
                l = staff.GetSetting("Staff", list)
                Player.MessageFrom("Stafflist", l)




    def giveadmintools(self, Player):
        if Player.Admin or Player.Moderator and self.AllowMods == 1:
            if self.InstaInvis == 1:
                Player.Inventory.AddItemTo("Invisible Helmet", 36, 1)
                Player.Inventory.AddItemTo("Invisible Vest", 37, 1)
                Player.Inventory.AddItemTo("Invisible Pants", 38, 1)
                Player.Inventory.AddItemTo("Invisible Boots", 39, 1)
            ini = self.AdminConfig()
            enum = ini.EnumSection("Items")
            for items in enum:
                amount = int(ini.GetSetting("Items", items))
                Player.Inventory.AddItem(items, amount)



    def recordInventory(self, Player):
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

        DataStore.Add("readdinv", id, Inventory)
        DataStore.Save()
        Player.Inventory.ClearAll()

    def returnInventory(self, Player):
        id = Player.SteamID
        if DataStore.ContainsKey("readdinv", id):
            Inventory = DataStore.Get("readdinv", id)
            Player.Inventory.ClearAll()
            for dictionary in Inventory:
                if dictionary['name'] is not None:
                    Player.Inventory.AddItemTo(dictionary['name'], dictionary['slot'], dictionary['quantity'])
                else:
                    Player.MessageFrom(sysname, red + "No dictionary found in the for cycle?!")
            Player.MessageFrom(sysname, green + "Your have received your original inventory")
            DataStore.Remove("readdinv", id)
        else:
            Player.MessageFrom(sysname, red + "No Items of your last inventory found!")

    def argsToText(self, args):
        text = str.join(" ", args)
        return text




            
