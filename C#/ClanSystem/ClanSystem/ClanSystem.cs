using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Fougerite;
using Fougerite.Events;
using LevelSystem;
using System.IO;
using UnityEngine;
using System.Timers;

namespace ClanSystem
{
    public class Config
    {
        public int clanLimit;
        public int nameLimit;
        public double XP;
        public double TeleportDelay;
        public double TeleportCooldown;
        public Dictionary<string, string> Messages;

        public Config Default()
        {
            clanLimit = 6;
            nameLimit = 6;
            XP = 30.0;
            TeleportDelay = 20.0;
            TeleportCooldown = 360.0;
            Messages = new Dictionary<string, string>()
            {
                { "ClanCreate", "{0} has created the clan {1}" },
                { "ClanInvite", "{0} has invited you to join his clan {1}, type /clan accept to join" },
                { "ClanInviteSend", "You have succesfully invited {0} to join your clan" },
                { "ClanDisband", "{0} has disbanded the clan {1}" },
                { "FriendlyFire", "Stop shooting!! this {0} is in your clan" },
                { "ClanFF", "FriendlyFire has been set to {0}" },
                { "IsInClan", "You're already inside a clan" },
                { "InviteFail", "{0} is already inside a clan" },
                { "InviteFail2", "You are not invited for a clan" },
                { "InviteAccepted", "{0} has joined the clan" },
                { "ClanLeave", "{0} has left the clan" },
                { "NotInClan", "You do not have a clan" },
                { "ClanBaseSet", "{0} has set the clan base at {1}" },
                { "BaseTeleport", "You wil be teleported to can base in {0} seconds" },
                { "BaseCooldown", "You are under cooldown for {0} seconds" },
                { "ClanFull", "Your clan is full, you cannot invite anymore people" },
                { "NoClanBase", "The owner hasn't set a clan base yet" }

            };
            return this;
        }
    }
    public class ClanSystem : Module
    {
        public static ClanSystem instance;
        public static Config config = new Config();
        public Dictionary<string, ClanProps> Clans;
        public Dictionary<string, string> Invites;
        public Dictionary<string, double> Cooldown;

        private const string aqua = "[color #7fffd4]";
        private const string coral = "[color #ff7256]";
        private const string cyan = "[color #00eeee]";
        private const string salmon = "[color #e9967a]";
        private const string marine = "[color #7fffd4]";

        Server server = Server.GetServer();
        Util util = Util.GetUtil();



        public override void Initialize()
        {
            instance = this;
            Clans = new Dictionary<string, ClanProps>();
            Invites = new Dictionary<string, string>();
            Cooldown = new Dictionary<string, double>();

            config = ReadyConfigChecked(config.Default(), "cfg_Configuration.json");
            Clans = ReadyConfigChecked(Clans, "db_Clans.json");

            Hooks.OnChatRaw += OnCommand;
            Hooks.OnServerSaved += OnServerSave;
            Hooks.OnServerShutdown += OnServerShutdown;
            Hooks.OnPlayerConnected += OnPlayerConnected;

        }

        private void OnPlayerConnected(Fougerite.Player player)
        {
            if(this.HasClan(player) || this.IsInClan(player))
            {
                string clan = this.GetClanOfPlayer(player.SteamID);
                player.Name = $"[{clan}]" + player.Name;
            }
            
        }

        private void OnServerShutdown()
        {
            JsonHelper.SaveFile(Clans, GetAbsoluteFilePath("db_Clans.json"));
        }

        private void OnServerSave(int Amount, double Seconds)
        {
            JsonHelper.SaveFile(Clans, GetAbsoluteFilePath("db_Clans.json"));
        }

