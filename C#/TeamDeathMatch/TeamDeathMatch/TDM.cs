using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Fougerite;
using Fougerite.Events;
using UnityEngine;
using System.IO;
using Random = System.Random;

namespace TeamDeathMatch
{
    public class Config
    {
        public Dictionary<string, object> Options;
        public Dictionary<string, string> Messages;
        public Dictionary<string, List<KitSetup>> Kits;
        public List<string> BlockedCommands;

        public Config Default()
        {
            Options = new Dictionary<string, object>()
            {
                {"Enabled", true },
                {"WaitTimer", 1.0 }, // 6 = 6 hours
                {"BattleTimer", 10.0 }, //10 = 10 minutes
                {"LobbyTimer", 30.0}, // 30 seconds
                {"MinPlayers", 5 },
                {"MaxPlayers", 20 },
                {"LobbyLocation", "" },
                {"BlueSpawn", "" },
                {"RedSpawn", "" }
            };
            Messages = new Dictionary<string, string>()
            {
                {"Disabled", "[color red]Sorry, our TDM plugin is currently disabled, please try again later" },
                {"NotRunning", "[color orange]There is not a TDM event yet" },
                {"IsRunning", "[color orange]There is a current match going on, please try next time" },
                {"IsFull", "[color orange]The lobby is full, please try again next time"},
                {"LobbyOpen", "[color green]THE TDM LOBBY IS NOW OPEN, TYPE /tdm join" },
                {"LobbyOpenNotice", "The TDM lobby is now open, type /tdm join" },
                {"LobbyJoin", "[color #7fffd4]{0} [color #6495ed] has entered the tdm lobby. [color yellow]{1} places left " },
                {"LobbyLeave", "[color orange]{0} [color yellow]has left the tdm lobby. [color aqua] {1} places left" },
                {"TeamRedJoin", "[color yellow]{0} [color orange]joined team [color red]RED!" },
                {"TeamBlueJoin", "[color yellow]{0} [color orange]joined team [color blue]BLUE!" },
                {"TeamJoinNotice", "You joined team {0}" },
                {"BattleStart", "[color green]The TDM battle has started" },
                {"DeathMessage", "[color #7fff00]{0} [color white]|{1}| [color #00b2ee]{2}" },
                {"SuicideMessage", "[color #7fff00]{0} [color white]SUICIDE!" }
            };
            BlockedCommands = new List<string>()
            {
                "tpr",
                "tpa",
                "home",
                "sethome",
                "kit"
            };

            Kits = new Dictionary<string, List<KitSetup>>
            {
                {"Blue", new List<KitSetup>(){new KitSetup("Kevlar Helmet", 1, 36), new KitSetup("Kevlar Vest", 1, 37), new KitSetup("Kevlar Pants", 1, 38), new KitSetup("Kevlar Boots", 1, 39), new KitSetup("M4", 1, 30), new KitSetup("Small Medkit", 5, 31), new KitSetup("Small Medkit", 5, 32), new KitSetup("Shotgun", 1, 33), new KitSetup("Cooked Chicken Breast", 20, 34), new KitSetup("556 Ammo", 250, 01), new KitSetup("Shotgun Shells", 50, 01), new KitSetup("Small Medkit", 20, 01)} },

                {"Red", new List<KitSetup>(){new KitSetup("Leather Helmet", 1, 36), new KitSetup("Leather Vest", 1, 37), new KitSetup("Leather Pants", 1, 38), new KitSetup("Leather Boots", 1, 39), new KitSetup("M4", 1, 30), new KitSetup("Large Medkit", 5, 31), new KitSetup("Large Medkit", 5, 32), new KitSetup("MP5A4", 1, 33), new KitSetup("Cooked Chicken Breast", 20, 34), new KitSetup("556 Ammo", 250, 01), new KitSetup("9mm Ammo", 250, 01), new KitSetup("Large Medkit", 20, 01)} },
            };

            return this;

        }
    }
    public class KitSetup
    {
        public string name;
        public int amount;
        public int slot;

        public KitSetup(string name, int amount, int slot)
        {
            this.name = name;
            this.amount = amount;
            this.slot = slot;
        }
    }

