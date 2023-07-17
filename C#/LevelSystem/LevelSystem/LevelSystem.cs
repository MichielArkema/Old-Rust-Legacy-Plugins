using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Fougerite;
using UnityEngine;
using System.IO;
using Fougerite.Events;
using System.Timers;

namespace LevelSystem
{
    public class Config
    {
        public double activityReward;
        public double autoRewardTime;
        public double gatherXP;

        public Dictionary<string, object> killOptions;
        public Dictionary<string, object> gatherOptions;
        public Dictionary<string,string> messages;

        public Config Default()
        {
            activityReward = 15.0;
            autoRewardTime = 30.0;
            gatherXP = 0.5;
            killOptions = new Dictionary<string, object>()
            {
                { "killerxp", 10.0 },
                { "victimxp", 10.0 },
                { "NPCKillxp", 3.0 }
            };         
            messages = new Dictionary<string, string>()
            {
                { "KillReceive",  "You received {0} xp for a kill {1}" },
                { "DeathReduce", "You lost {0} xp for dying" },
                { "ActivityReward", "You have rewarded {0} xp for activity" },
                { "UnlockMessage", "You can unlock a {0} for {1} xp" },
                { "LevelUpMessage", "You've leveled up to level {0}, Type /unlockable to see the list of your unlockable blueprints" },
                { "LevelupBroadcast", "{0} has leveled up to level {1}" },
                { "LevelupNotice", "Congratulations, you have been leveled up!" },
                { "CantUnlock", "You have not unlocked this blueprint yet!" },
                { "Unlocked", "You have unlocked {0} for {1} xp" },
                { "NotEnoughtXP", "You do not have enough xp to unlock this blueprint" },
                { "NotABluePrint", "You can only unlock blueprints with xp" }
            };




            return this;
        }
    }

    public class LevelSystem : Module
    {
        public static LevelSystem instance;
        public static Config config = new Config();
        private const string darksea = "[color 	#b4eeb4]";
        private const string plum = "[color #ffbbff]";
        private const string seagreen = "[color #4eee94]";

        public Dictionary<int, LevelProps> levels;
        public Dictionary<string, PlayerLevelProps> playerlevels;

        Server server = Server.GetServer();

        public override string Name
        {
            get { return "LevelSystem"; }

        }
        public override string Author
        {
            get { return "ice cold"; }
        }
        public override string Description
        {
            get { return "Allows people to unlock features and blueprints"; }
        }
        public override Version Version
        {
            get { return new Version("1.0"); }
        }
        public override void Initialize()
        {
            instance = this;
            levels = new Dictionary<int, LevelProps>();
            playerlevels = new Dictionary<string, PlayerLevelProps>();

            Hooks.OnChatRaw += OnCommand;
            Hooks.OnPlayerGathering += OnGather;
            Hooks.OnNPCKilled += NPCKilled;
            Hooks.OnPlayerKilled += OnPlayerKilled;
            Hooks.OnServerSaved += OnSave;
            Hooks.OnPlayerConnected += OnPlayerConnected;
            Hooks.OnServerShutdown += OnServerShutdown;
            config = ReadyConfigChecked(config.Default(), "cfg_Configuration.json");
            if (!File.Exists(Path.Combine(ModuleFolder, "cfg_Levels.json")))
            {
                levels.Add(0, new LevelProps(0.0F, "Rookie", new Dictionary<string, object>()));              
                levels.Add(1, new LevelProps(50.0F, "Basic", new Dictionary<string, object> {
                    { "kit", null },
                    { "kits", null },
                    { "remove", null }
                }));
                levels.Add(2, new LevelProps(100.0F, "Starter", new Dictionary<string, object>
                {
                    { "home", null },
                    { "tpr", null },
                    { "kit:starter", null },
                    { "remove", null }
                }));
                levels.Add(3, new LevelProps(200.0F, "Hunter", new Dictionary<string, object>
                {
                    { "kit:home", null },
                    { "kit:hunter", null },
                    { "Revolver Blueprint", 30.0F},
                    { "Leather Helmet BP",  50.0F},
                    { "Pick Axe Blueprint",  15.0F}
                }));
                levels.Add(4, new LevelProps(300.0F, "Novice", new Dictionary<string, object>
                {
                    { "repair", null },
                    { "paperwork", null },
                    { "Shotgun Blueprint", 80.0F },
                    { "Leather Vest BP", 50.0F }
                }));
                levels.Add(5, new LevelProps(400.0F, "Killer", new Dictionary<string, object>
                {
                    { "Leather Pants BP", 55.0F },
                    { "Leather Boots BP", 50.0F},
                    { "P250 Blueprint", 60.0F }
                }));
             
                
            }
            levels = ReadyConfigChecked(levels, "cfg_Levels.json");
            playerlevels = ReadyConfigChecked(playerlevels, "db_PlayerLevels.json");

            StartActivityTimer();


        }

