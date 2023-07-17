using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Fougerite;
using Fougerite.Events;
using UnityEngine;
using LevelSystem;
using System.IO;
using User = Fougerite.Player;

namespace Teleportation
{
    public class Config
    {
        public double Delay;
        public double XP;
        public double Cooldown;
        public bool BlockBuilding;
        public bool CancelOnHurt;

        public Dictionary<string, string> Messages;

        public Config Default()
        {
            Delay = 20.0;
            XP = 30.0;
            Cooldown = 120.0;
            BlockBuilding = true;
            CancelOnHurt = true;

            Messages = new Dictionary<string, string>()
            {
                { "Requested", "You've sended a teleport request to {0} for {1} xp, wait for him to accept" },
                { "Incomming", "You have a incomming teleport request from {0}, Type /tpa to accept or /tpd to deny" },
                { "Accept", "You've accepted the teleport request of {0}" },
                { "Accepted", "{0} has accepted the teleport request, teleporting in {1} Seconds" },
                { "Teleport", "{0} has teleported to you" },
                { "NotEnoughXP", "You do not have enough xp to use this command!" },
                { "NotUnlocked", "You do not have the tpr command unlocked yet" },
                { "Cancelled", "You've cancelled all teleport requests" },
                { "Deny", "You've denied all teleport requests" },
                { "Denied", "Your teleport request has been denied" },
                { "NearStructure", "You may not teleport near a structure" },
                { "AlreadyRequesting", "You've already a outgoing request" },
                { "NoIncomming", "You have no incomming requests" },
                { "AlreadyIncomming", "{0} has already a incomming request from someone else" },
                { "UnderCooldown", "You are under cooldown for {0} seconds" },
                { "Hurt", "Damage dealed, Teleport canceled" }
            };
            return this;

        }

    }
    public class Teleportation : Module
    {
        public static Config config = new Config();
        public Dictionary<User, User> Requested;
        public Dictionary<User, User> Incomming;
        public Dictionary<string, double> Cooldown;

        private const string cadet = "[color #8ee5ee]";
        private const string orange = "[color #ff7f24]";

        Server server = Server.GetServer();


        public override void Initialize()
        {
            Requested = new Dictionary<User, User>();
            Incomming = new Dictionary<User, User>();
            Cooldown = new Dictionary<string, double>();
            config = ReadyConfigChecked(config.Default(), "cfg_Configuration.json");

            Hooks.OnCommand += OnCommand;
            Hooks.OnPlayerHurt += OnHurt;
            Hooks.OnPlayerDisconnected += OnPlayerLeave;
            Hooks.OnSteamDeny += SteamDeny;
        }

        private void SteamDeny(SteamDenyEvent sde)
        {
            if(sde.ErrorNumber == NetError.Facepunch_Connector_Cancelled)
            {
                sde.ForceAllow = true;
            }
        }

        private void OnPlayerLeave(User player)
        {
            if(Requested.ContainsKey(player))
            {
                Incomming.Remove(Requested[player]);
                Requested.Remove(player);
            }
            else if(Incomming.ContainsKey(player))
            {
                Requested.Remove(Incomming[player]);
                Incomming.Remove(player);
            }
        }

        private void OnHurt(HurtEvent he)
        {
            if(he.AttackerIsPlayer && he.VictimIsPlayer && he.DamageAmount > 0F)
            {
                User attacker = (User)he.Attacker;
                User victim = (User)he.Victim;

                if(config.CancelOnHurt)
                {
                    if (Requested.ContainsKey(attacker))
                    {
                        Requested.Remove(attacker);
                        Incomming.Remove(attacker);
                        attacker.MessageFrom(Name, config.Messages["Hurt"]);
                    }
                }

               
            }
        }