    public class TDM : Fougerite.Module
    {
        public TimerPlus WaitTimer;
        public TimerPlus LobbyTimer;
        public TimerPlus BattleTimer;

        public List<Fougerite.Player> RedPlayers;
        public List<Fougerite.Player> BluePlayers;
        public List<Fougerite.Player> InLobby;
        public Dictionary<ulong, List<PlayerInventorySafe>> Inventories;
        public Dictionary<ulong, Vector3> lastLoc;

        public bool IsOpen = false;

        public int BlueKills;
        public int RedKills;

        Server server = Server.GetServer();
        Util util = Util.GetUtil();
        DataStore ds = DataStore.GetInstance();

        public static Config config = new Config();
        public override void DeInitialize()
        {
            Hooks.OnCommand -= OnCommand;
            Hooks.OnPlayerKilled -= OnPlayerKilled;
            Hooks.OnPlayerDisconnected -= OnPlayerDisconnect;
            Hooks.OnPlayerSpawned -= OnPlayerSpawned;
            Hooks.OnServerLoaded -= OnServerLoaded;
            Hooks.OnPlayerHurt -= OnPlayerHurt;
        }

        public override void Initialize()
        {
            RedPlayers = new List<Fougerite.Player>();
            BluePlayers = new List<Fougerite.Player>();
            InLobby = new List<Fougerite.Player>();
            Inventories = new Dictionary<ulong, List<PlayerInventorySafe>>();
            lastLoc = new Dictionary<ulong, Vector3>();
            config = ReadyConfigChecked(config.Default(), "cfg_Configuration.json");
            Hooks.OnCommand += OnCommand;
            Hooks.OnPlayerKilled += OnPlayerKilled;
            Hooks.OnPlayerDisconnected += OnPlayerDisconnect;
            Hooks.OnPlayerSpawned += OnPlayerSpawned;
            Hooks.OnServerLoaded += OnServerLoaded;
            Hooks.OnPlayerHurt += OnPlayerHurt;
        }

        private void OnPlayerHurt(HurtEvent he)
        {
            if(he.AttackerIsPlayer && he.VictimIsPlayer)
            {
                if (InLobby.Contains((Fougerite.Player)he.Victim))
                {
                    he.DamageAmount = 0;

                }
            }
           
        }

        private void OnPlayerKilled(DeathEvent de)
        {
            if(de.AttackerIsPlayer && de.VictimIsPlayer)
            {
                Fougerite.Player attacker = (Fougerite.Player)de.Attacker;
                Fougerite.Player victim = (Fougerite.Player)de.Victim;
                string weapon = de.WeaponName;
                if(attacker != victim)
                {
                    string message = string.Format(config.Messages["DeathMessage"], attacker.Name, weapon, victim.Name);
                    if(BluePlayers.Contains(victim))
                    {
                        BlueKills--;
                        RedKills++;
                        this.EventBroadcast(message);
                    }
                    else if(RedPlayers.Contains(victim))
                    {
                        RedKills--;
                        BlueKills++;
                        this.EventBroadcast(message);

                    }
                }
                else if(BluePlayers.Contains(victim) || RedPlayers.Contains(victim))
                {
                    string message = string.Format(config.Messages["SuicideMessage"], victim.Name);
                    this.EventBroadcast(message);
                }
            }
        }

        private void OnPlayerDisconnect(Fougerite.Player player)
        {
            if(BluePlayers.Contains(player) || RedPlayers.Contains(player) || InLobby.Contains(player))
            {
                BluePlayers.Remove(player);
                RedPlayers.Remove(player);
                InLobby.Remove(player);
                Inventories.Remove(player.UID);
                player.Kill();
                ds.Add("InEvent", player.SteamID, false);
            }
        }

        private void OnPlayerSpawned(Fougerite.Player player, SpawnEvent se)
        {
            if (BluePlayers.Contains(player))
            {
                player.TeleportTo(util.ConvertStringToVector3(config.Options["BlueSpawn"].ToString()));
                this.GiveBlueKit(player);
            }
                
            if(RedPlayers.Contains(player))
            {
                player.TeleportTo(util.ConvertStringToVector3(config.Options["RedSpawn"].ToString()));
                this.GiveRedKit(player);
            }
                

        }

