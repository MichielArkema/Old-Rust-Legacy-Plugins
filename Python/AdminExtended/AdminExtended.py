__title__ = 'AdminExtended'
__author__ = 'ice cold'
__version__ = '1.0.'

# THIS PLUGIN IS BETTER AND STILL UNDER DEV > https://github.com/icecolderino/fougerite-plugins/blob/master/Fougmin.py

import clr
clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import Fougerite

yellow = "[color #FFFF00]"
red = "[color #FF0000]"
green = "[color #009900]"
sysname = "AdminExtended"

class AdminExtended:
    
    Enable = None
    AdminGather = None
    GiveAdminLoadoutOnSpawn = None

    def On_PluginInit(self):
        Util.ConsoleLog( __title__ +" by " + __author__ + " Version: " + __version__ + " loaded.", False)
        ini = self.Settings()
        self.Enable = int(ini.GetSetting("Settings", "Enable"))
        self.AdminGather = int(ini.GetSetting("Settings", "AdminGather"))
        self.GiveAdminLoadoutOnSpawn = int(ini.GetSetting("Settings", "GiveAdminLoadoutOnSpawn"))

    def Settings(self):
        if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.AddSetting("Settings", "Enable", "1")
            ini.AddSetting("Settings", "AdminGather", "1")
            ini.AddSetting("Settings", "GiveAdminLoadoutOnSpawn", "0")
            ini.Save()               
        return Plugin.GetIni("Settings")

    def GetPlayerName(self, namee):
        try:
            name = namee.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

    def CheckV(self, Player, args):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.join(" ", args))
            if p is not None:
                return p
            for pl in Server.Players:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            nargs = str(args).lower()
            p = self.GetPlayerName(nargs)
            if p is not None:
                return p
            for pl in Server.Players:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            if Player is not None:
                Player.MessageFrom(sysname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            if Player is not None:
                Player.MessageFrom(sysname, "Found [color#FF0000]" + str(count) +
                                   "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def GetIt(self, Entity):
        try:
            if Entity.IsDeployableObject():
                return Entity.Object.ownerID
            if Entity.IsStructure():
                return Entity.Object._master.ownerID
        except:
            return None

    def On_Command(self, Player, cmd, args):
        if cmd == "ma":
            if self.Enable == 1:
                if Player.Admin:
                    if len(args) == 0:
                          Player.MessageFrom(sysname, yellow + "AdminExtended by [color green]ice cold [color aqua]Version [color yellow]1.0")
                          Player.MessageFrom(sysname, yellow + "/ma owner - go into owner view mode type /owner again to disable it")
                          Player.MessageFrom(sysname, yellow + "/ma - to see commands")
                          Player.MessageFrom(sysname, yellow + "/ma tp <Name>")
                          Player.MessageFrom(sysname, yellow + "/ma bring <Name> - brings the player to you")
                          Player.MessageFrom(sysname, yellow + "/ma return - brings you back to your last location")
                          Player.MessageFrom(sysname, yellow + "/ma loadout - gives loadout")
                          Player.MessageFrom(sysname, yellow + "/ma invis - Gives you an Invisible suit")
                          Player.MessageFrom(sysname, yellow + "/ma invisoff - Removes invisible suit")
                          Player.MessageFrom(sysname, yellow + "/ma vanish - Turn into ghost mode")
                          Player.MessageFrom(sysname, yellow + "/ma vanishoff - Back to normal Human")
                          Player.MessageFrom(sysname, yellow + "/ma doors - Enable admin doors")
                          Player.MessageFrom(sysname, yellow + "/ma doorsoff - Disable admin doors")
                          Player.MessageFrom(sysname, yellow + "/ma remove - Turns on admin remove mode")
                          Player.MessageFrom(sysname, yellow + "/ma removeoff - Disable Admin remove mode")
                          Player.MessageFrom(sysname, yellow + "/ma stp - teleports you to the entity you hit")
                          Player.MessageFrom(sysname, yellow + "/ma hp <Name>- Check someones Health")
                          Player.MessageFrom(sysname, yellow + "/ma savepoint - Saves 1 point where you stand")
                          Player.MessageFrom(sysname, yellow + "/ma usepoint - tp to the saved point")
                          Player.MessageFrom(sysname, yellow + "/ma gameid <Name> - shows soemone his ID")
                          Player.MessageFrom(sysname, yellow + "/ma ipad <Name> - see seomeone his Ip Addres")
                          Player.MessageFrom(sysname, yellow + "/ma timeonline <Name> - See how long someone is playing on t")
                          return
                    else:
                        arg = args[0]
                        if arg == "tp":
                            if Player.Admin or Player.Moderator:
                                playerr = self.CheckV(Player, args)
                                if playerr is None:
                                    return
                                else:
                                    ini = self.Settings()
                                    Player.TeleportTo(playerr.Location)
                                    Player.MessageFrom(sysname, yellow + "You have been teleported to " + playerr.Name)
                                    Plugin.Log("Teleport", Player.Name + " Has Teleported to " + playerr.Name)
                                    DataStore.Add("Return Location", Player.SteamID, Player.Location)
                                    return
                        elif arg == "loadout":
                            if Player.Admin:
                                Player.Inventory.RemoveItem(36);
                                Player.Inventory.RemoveItem(37);
                                Player.Inventory.RemoveItem(38);
                                Player.Inventory.RemoveItem(39);
                                Player.Inventory.AddItemTo("Kevlar Helmet", 36, 1);
                                Player.Inventory.AddItemTo("Kevlar Vest", 37, 1);
                                Player.Inventory.AddItemTo("Kevlar Pants", 38, 1);
                                Player.Inventory.AddItemTo("Kevlar Boots", 39, 1);
                                Player.Inventory.AddItem("M4", 1);
                                Player.Inventory.AddItem("P250", 1);
                                Player.Inventory.AddItem("556 Ammo", 250);
                                Player.Inventory.AddItem("9mm Ammo", 250);
                                Player.MessageFrom(sysname, yellow + "Loadout spawned")
                                Plugin.Log("Loadout", Player.Name + " has used the loadout command")
                                return
                        elif arg == "doors":
                            if Player.Admin:
                                DataStore.Add("madoor", Player.SteamID, "madoor")                                
                                Player.MessageFrom(sysname, yellow + "Admin doors activated")
                                Plugin.Log("Doors", Player.Name + " has used the Doors command")
                                return
                        elif arg == "doorsoff":
                            if Player.Admin:
                                DataStore.Remove("madoor", Player.SteamID)
                                Player.MessageFrom(sysname, yellow + "Admin doors Deactivated")
                                Plugin.Log("Doors", Player.Name + " has used the doorsoff command")
                                return
                        elif arg == "invis":
                            if Player.Admin or Player.Moderator:
                                 Player.Inventory.RemoveItem(36)
                                 Player.Inventory.RemoveItem(37)
                                 Player.Inventory.RemoveItem(38)
                                 Player.Inventory.RemoveItem(39)
                                 Player.Inventory.AddItemTo("Invisible Helmet", 36, 1)
                                 Player.Inventory.AddItemTo("Invisible Vest", 37, 1)
                                 Player.Inventory.AddItemTo("Invisible Pants", 38, 1)
                                 Player.Inventory.AddItemTo("Invisible Boots", 39, 1)
                                 Player.MessageFrom(sysname, yellow + "You are now Invisible")
                                 Plugin.Log("Invis", Player.Name + " has used the invis command")
                                 DataStore.Add("InvisEnable", Player.SteamID, "on")
                                 return
                        elif arg == "invisoff":
                            if Player.Admin or Player.Moderator:
                                 Player.Inventory.RemoveItem(36)
                                 Player.Inventory.RemoveItem(37)
                                 Player.Inventory.RemoveItem(38)
                                 Player.Inventory.RemoveItem(39)
                                 Player.MessageFrom(sysname, yellow + "You are back to visible mode")
                                 Plugin.Log("Invis", Player.Name + " has used the invisoff command")
                                 DataStore.Remove("InvisEnable", Player.SteamID)
                                 return
                        elif arg == "vanishoff":
                            if Player.Admin:
                                if Player.PlayerClient.controllable.health == 0.0:
                                    Player.Health = 100
                                    Player.Notice("☢", "Your soul has been returned into your body")
                                    Plugin.Log("Vanish", Player.Name + " has used the vanishoff command")
                                    return
                        elif arg == "vanish":
                            if Player.Admin:
                                Player.Health = Player.PlayerClient.controllable.health - Player.PlayerClient.controllable.health
                                Player.Notice("☢", "You are now a ghosty boo")
                                Plugin.Log("Vanish", Player.Name + " has used the vanish command")
                                return
                        elif arg == "remove":
                            if Player.Admin or Player.Moderator:
                                DataStore.Add("MaRemove", Player.SteamID, "Maremover")
                                Player.MessageFrom(sysname, yellow + "Admin remove mode enable hit an object to remove it")
                                Plugin.Log("Remover", Player.Name + " has used the remove command")
                                return
                        elif arg == "removeoff":
                            if Player.Admin or Player.Moderator:
                                DataStore.Remove("MaRemove", Player.SteamID)
                                Player.MessageFrom(sysname, yellow + "Admin Remover tool disabled")
                                Plugin.Log("Remover", Player.Name + " has used the removeoff command")
                        elif arg == "bring":
                            if Player.Admin or Player.Moderator:
                                playerr = self.CheckV(Player, args)
                                if playerr is None:
                                    return
                                else:
                                    DataStore.Add("Bringer", playerr.SteamID, playerr.Location)
                                    playerr.TeleportTo(Player.Location)
                                    playerr.MessageFrom(sysname, yellow + "You have been teleported to " + Player.Name)
                                    Player.MessageFrom(sysname, yellow + "You have brought " + playerr.Name + " to you ")
                                    Plugin.Log("Bring", Player.Name + " Has Brought " + playerr.Name + " to him")                                   
                                    return                             
                        elif arg == "owner":
                            if Player.Admin:
                                id = Player.SteamID
                                if not DataStore.ContainsKey("OwnerMode", id):
                                    Player.MessageFrom(sysname, yellow + "Owner view tool enabled  hit an object to see the owner type /owner again to disable it")
                                    DataStore.Add("OwnerMode", id, "true")
                                else:
                                    DataStore.Remove("OwnerMode", id)
                                    Player.MessageFrom(sysname, yellow + "Owner view tool disabled")
                        elif arg == "stp":
                            if Player.Admin:
                                if not DataStore.ContainsKey("stp", Player.SteamID):
                                    Player.MessageFrom(sysname, yellow + "Shoot an object to teleport to it")
                                    DataStore.Add("stp", Player.SteamID, "stp")
                                else:
                                    Player.MessageFrom(sysname, yellow + "Shoot teleport disabled")
                                    DataStore.Remove("stp", Player.SteamID)
                                    return
                        elif arg == "hp":
                            if Player.Admin:
                                playerr = self.CheckV(Player, args)
                                if playerr is None:
                                    return
                                else:
                                    Player.MessageFrom(sysname, yellow + playerr.Name + " his health is " + green + "" + str(playerr.Health))
                                    return
                        elif arg == "ipad":
                            if Player.Admin:
                                playerr = self.CheckV(Player, args)
                                if playerr is None:
                                    return
                                else:
                                    Player.MessageFrom(sysname, yellow + playerr.Name + "His ip is " + green + "" + playerr.IP)
                                    return
                        elif arg == "return":
                            if Player.Admin:
                                if DataStore.Get("Return Location", Player.SteamID):
                                    returner = DataStore.Get("Return Location", Player.SteamID)
                                    Player.TeleportTo(returner)
                                    Player.MessageFrom(sysname, green + "You been returned to your last point")
                                    DataStore.Remove("Return Location", Player.SteamID)
                                else:
                                    Player.MessageFrom(sysname, red + "No returning point found")
                                    return
                        elif arg == "savepoint":
                            if Player.Admin:
                                if not DataStore.ContainsKey("Points", Player.SteamID):
                                    DataStore.Add("Points", Player.SteamID, Player.Location)
                                    Player.MessageFrom(sysname, green + "Point saved at " + yellow + str(Player.Location))
                                else:
                                    Player.MessageFrom(sysname, red + "There is already 1 point saved please use him before setting new one")
                                    return
                        elif arg == "usepoint":
                            if Player.Admin:
                                if DataStore.ContainsKey("Points", Player.SteamID):       
                                    pointer = DataStore.Get("Points", Player.SteamID)
                                    Player.TeleportTo(pointer)
                                    Player.MessageFrom(sysname, yellow + "Teleported")
                                    DataStore.Remove("Points", Player.SteamID)
                                else:                              
                                    Player.MessageFrom(sysname, red + "Error: failed to found saved point type /ma savepoint to set one")
                                    return
                        elif arg == "gameid":
                            if Player.Admin:
                                playerr = self.CheckV(Player, args)
                                if playerr is None:
                                    return
                                else:
                                    Player.MessageFrom(sysname, yellow + playerr.Name + " His GameID is " + green + playerr.GameID)
                        elif arg == "timeonline":
                            if Player.Admin:
                                playerr = self.CheckV(Player, args)
                                if playerr is None:
                                    return
                                else:
                                    Player.MessageFrom(sysname, yellow + playerr.Name + " Is online for " + green + str(playerr.TimeOnline))      
                                                  
                        
    def On_DoorUse(self, Player, DoorUseEvent):
        if DataStore.Get("madoor", Player.SteamID):
            if Player.Admin:
                Player.MessageFrom(sysname, green + "Door used")
                DoorUseEvent.Open = True

  
    def On_PlayerGathering(self, Player, GatherEvent):
        if self.AdminGather == 1:
            if Player.Admin:
                if GatherEvent.Item == "Wood":  
                     Player.Inventory.AddItem(GatherEvent.Item, 50)
                     Player.MessageFrom(sysname, yellow + "You have got an extra 50[color aqua] " + GatherEvent.Item)
                     return
                elif GatherEvent.Item == "Sulfer Ore":
                    Player.Inventory.AddItem(GatherEvent.Item, 50)
                    Player.MessageFrom(sysname, yellow + "You have got an extra 50[color aqua] " + GatherEvent.Item)
                    return
                elif GatherEvent.Item == "Metal Ore":
                    Player.Inventory.AddItem(GatherEvent.Item, 50)
                    Player.MessageFrom(sysname, yellow + "You have got an extra 50[color aqua] " + GatherEvent.Item)
                    return
                elif GatherEvent.Item == "Stones":
                    Player.Inventory.AddItem(GatherEvent.Item, 50)
                    Player.MessageFrom(sysname, yellow + "You have got an extra 50[color aqua] " + GatherEvent.Item)

    def On_PlayerSpawned(self, Player, SpawnEvent):
        if self.GiveAdminLoadoutOnSpawn == 1:
            if Player.Admin:
                Player.Inventory.RemoveItem(36);
                Player.Inventory.RemoveItem(37);
                Player.Inventory.RemoveItem(38);
                Player.Inventory.RemoveItem(39);
                Player.Inventory.AddItemTo("Kevlar Helmet", 36, 1);
                Player.Inventory.AddItemTo("Kevlar Vest", 37, 1);
                Player.Inventory.AddItemTo("Kevlar Pants", 38, 1);
                Player.Inventory.AddItemTo("Kevlar Boots", 39, 1);
                Player.Inventory.AddItem("M4", 1);
                Player.Inventory.AddItem("P250", 1);
                Player.Inventory.AddItem("556 Ammo", 250);
                Player.Inventory.AddItem("9mm Ammo", 250);
                Player.MessageFrom(sysname, yellow + "Loadout spawned")
                return
            elif DataStore.get("InvisEnable", Player.SteamID):
                DataStore.Remove("InvisEnable", Player.SteamID)

              

    def On_EntityHurt(self, HurtEvent):
        if DataStore.Get("MaRemove", HurtEvent.Attacker.SteamID):
            if HurtEvent.Attacker.Admin:
                if HurtEvent.Entity.Name is not None:
                    loc = str(HurtEvent.Entity.Location)
                    weapon = str(HurtEvent.WeaponName)
                    HurtEvent.Entity.Destroy()
                    HurtEvent.Attacker.MessageFrom(sysname, red + "You have removed a " + HurtEvent.Entity.Name)
                    Plugin.Log("Removed Objects", HurtEvent.Attacker.Name + " has removed " + HurtEvent.Entity.Name + " With admin remover tool with an " + weapon + " at " + loc)
                    return
        elif HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay:
            if not HurtEvent.AttackerIsPlayer:
                return
            id = HurtEvent.Attacker.SteamID
            OwnerID = HurtEvent.Entity.OwnerID
            if DataStore.ContainsKey("OwnerMode", HurtEvent.Attacker.SteamID):
                gun = HurtEvent.WeaponName
                if gun == "Shotgun":
                    return
                HurtEvent.DamageAmount = 0
                if not Server.HasRustPP:
                    return
                dict = Server.GetRustPPAPI().Cache
                if dict.ContainsKey(long(OwnerID)):
                    name = dict[long(OwnerID)]
                    HurtEvent.Attacker.MessageFrom(sysname, yellow + HurtEvent.Entity.Name + " is owned by " + name + ".")
                else:
                    HurtEvent.Attacker.MessageFrom(sysname, yellow + HurtEvent.Entity.Name + " is owned by " + OwnerID + ".")
                    return
        elif DataStore.Get("stp", HurtEvent.Attacker.SteamID):
            if HurtEvent.Attacker.Admin:
                en = HurtEvent.Entity.Location
                HurtEvent.Attacker.TeleportTo(en)
                HurtEvent.Attacker.MessageFrom(sysname, red + "Teleported")


    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.VictimIsPlayer and HurtEvent.AttackerIsPlayer:
            if DataStore.Get("InvisEnable", HurtEvent.Attacker.SteamID):
                HurtEvent.DamageAmount = 0
                HurtEvent.Victim.MessageFrom(sysname, red + HurtEvent.Attacker.Name + " Is trying to kill you while hes invisible We wil prevent damage")
                HurtEvent.Attacker.MessageFrom(sysname, red + " You cant kill players while you are invisible")

    def On_PlayerDisconnected(self, Player):
        if DataStore.Get("InvisEnable", Player.SteamID):
            DataStore.Remove("InvisEnable", Player.SteamID)

                                                                                         