        private void OnCommand(ref ConsoleSystem.Arg ChatArgument)
        {
            if (ChatArgument.argUser == null) return;

            Fougerite.Player player = Server.GetServer().FindByNetworkPlayer(ChatArgument.argUser.networkPlayer);
            string[] arg = Facepunch.Utility.String.SplitQuotesStrings(ChatArgument.GetString(0).Trim());
            string cmd = arg[0].Trim().ToLower();
            if (!cmd.StartsWith("/")) return;
            if (arg.Length < 2) arg = new string[0]; else { Array.Copy(arg, 1, arg, 0, arg.Length - 1); Array.Resize(ref arg, arg.Length - 1); }

            if(cmd == "/clan")
            {
                if(arg.Length == 0)
                {
                    player.Notice("✪", $"ClanSystem {Version} by {Author}");
                    player.MessageFrom(Name, aqua + $"*********************** [color orange]Clan System {aqua} ***********************");
                    player.MessageFrom(Name, coral + "Syntax: /clan create ClanName - Creates a clan");
                    player.MessageFrom(Name, coral + "Syntax: /clan invite playername - Invites a player to your clan");
                    player.MessageFrom(Name, coral + "Syntax: /clan accept - Accept a clan invite");
                    player.MessageFrom(Name, coral + "Syntax: /clan setbase - Sets a clan base (1 MAX)");
                    player.MessageFrom(Name, coral + "Syntax: /clan home - Teleports you to the clan base");
                    player.MessageFrom(Name, coral + "Syntax: /clan config option optionvalue - Set/change a config value in your clan");
                    player.MessageFrom(Name, coral + "Syntax: /clan members - See the list of people in your clan");
                    player.MessageFrom(Name, coral + "Syntax: /clan kick playername - Kicks the player from your clan");
                    player.MessageFrom(Name, coral + "Syntax: /clan chat \"Message\" - Kicks the player from your clan");
                    player.MessageFrom(Name, coral + "Syntax: /clan call - Call help in clan chat with the location");
                    player.MessageFrom(Name, coral + "Syntax: /clan leave - Leave the clan you're currently in");
                    player.MessageFrom(Name, coral + "Syntax: /clan disband - Disband(Delete) your whole clan");
                    player.MessageFrom(Name, aqua + $"*********************** [color orange]Clan System {aqua} ***********************");
                    return;
                }
                if(arg[0] == "create" && arg.Length == 2)
                {
                    if(!string.IsNullOrEmpty(arg[1]))
                    {
                        if(!Clans.ContainsKey(arg[1]))
                        {
                            if (!this.HasClan(player))
                            {
                                if (!this.IsInClan(player))
                                {
                                    Clans.Add(arg[1], new ClanProps(player.SteamID, 0, "Welcome to the clan", string.Empty, new List<string>() { player.SteamID }));
                                    server.BroadcastFrom(Name, string.Format(config.Messages["ClanCreate"], player.Name, arg[1]));
                                    player.Name = "[" + arg[1] + "]" + player.Name;
                                }
                                else
                                    player.MessageFrom(Name, string.Format(config.Messages["IsInClan"]));

                            }
                            else
                                player.MessageFrom(Name, string.Format(config.Messages["IsInClan"]));
                        }
                        else
                        {
                            player.Notice("✘", "The name " + arg[1] + "is already occupied", 5F);
                        }
                    }
                }
                if(arg[0] == "invite" && arg.Length == 2)
                {
                    if(!string.IsNullOrEmpty(arg[1]))
                    {
                        Fougerite.Player target = server.FindPlayer(arg[1]);
                        if(target == null) { player.Message("[color red]Couldn't find the target user"); return; }
                        if(target == player) { player.Message("[color red]You cannot invite yourself"); return; }
                        string clan = this.GetClanOfPlayer(player.SteamID);
                        if(Clans[clan].members.Count == config.clanLimit) { player.MessageFrom(Name, config.Messages["ClanFull"]); return; }
                        if (this.HasClan(player))
                        {
                            if (!this.IsInClan(target) && !this.HasClan(target))
                            {
                                if(Invites.ContainsKey(target.SteamID)) { Invites.Remove(target.SteamID); }
                                player.Message(string.Format(config.Messages["ClanInviteSend"], target.Name));
                                target.MessageFrom(Name, string.Format(config.Messages["ClanInvite"], player.Name, this.FindClanOfOwnerID(player.SteamID)));
                                Invites.Add(target.SteamID, (string)this.FindClanOfOwnerID(player.SteamID));
                            }
                            else
                                player.MessageFrom(Name, string.Format(config.Messages["InviteFail"], target.Name));
                        }
                        else
                            player.MessageFrom(Name, config.Messages["NotInClan"]);

                    }
                }
                if(arg[0] == "accept")
                {
                    if(Invites.ContainsKey(player.SteamID))
                    {
                        this.AddPlayerToMemberList(player.SteamID, Invites[player.SteamID]);
                        SendClanMessage(Invites[player.SteamID], $"[{Invites[player.SteamID]}]", string.Format(config.Messages["InviteAccepted"], this.GetPlayerNameByID(player.SteamID)));
                        Invites.Remove(player.SteamID);

                    }
                    else
                    {
                        player.MessageFrom(Name, config.Messages["InviteFail2"]);
                    }
                }
                if(arg[0] == "chat" && arg.Length == 2)
                {
                    if(this.IsInClan(player) || this.HasClan(player))
                    {
                        string clan = this.GetClanOfPlayer(player.SteamID);                      
                        SendClanMessage(clan, player.Name, "[color 	#ffd39b]" + arg[1]);
                        player.MessageFrom($"[CHAT]{player.Name}", "[color #ffd39b]" + arg[1]);
                    }
                }
                if(arg[0] == "setbase")
                {
                    if(this.HasClan(player))
                    {
                        if(player.AtHome)
                        {
                            string clan = (string)this.FindClanOfOwnerID(player.SteamID);
                            Clans[clan].clanbase = player.Location.ToString();
                            player.Notice("✪", "Succesfully set the clan base at " + player.Location);
                            SendClanMessage(clan, Name, string.Format(config.Messages["ClanBaseSet"], player.Name, player.Location.ToString()));
                        }
                        else
                        {
                            player.Notice("✘", "You can only set a clan base at structure that belongs to you", 5F);
                        }
                      
                    }
                    else
                        player.MessageFrom(Name, config.Messages["NotInClan"]);
                }
                if(arg[0] == "home")
                {
                    if(this.HasClan(player) || this.IsInClan(player))
                    {
                        if (!string.IsNullOrEmpty(Clans[this.GetClanOfPlayer(player.SteamID)].clanbase))
                        {
                            if (Cooldown.ContainsKey(player.SteamID))
                            {
                                double calc = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds - Cooldown[player.SteamID];
                                if (calc < config.TeleportCooldown)
                                {
                                    player.MessageFrom(Name, string.Format(config.Messages["BaseCooldown"], Math.Round(Math.Abs(calc - config.TeleportCooldown))));
                                    return;
                                }
                            }
                            Cooldown.Remove(player.SteamID);
                            ClanProps clan = Clans[this.GetClanOfPlayer(player.SteamID)];
                            player.MessageFrom(Name, string.Format(config.Messages["BaseTeleport"], config.TeleportDelay));

                            StartClanBaseTeleportDelay(player, clan);
                        }
                        else
                            player.MessageFrom(Name, config.Messages["NoClanBase"]);
                        
                    }
                    else
                        player.MessageFrom(Name, config.Messages["NotInClan"]);

                }
                if(arg[0] == "leave")
                {
                    if(!this.HasClan(player))
                    {
                        if(this.IsInClan(player))
                        {
                            string clan = this.GetClanOfPlayer(player.SteamID);
                            Clans[clan].members.Remove(player.SteamID);
                            player.Name = player.Name.Replace("[" + clan + "]", string.Empty);
                            this.SendClanMessage(clan, clan, string.Format(config.Messages["ClanLeave"], player.Name));

                        }
                        else
                            player.MessageFrom(Name, config.Messages["NotInClan"]);

                    }
                    else
                        player.Notice("✪", "Your the owner of the clan, use /clan disband instead");
                }
                if(arg[0] == "members")
                {
                    if(this.HasClan(player)|| this.IsInClan(player))
                    {
                        ClanProps clan = Clans[this.GetClanOfPlayer(player.SteamID)];
                        player.MessageFrom(Name, aqua + $"*********************** [color orange]Clan Members {aqua} ***********************");
                        player.MessageFrom(Name, cyan + $"Members: {aqua}{clan.members.Count}|{config.clanLimit}");
                        int count = 0;
                        foreach(string id in clan.members)
                        {
                            count++;
                            string name = (string)this.GetPlayerNameByID(id);                            
                            Fougerite.Player pl = server.FindPlayer(name);
                            string c = this.GetClanOfPlayer(pl.SteamID);
                            name = name.Replace($"[{c}]", string.Empty);
                            if(pl.IsOnline)
                            {
                                player.MessageFrom(Name, cyan + $"{count}: {salmon}{name} {marine}(ONLINE)");
                            }
                            else
                            {
                                player.MessageFrom(Name, cyan + $"{count}: {salmon}{name} [color red](OFFLINE)");
                            }
                            
                        }
                        count = 0;
                        player.MessageFrom(Name, aqua + $"*********************** [color orange]Clan Members {aqua} ***********************");

                    }
                }
                if(arg[0] == "config")
                {
                    ClanProps clan = Clans[this.GetClanOfPlayer(player.SteamID)];
                    if(arg.Length == 1)
                    {
                        player.MessageFrom(Name, aqua + $"*********************** [color orange]Clan Members {aqua} ***********************");
                        player.MessageFrom(Name, cyan + "Option: " + marine + "Description = " + clan.description);
                        player.MessageFrom(Name, cyan + "Option: " + marine + "FF = " + clan.FF);
                        player.MessageFrom(Name, aqua + $"*********************** [color orange]Clan Members {aqua} ***********************");
                    }
                    else if(arg.Length == 3)
                    {
                        if (arg[1] == "Description")
                        {
                            clan.description = arg[2];
                            player.MessageFrom(Name, cyan + "Clan Description has been set to " + arg[2]);
                        }
                        if(arg[1] == "FF")
                        {
                            int set;
                            if(int.TryParse(arg[2], out set))
                            {
                                clan.FF = set;
                                player.MessageFrom(Name, cyan + "Clan Description has been set to " + set);
                            }
                            else
                            {
                                player.Notice("✘", "Please choose the number 0 or 1", 5F);
                            }
                        }
                            
                        
                    }
                }
                if(arg[0] == "kick" && arg.Length == 2)
                {
                    if(this.HasClan(player))
                    {
                        Fougerite.Player target = server.FindPlayer(arg[1]);
                        if(target == null) { player.MessageFrom(Name, "[color red]Couldn't find the target user"); return; }
                        if(this.GetClanOfPlayer(player.SteamID) == this.GetClanOfPlayer(target.SteamID))
                        {
                            string clan = this.GetClanOfPlayer(target.SteamID);
                            Clans[clan].members.Remove(target.SteamID);
                            target.Name = target.Name.Replace("[" + clan + "]", string.Empty);
                            this.SendClanMessage(clan, clan, string.Format(config.Messages["ClanLeave"], target.Name));
                        }
                        else
                        {
                            player.Notice("✘", target.Name + " Is not in your clan");
                        }
                    }
                }
                if(arg[0] == "disband")
                {
                    if(this.HasClan(player))
                    {
                        string clanname = (string)this.FindClanOfOwnerID(player.SteamID);
                        if(!string.IsNullOrEmpty(clanname))
                        {
                            foreach(string id in Clans[clanname].members)
                            {
                                Fougerite.Player pl = this.FindMemberById(id);
                                if(pl != null)
                                {                                   
                                    pl.Name = pl.Name.Replace("[" + clanname + "]", string.Empty);
                                }
                            }
                            Clans[clanname].members.Clear();
                            Clans.Remove(clanname);
                            server.Broadcast(string.Format(config.Messages["ClanDisband"], player.Name, clanname));
                        }

                    }
                    else
                        player.MessageFrom(Name, config.Messages["NotInClan"]);
                }
            }
            
        }