        private void OnCommand(Fougerite.Player player, string cmd, string[] args)
        {
            if(cmd == "tdm")
            {
                if(args.Length == 0)
                {
                    player.Notice("ϟ", "TDM Created by ice cold");
                    player.MessageFrom(Name, "[color #c1ffc1]***************************************************************");
                    player.MessageFrom(Name, "[color #ffbbff]/tdm join - [color #4eee94]join the event");
                    player.MessageFrom(Name, "[color #ffbbff]/tdm status -[color #4eee94] Status about current match");
                    player.MessageFrom(Name, "[color #ffbbff]/tdm info - [color #4eee94]Info about TDM Plugin");
                    player.MessageFrom(Name, "[color #ffbbff]/tdm kit teamname[red/blue] - [color #4eee94]See the team kits");
                    player.MessageFrom(Name, "[color #ffbbff]/tdm players - [color #4eee94]Shows all players");
                    player.MessageFrom(Name, "[color #c1ffc1]***************************************************************");
                }
                else
                {
                    string arg = args[0];
                    if(arg == "join")
                    {
                        if ((bool)config.Options["Enabled"])
                        {
                            if (IsOpen)
                            {
                                if (InLobby.Count < (int)config.Options["MaxPlayers"])
                                {
                                    //todo joins the lobby, save inventory etc
                                    lastLoc.Add(player.UID, player.Location);
                                    this.SafePlayerInventory(player);
                                    player.TeleportTo(util.ConvertStringToVector3(config.Options["LobbyLocation"].ToString()));
                                    int leftp = Math.Abs(InLobby.Count - (int)config.Options["MaxPlayers"]);
                                    server.BroadcastFrom(Name, string.Format(config.Messages["LobbyJoin"], player.Name, leftp));
                                    ds.Add("InEvent", player.SteamID, true);
                                    this.BlockCommands(player);
                                }
                                else
                                    player.MessageFrom(Name, config.Messages["IsFull"]);

                            }
                            else
                                player.MessageFrom(Name, config.Messages["NotRunning"]);
                        }
                        else
                            player.MessageFrom(Name, config.Messages["NotRunning"]);
                    }
                    if(arg == "status")
                    {
                        player.MessageFrom(Name, "[color orange]RedTeam: " + RedPlayers.Count + " players");
                        player.MessageFrom(Name, "[color orange]BlueTeam: " + BluePlayers.Count + " players");
                    }
                    if(arg == "info")
                    {
                        player.MessageFrom(Name, "Welcome to TDM \n This is a event plugin that allow's 2 teams (blue & Red) to fight eachother inside a arena, The team that has the most kills wins and gets a reward");
                    }
                    if(arg == "kits")
                    {
                        if (string.IsNullOrEmpty(args[1]))
                        {
                            player.MessageFrom(Name, "[color #ffbbff]Syntax /tdm kit red");
                            player.MessageFrom(Name, "[color #ffbbff]Syntax /tdm kit blue");
                        }
                        else if(args[1] == "red")
                        {
                            foreach(var x in config.Kits["Red"])
                            {
                                player.MessageFrom(Name, "[color #54ff9f]" + x.name + " | " + x.amount);
                            }
                        }
                        else if(args[1] == "blue")
                        {
                            foreach (var x in config.Kits["Blue"])
                            {
                                player.MessageFrom(Name, "[color #54ff9f]" + x.name + " | " + x.amount);
                            }
                        }
                    
                    }
                    if(arg == "players")
                    { 
                        string message = "[color #ff7256]RED TEAM:[color #c1ffc1] ";
                        foreach (var pl in RedPlayers)
                        {
                            message += pl.Name + ", ";
                        }
                        player.MessageFrom(Name, message);

                        string message2 = "[color #8deeee] BLUE TEAM: [color #ffd700] ";
                        foreach (var pl in BluePlayers)
                        {
                            message2 += pl.Name + ", ";
                        }
                        player.MessageFrom(Name, message2);
                    }
                    if(arg == "forcestart")
                    {
                        if(player.Admin)
                        {
                            WaitTimer.Stop();
                            WaitTimer.Close();
                            this.StartLobbyTimer();
                            server.BroadcastFrom(Name, player.Name + " [color orange] has force start the TDM event");

                        }
                    }
                }
            }
        }

      
        private void OnServerLoaded()
        {
            WaitTimer = new TimerPlus();
            WaitTimer.Interval = double.Parse(config.Options["WaitTimer"].ToString()) * 3600000.0;
            WaitTimer.AutoReset = false;
            WaitTimer.Enabled = true;
            WaitTimer.Elapsed += (x, y) =>
            {
               
                this.StartLobbyTimer();
            };
        }
        private void BlockCommands(Fougerite.Player player)
        {
            foreach (string cmd in config.BlockedCommands)
                player.RestrictCommand(cmd);
        }
        private void UnblockCommands(Fougerite.Player player)
        {
            foreach (string cmd in config.BlockedCommands)
                player.UnRestrictCommand(cmd);
        }
        private void StartLobbyTimer()
        {
            IsOpen = true;
            server.BroadcastFrom(Name, config.Messages["LobbyOpen"]);
            this.NoticeAll(config.Messages["LobbyOpenNotice"]);
            LobbyTimer = new TimerPlus();
            LobbyTimer.Interval = double.Parse(config.Options["LobbyTimer"].ToString()) * 1000.0;
            LobbyTimer.AutoReset = false;
            LobbyTimer.Enabled = true;
            LobbyTimer.Elapsed += (j, u) =>
            {
                IsOpen = false;
                foreach(var pl in InLobby)
                {
                    if (Math.Abs(RedPlayers.Count - BluePlayers.Count) > 1)
                    {
                        pl.TeleportTo(util.ConvertStringToVector3(config.Options["RedSpawn"].ToString()));
                        RedPlayers.Add(pl);
                        InLobby.Remove(pl);
                        server.BroadcastFrom(Name, string.Format(config.Messages["TeamRedJoin"], pl.Name));
                        this.GiveRedKit(pl);
                    }
                    else
                    {
                        pl.TeleportTo(util.ConvertStringToVector3(config.Options["BlueSpawn"].ToString()));
                        BluePlayers.Add(pl);
                        InLobby.Remove(pl);
                        server.BroadcastFrom(Name, string.Format(config.Messages["TeamBlueJoin"], pl.Name));
                        this.GiveBlueKit(pl);

                    }
                }
                server.BroadcastFrom(Name, config.Messages["BattleStart"]);
                this.NoticeAll("TDM has started");
                RedKills = 0;
                BlueKills = 0;
                this.StartBattleTimer();
                
            };
        }