        private void StartActivityTimer()
        {
            Timer timer = new Timer();
            timer.AutoReset = true;
            timer.Interval = (double)config.autoRewardTime * 60000;
            timer.Enabled = true;
            timer.Elapsed += (x, y) =>
            {
                foreach(var pl in server.Players)
                {
                    if(playerlevels.ContainsKey(pl.SteamID))
                    {
                        playerlevels[pl.SteamID].xp += (double)config.activityReward;
                        this.CheckForPlayerUpdate(pl);
                    }
                }
            };
        }

        private void NPCKilled(DeathEvent de)
        {
            if(de.AttackerIsPlayer && de.VictimIsNPC)
            {
                Fougerite.Player attacker = (Fougerite.Player)de.Attacker;
                NPC victim = (NPC)de.Victim;
                if(playerlevels.ContainsKey(attacker.SteamID))
                {
                    if(playerlevels.ContainsKey(attacker.SteamID))
                    {
                        attacker.MessageFrom(Name, string.Format(config.messages["KillReceive"], config.killOptions["NPCKillxp"], victim.Name));
                        playerlevels[attacker.SteamID].xp += (double)config.killOptions["NPCKillxp"];
                        this.CheckForPlayerUpdate(attacker);
                    }
                }
            }
        }

        private void OnServerShutdown()
        {
            JsonHelper.SaveFile(levels, GetAbsoluteFilePath("cfg_Levels.json"));
            JsonHelper.SaveFile(playerlevels, GetAbsoluteFilePath("db_PlayerLevels.json"));
        }

        private void OnPlayerConnected(Fougerite.Player player)
        {
            if(!playerlevels.ContainsKey(player.SteamID))
            {
                playerlevels.Add(player.SteamID, new PlayerLevelProps(0.0F, 0, "Rookie", new Dictionary<string, object>()));
                player.MessageFrom(Name, "You are now level Rookie");
            }
        }

        private void OnSave(int Amount, double Seconds)
        {
            JsonHelper.SaveFile(levels, GetAbsoluteFilePath("cfg_Levels.json"));
            JsonHelper.SaveFile(playerlevels, GetAbsoluteFilePath("db_PlayerLevels.json"));
        }

        private void OnPlayerKilled(DeathEvent de)
        {
            if(de.AttackerIsPlayer && de.VictimIsPlayer)
            {
                Fougerite.Player attacker = (Fougerite.Player)de.Attacker;
                Fougerite.Player victim = (Fougerite.Player)de.Victim;

                if(attacker != victim)
                {
                    if(playerlevels.ContainsKey(attacker.SteamID) && playerlevels.ContainsKey(victim.SteamID))
                    {
                        attacker.MessageFrom(Name, string.Format(config.messages["KillReceive"], config.killOptions["NPCKillxp"], victim.Name));
                        playerlevels[attacker.SteamID].xp += (double)config.killOptions["killerxp"];

                        if(this.CanTakePlayerXp(victim, (double)config.killOptions["victimxp"]))
                            playerlevels[victim.SteamID].xp -= (double)config.killOptions["victimxp"];


                        this.CheckForPlayerUpdate(attacker);

                    }
                }
            }
        }

       