        public void StartClanBaseTeleportDelay(Fougerite.Player player, ClanProps clan)
        {
            Timer timer = new Timer();
            timer.AutoReset = false;
            timer.Interval = config.TeleportDelay * 1000;
            timer.Enabled = true;
            timer.Elapsed += (x, y) =>
            {
                player.SafeTeleportTo(util.ConvertStringToVector3(clan.clanbase), false);
                Cooldown[player.SteamID] = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds;
            };
        }

        public string GetClanOfPlayer(string steamID)
        {
            foreach(KeyValuePair<string, ClanProps> pair in Clans)
            {
                if(pair.Value.ownerid == steamID || pair.Value.members.Contains(steamID))
                {
                    return pair.Key;
                }
                return null;
            }
            return null;
        }

        public void SendClanMessage(string clan, string prefix, string message)
        {
            foreach (KeyValuePair<string, ClanProps> pair in Clans)
            {
                if(pair.Key == clan)
                {
                    
                    foreach(string id in pair.Value.members)
                    {
                        Fougerite.Player member = this.FindMemberById(id);
                        member.MessageFrom(prefix, message);
                    }
                }
            }
        }

        public Fougerite.Player FindMemberById(string id)
        {
            foreach(var pl in server.Players)
            {
                if(pl.SteamID == id)
                {
                    return pl;
                }
                return null;
            }
            return null;
        }