        private void StartBattleTimer()
        {
            BattleTimer = new TimerPlus();
            BattleTimer.Interval = double.Parse(config.Options["BattleTimer"].ToString()) * 60000;
            BattleTimer.AutoReset = false;
            BattleTimer.Enabled = true;
            BattleTimer.Elapsed += (x, y) =>
            {
                this.EndMatch();
                string winning_team = string.Empty;
                string endmessage = $"Team {winning_team} has won the TDM event, Congratulations";
                if (BlueKills > RedKills)
                    winning_team = "blue";
                else
                    winning_team = "red";
                if (BlueKills == RedKills)
                    endmessage = "Both teams have same amount of kills, NONE WINS";
                this.NoticeAll(endmessage);
                server.BroadcastFrom(Name, "[color #c1ffc1]****************************[color #ff8c00]Match Score [color #c1ffc1] ***********************************");
                server.BroadcastFrom(Name, $"[color #c1ffc1]Team blue: {BlueKills} kills!");
                server.BroadcastFrom(Name, $"[color #c1ffc1]Team red: {RedKills} kills!");
                server.BroadcastFrom(Name, $"[color #c1ffc1]Kill diffrence: {Math.Abs(BlueKills - RedKills)}");
                server.BroadcastFrom(Name, "[color #c1ffc1]****************************[color #ff8c00]Match Score [color #c1ffc1] ***********************************");
                server.BroadcastFrom(Name, "[color orange]Next event starts in " + (int)config.Options["WaitTimer"] + " Hours");
                RedKills = 0;
                BlueKills = 0;
                this.OnServerLoaded();

                
            };
        }