        private void OnCommand(User player, string cmd, string[] args)
        {
            if(cmd == "tpr")
            {
                if(args.Length == 0)
                {
                    player.MessageFrom(Name, cadet + "Syntax: /tpr playername - Sends a teleport request to the user");
                    player.MessageFrom(Name, cadet + "Syntax: /tpa - Accepts a incomming teleport request");
                    player.MessageFrom(Name, cadet + "Syntax: /tpc - Cancel all outgoing teleport requests");
                    player.MessageFrom(Name, cadet + "Syntax: /tpd - Deny all incomming teleport requests");

                    if(config.XP != 0.0)
                    {
                        player.MessageFrom(Name, orange + "REMEMBER: Every teleportion costs " + config.XP + " XP");
                    }
                }
                else if(args.Length == 1)
                {
                    User target = server.FindPlayer(args[0]);
                    if(target == null) { player.MessageFrom(Name, "[color red]This player doesnt exist"); return; }
                    if(config.BlockBuilding && player.IsNearStructure || target.IsNearStructure) { player.MessageFrom(Name, config.Messages["NearStructure"]); return; }
                    if(config.XP > 0.0 && !LevelSystem.API.HasXP(player, config.XP)) { player.MessageFrom(Name, config.Messages["NotEnoughXP"]); return; }
                    if(Requested.ContainsKey(player)) { player.MessageFrom(Name, config.Messages["AlreadyRequesting"]); return; }
                    if(Incomming.ContainsKey(target)) { player.MessageFrom(Name, string.Format(config.Messages["AlreadyIncomming"], target.Name)); return; }
                    if(Cooldown.ContainsKey(player.SteamID)) {
                        double calc = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds - Cooldown[player.SteamID];

                        player.MessageFrom(Name, string.Format(config.Messages["UnderCooldown"], Math.Round(Math.Abs(calc - config.Cooldown))));
                        return;
                    }
                    Cooldown.Remove(player.SteamID);
                    player.MessageFrom(Name, string.Format(config.Messages["Requested"], target.Name, config.XP));
                    target.MessageFrom(Name, string.Format(config.Messages["Incomming"], player.Name));
                    Requested.Add(player, target);
                    Incomming.Add(target, player);
                    LevelSystem.API.TakeXP(player, config.XP);
                    Metabolism controllable = target.PlayerClient.controllable.GetComponent<Metabolism>();
                    controllable.networkView.RPC("Vomit", controllable.networkView.owner);
                }
            }
            if(cmd == "tpa")
            {
                if(!Incomming.ContainsKey(player)) { player.MessageFrom(Name, config.Messages["NoIncomming"]); return; }
                if(!Incomming[player].IsOnline) { player.MessageFrom(Name, "Your friend isn't online anymore"); Incomming.Remove(player); Requested.Remove(Incomming[player]); return; }

                player.MessageFrom(Name, string.Format(config.Messages["Accept"], Incomming[player].Name));
                Incomming[player].MessageFrom(Name, string.Format(config.Messages["Accepted"], Incomming[player].Name, config.Delay));

                StartTeleportDelay(player, Incomming[player]);

            }
            if(cmd == "tpc")
            {
                if(!Requested.ContainsKey(player)) { player.MessageFrom(Name, "[color red]You do not have any outgoing requests"); return; }
                player.MessageFrom(Name, config.Messages["Cancelled"]);
                Requested.Remove(player);
            }
            if(cmd == "tpd")
            {
                if (!Incomming.ContainsKey(player)) { player.MessageFrom(Name, string.Format(config.Messages["NoIncomming"])); return; }

                player.MessageFrom(Name, config.Messages["You've denied all teleport requests"]);
                Incomming[player].MessageFrom(Name, config.Messages["Denied"]);
                Requested.Remove(Incomming[player]);
                Incomming.Remove(player);
            }
        }

        private void StartTeleportDelay(User player1, User player2)
        {
            if (Requested.ContainsKey(player2) && Incomming.ContainsKey(player1))
            {
                if (player1.IsOnline && player2.IsOnline)
                {
                    if (player1.IsAlive && player2.IsAlive)
                    {
                        TimerPlus timer = new TimerPlus();
                        timer.AutoReset = false;
                        timer.Interval = config.Delay * 1000;
                        timer.Enabled = true;
                        timer.Elapsed += (x, y) =>
                        {
                            player2.TeleportToTheClosestSpawnpoint(player1.Location, false);

                            TimerPlus timer2 = new TimerPlus();
                            timer2.AutoReset = false;
                            timer2.Interval = 2.0 * 1000;
                            timer2.Enabled = true;
                            timer2.Elapsed += (k, r) =>
                            {
                                player2.TeleportTo(player1.Location, false);
                                player1.MessageFrom(Name, string.Format(config.Messages["Teleport"], player2.Name));
                                Incomming.Remove(player1);
                                Requested.Remove(player2);

                                StartCooldownTimer(player2);

                            };
                        };
                    }
                }
            }                         
        }

        private void StartCooldownTimer(User player)
        {
            Cooldown[player.SteamID] = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds;
        }

        public override void DeInitialize()
        {
            Hooks.OnCommand -= OnCommand;
            Hooks.OnPlayerHurt -= OnHurt;
            Hooks.OnPlayerDisconnected -= OnPlayerLeave;
            Hooks.OnSteamDeny -= SteamDeny;
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

        public override string Name
        {
            get { return "Teleportation"; }

        }
        public override string Author
        {
            get { return "ice cold"; }
        }
        public override string Description
        {
            get { return "Advanced Teleportion system"; }
        }
        public override Version Version
        {
            get { return new Version("1.0"); }
        }
    }
}