        private void OnGather(Fougerite.Player player, GatherEvent ge)
        {
            if(playerlevels.ContainsKey(player.SteamID))
            {

                playerlevels[player.SteamID].xp += config.gatherXP;
                this.CheckForPlayerUpdate(player);
            }       
        }

        private void CheckForPlayerUpdate(Fougerite.Player player)
        {
            string id = player.SteamID;
            double xp = playerlevels[id].xp;
            int level = playerlevels[id].level;
            var playerunlocks = playerlevels[id].unlocked;
            if(levels.ContainsKey(level + 1))
            {
                level += 1;
                var newlevel = levels[level];
                if(xp == newlevel.xp || xp >= newlevel.xp)
                {
                    playerlevels[id].level = level;
                    playerlevels[id].levelName = newlevel.levelName;
                  
                    player.Notice("★", config.messages["LevelupNotice"]);
                    player.MessageFrom(Name, string.Format(config.messages["LevelUpMessage"], newlevel.levelName));
                    server.BroadcastFrom(Name, string.Format(config.messages["LevelupBroadcast"], player.Name, level));

                    foreach(KeyValuePair<string, object> pair in levels[level].unlockable)
                    {
                        playerlevels[player.SteamID].unlocked.Add(pair.Key, pair.Value);
                    }


                }
            }
        }