        private void EndMatch()
        {
            foreach(var pl in server.Players.Where(x => BluePlayers.Contains(x) || RedPlayers.Contains(x)))
            {
                this.ReturnInventory(pl);
                Vector3 loc = lastLoc[pl.UID];
                pl.TeleportTo(loc);
                RedPlayers.Remove(pl);
                BluePlayers.Remove(pl);
                ds.Add("InEvent", pl.SteamID, false);
                this.UnblockCommands(pl);

            }
        }

        private void GiveBlueKit(Fougerite.Player pl)
        {
            pl.Inventory.ClearAll();
            foreach (var kit in config.Kits["Blue"])
            {
                string name = kit.name;
                int amount = kit.amount;
                int slot = kit.slot;
                pl.Inventory.AddItemTo(name, slot, amount);

            }
        }

        private void GiveRedKit(Fougerite.Player pl)
        {
            pl.Inventory.ClearAll();
            foreach (var kit in config.Kits["Red"])
            {
                string name = kit.name;
                int amount = kit.amount;
                int slot = kit.slot;
                pl.Inventory.AddItemTo(name, slot, amount);

            }
        }

        private void NoticeAll(string v)
        {
            foreach(var pl in server.Players.Where(x => x.IsOnline))
            {
                pl.Notice("☢", v, 10);
            }
        }
        private void SafePlayerInventory(Fougerite.Player pl)
        {
            foreach(var item in pl.Inventory.Items.Where(x => !x.IsEmpty()))
            {
                if (!Inventories.ContainsKey(pl.UID))
                {
                    Inventories.Add(pl.UID, new List<PlayerInventorySafe> { new PlayerInventorySafe(item.Name, item.Slot, item.Quantity) });
                }
                else
                    Inventories[pl.UID].Add(new PlayerInventorySafe(item.Name, item.Slot, item.Quantity));
            }
            foreach(var item in pl.Inventory.ArmorItems.Where(x => !x.IsEmpty()))
            {
                Inventories[pl.UID].Add(new PlayerInventorySafe(item.Name, item.Slot, item.Quantity));
            }
            foreach (var item in pl.Inventory.BarItems.Where(x => !x.IsEmpty()))
            {
                Inventories[pl.UID].Add(new PlayerInventorySafe(item.Name, item.Slot, item.Quantity));
            }
            pl.Inventory.ClearAll();

        }
        public void ReturnInventory(Fougerite.Player player)
        {
            if(Inventories.ContainsKey(player.UID))
            {
                player.Inventory.ClearAll();
                foreach(var item in Inventories[player.UID])
                {
                    player.Inventory.AddItemTo(item.name, item.slot, item.amount);
                }
                Inventories.Remove(player.UID);
            }
        }
        public void EventBroadcast(string message)
        {
            foreach(var pl in server.Players.Where(x => BluePlayers.Contains(x) || RedPlayers.Contains(x)))
            {
                pl.MessageFrom("TDM-Death", message);
            }
        }
        public T ReadyConfigChecked<T>(T obj, string pathFile)
        { 
            try
            {
                if (File.Exists(GetAbsoluteFilePath(pathFile)))
                {
                    return JsonHelper.ReadyFile<T>(GetAbsoluteFilePath(pathFile));
                }
                else
                {
                    JsonHelper.SaveFile(obj, GetAbsoluteFilePath(pathFile));
                    return obj;
                }
            }
            catch (Exception ex)
            {
                Logger.LogError("Error path: " + pathFile + "Error: " + ex);
                return default(T);
            }

        }
        public string GetAbsoluteFilePath(string fileName)
        {
            return Path.Combine(ModuleFolder, fileName);
        }
        public override string Name => "TDM";
        public override string Author => "ice cold";
        public override string Description => "Let 2 teams fight eachother for a reward";
        public override Version Version => new Version("1.0");

    }
    public class PlayerInventorySafe
    {
        public string name;
        public int slot;
        public int amount;
        public PlayerInventorySafe(string name, int slot, int amount)
        {
            this.name = name;
            this.amount = amount;
            this.slot = slot;
        }
    }

}