        public object GetPlayerNameByID(string steamID)
        {
            foreach(var pl in server.Players)
            {
                if(pl.SteamID == steamID)
                {
                    return pl.Name;
                }
                return "Blaster :0";
            }
            return "Blaster :0";
        }

        public void AddPlayerToMemberList(string steamID, string v)
        {
            foreach(KeyValuePair<string, ClanProps> pair in Clans)
            {
                if(pair.Key == v)
                {
                    pair.Value.members.Add(steamID);
                }
            }
        }

        public object FindClanOfOwnerID(string steamID)
        {
            foreach (KeyValuePair<string, ClanProps> pair in Clans)
            {
                if(pair.Value.ownerid == steamID)
                {
                    return pair.Key;
                }
                return null;
            }
            return null;
        }

        public bool HasClan(Fougerite.Player player)
        {
            foreach(KeyValuePair<string, ClanProps> pair in Clans)
            {
                if(pair.Value.ownerid == player.SteamID)
                {
                    return true;
                }
                return false;
            }
            return false;
        }

        public bool IsInClan(Fougerite.Player player)
        {
            foreach (KeyValuePair<string, ClanProps> pair in Clans)
            {
                foreach(string member in pair.Value.members)
                {
                    if (member == player.SteamID)
                        return true;
                    return false;
                }
                return false;
            }
            return false;
        }

        public override string Name
        {
            get { return "ClanSystem"; }

        }
        public override string Author
        {
            get { return "ice cold"; }
        }
        public override string Description
        {
            get { return "Advanced Clan System"; }
        }
        public override Version Version
        {
            get { return new Version("1.0"); }
        }
        public override void DeInitialize()
        {
            JsonHelper.SaveFile(Clans, GetAbsoluteFilePath("db_Clans.json"));

            Hooks.OnChatRaw -= OnCommand;
            Hooks.OnServerSaved -= OnServerSave;
            Hooks.OnServerShutdown -= OnServerShutdown;
            Hooks.OnPlayerConnected -= OnPlayerConnected;

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
        public class ClanProps
        {
            public string ownerid;
            public int FF;
            public string description;
            public string clanbase;
            public List<string> members;

            public ClanProps(string ownerid, int FF, string description, string clanbase, List<string> members)
            {
                this.ownerid = ownerid;
                this.FF = FF;
                this.description = description;
                this.clanbase = clanbase;
                this.members = members;
            }
        }

    }
}