        private void OnCommand(ref ConsoleSystem.Arg ChatArgument)
        {
            if (ChatArgument.argUser == null) return;

            Fougerite.Player player = Server.GetServer().FindByNetworkPlayer(ChatArgument.argUser.networkPlayer);
            string[] arg = Facepunch.Utility.String.SplitQuotesStrings(ChatArgument.GetString(0).Trim());
            string cmd = arg[0].Trim().ToLower();
            if (!cmd.StartsWith("/")) return;
            if (arg.Length < 2) arg = new string[0]; else { Array.Copy(arg, 1, arg, 0, arg.Length - 1); Array.Resize(ref arg, arg.Length - 1); }
            if (cmd == "/level")
            {
                player.Notice("★", $"LevelSystem {Version}  by {Author}");
                player.MessageFrom(Name, seagreen + "******************** [color orange]Level System " + seagreen + "********************");
                player.MessageFrom(Name, darksea + "Syntax: /stats - See your current level status");
                player.MessageFrom(Name, darksea + "Syntax: /levels - See how many levels are available");
                player.MessageFrom(Name, darksea + "Syntax: /unlock blueprint - Unlock a blueprint for XP");
                player.MessageFrom(Name, darksea + "Syntax: /unlockable - See the list of your current unlockable blueprints");
                player.MessageFrom(Name, seagreen + "******************** [color orange]Level System " + seagreen + "********************");

            }
            if(cmd == "/unlock")
            {
                if(arg.Length == 1)
                {
                    string itemname = arg[0];
                    var dict = playerlevels[player.SteamID].unlocked;

                    if(dict.ContainsKey(itemname))
                    {
                        if(dict[itemname] != null)
                        {
                            double costs = (double)dict[itemname];
                            if(this.CanTakePlayerXp(player, costs))
                            {
                                playerlevels[player.SteamID].xp -= costs;
                                player.Inventory.AddItem(itemname, 1);
                                player.MessageFrom(Name, string.Format(config.messages["Unlocked"], itemname, costs));
                            }
                            else
                            {
                                player.MessageFrom(Name, string.Format(config.messages["NotEnoughtXP"]));
                            }
                            
                        }
                        else
                        {
                            player.MessageFrom(Name, string.Format(config.messages["NotABluePrint"]));
                        }
                    }
                    else
                    {
                        player.MessageFrom(Name, string.Format(config.messages["CantUnlock"]));
                    }
                }
            }
            if(cmd == "/unlockable")
            {
                if(playerlevels[player.SteamID].unlocked.Count == 0)
                {
                    player.MessageFrom(Name, "[color orange]You have not unlocked any blueprints yet!");
                    return;
                }
                player.MessageFrom(Name, seagreen + "******************** [color orange]Unlockable Blueprints " + seagreen + "********************");
                foreach (KeyValuePair<string,object> pair in playerlevels[player.SteamID].unlocked)
                {
                    var dict = playerlevels[player.SteamID].unlocked;
                    if(pair.Key.Contains("BP") || pair.Key.Contains("Blueprint"))
                    {
                        player.MessageFrom(Name, string.Format(config.messages["UnlockMessage"], pair.Key, dict[pair.Key]));
                    }
                }
                player.MessageFrom(Name, seagreen + "******************** [color orange]Unlockable Blueprints " + seagreen + "********************");
            }
            if(cmd == "/stats")
            {
                player.MessageFrom(Name, seagreen + "******************** [color orange]Your Stats " + seagreen + "********************");
                player.MessageFrom(Name, plum + "XP: " + seagreen + playerlevels[player.SteamID].xp);
                player.MessageFrom(Name, plum + "Level: " + seagreen + playerlevels[player.SteamID].levelName);
                player.MessageFrom(Name, plum + "levelNumber: " + seagreen + playerlevels[player.SteamID].level);
                player.MessageFrom(Name, plum + "NextLevel: " + seagreen + levels[playerlevels[player.SteamID].level + 1].levelName + " XPNeeded: " + Math.Abs(playerlevels[player.SteamID].xp - levels[playerlevels[player.SteamID].level + 1].xp));
                player.MessageFrom(Name, seagreen + "******************** [color orange]Your Stats " + seagreen + "********************");
            }
            if(cmd == "/levels")
            {
                player.MessageFrom(Name, seagreen + "******************** [color orange]Levels " + seagreen + "********************");
                foreach (KeyValuePair<int, LevelProps> pair in levels)
                {
                    if (playerlevels[player.SteamID].level == pair.Key)
                    {
                        player.MessageFrom(Name, plum + "LEVEL: " + pair.Key + " (" + pair.Value.levelName + ") XP: " + pair.Value.xp + " [color orange] (YOUR LEVEL)");
                        continue;
                    }
                    player.MessageFrom(Name, plum + "LEVEL: " + pair.Key + " (" + pair.Value.levelName + ") XP: " + pair.Value.xp);
                }
                player.MessageFrom(Name, seagreen + "******************** [color orange]Levels " + seagreen + "********************");
            }
        }

        public bool CanTakePlayerXp(Fougerite.Player player, double price)
        {
            double  xp = playerlevels[player.SteamID].xp;
          
            if(xp - price < 0.0)
            {
                return false;
            }
            else
            {
                return true;
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

        public override void DeInitialize()
        {
            Hooks.OnChatRaw -= OnCommand;
            Hooks.OnPlayerGathering -= OnGather;
            Hooks.OnNPCKilled -= NPCKilled ;
            Hooks.OnPlayerKilled -= OnPlayerKilled;
            Hooks.OnServerSaved -= OnSave;
        }

        public class PlayerLevelProps
        {
            public double xp;
            public int level;
            public string levelName;
            public Dictionary<string, object> unlocked;

            public PlayerLevelProps(double xp, int level, string levelName, Dictionary<string, object>unlocked)
            {
                this.xp = xp;
                this.level = level;
                this.levelName = levelName;
                this.unlocked = unlocked;
            }

        }
        public class LevelProps
        {
            public double xp;
            public string levelName;
            public Dictionary<string, object> unlockable = new Dictionary<string, object>();

            public LevelProps(double xp, string level, Dictionary<string, object>unlockable)
            {
                this.xp = xp;
                this.levelName = level;
                this.unlockable = unlockable;
            }



        }

    }
    
}
