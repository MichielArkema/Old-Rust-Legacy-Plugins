using System;
using Fougerite;
using Newtonsoft.Json;
using System.Net;
using System.Collections.Generic;
using System.IO;
namespace PlayerConnections
{
    public class Config
    {
        public bool showCountry;
        public bool blockVPN;

        public Dictionary<string, string> Messages;
        public List<string> BlockedCountries;

        public Config Default()
        {
            showCountry = true;
            blockVPN = true;
            Messages = new Dictionary<string, string>()
            {
                { "JoinMessage", "{0} has joined the server" },
                { "LeaveMessage", "{0} has left the server" },
                { "CountryMessage", "{0} has joined the server from {1}" },
                { "FirstJoinMessage", "{0} has joined the server for the first time, Please dont try to be KOS!" },
                { "VPNDetectedMessage", "{0} has been kicked for VPN" },
                { "CountryBlocked", "{0} has been kicked for country blacklist" },
                { "WelcomeMessage", "Welcome to Uberrust Remastered {0}" },
                { "WelcomeMessage2", "There are {0}| 100 people online" },
                { "WelcomeMessage3", "Check out our cool commands using /help" }
            };
            BlockedCountries = new List<string>();
            return this;
        }
    }
    public class PlayerConnections : Module
    {
        public Config config = new Config();
        Server server = Server.GetServer();

        public List<string> Joined;

        public override void Initialize()
        {
            
            Joined = new List<string>();
            Hooks.OnPlayerConnected += OnPlayerConnected;
            Hooks.OnPlayerDisconnected += OnPlayerDisconnected;
            Hooks.OnServerSaved += OnSave;
            config = ReadyConfigChecked(config.Default(), "cfg_Configuration.json");
            Joined = ReadyConfigChecked(Joined, "db_Joined.json");
        }

        private void OnSave(int Amount, double Seconds)
        {
            JsonHelper.SaveFile(Joined, GetAbsoluteFilePath("db_Joined.json"));
        }

        private void OnPlayerDisconnected(Fougerite.Player player)
        {
            server.Broadcast(string.Format(config.Messages["LeaveMessage"], player.Name));
        }

        private void OnPlayerConnected(Fougerite.Player player)
        {
            if(config.showCountry)
            {
                ShowCountry(player);
            }
            else
            {
                server.Broadcast(string.Format(config.Messages["JoinMessage"], player.Name));
            }
            if(config.blockVPN)
            {
                CheckProxy(player);
            }
            if(!Joined.Contains(player.SteamID))
            {
                server.Broadcast(string.Format(config.Messages["FirstJoinMessage"], player.Name));
                Joined.Add(player.SteamID);
            }
            player.Message(string.Format(config.Messages["WelcomeMessage"], player.Name));
            player.Message(string.Format(config.Messages["WelcomeMessage2"], server.Players.Count));
            player.Message(string.Format(config.Messages["WelcomeMessage3"]));
        }

        private void CheckProxy(Fougerite.Player player)
        {
            string url = "http://v2.api.iphub.info/ip/" + player.IP;
            VPNDetector vpn;
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
            request.Headers.Add("X-Key: NDAwNzozdmZXMzlCQ01QY2ROcXVNMURVc2N6NktBSFlDc0s5aA==");
            using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
            using (Stream stream = response.GetResponseStream())
            using (StreamReader reader = new StreamReader(stream))
            {
                int code = (int)response.StatusCode;
                if (code == 429)
                {
                    Logger.Log("You have reached the limit of allows requested per day");
                    return;
                }
                var json = reader.ReadToEnd();
                vpn = JsonConvert.DeserializeObject<VPNDetector>(json);
            }
            if (vpn.block == 1)
            {
                player.Disconnect(true, NetError.ApprovalDenied);
                Logger.Log("[AntiVPN] " + player.Name + " has been kicked for using VPN");
            }
        }

        private void ShowCountry(Fougerite.Player player)
        {
            County country;
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(@"http://ip-api.com/json/" + player.IP);
            using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
            using (Stream stream = response.GetResponseStream())
            using (StreamReader reader = new StreamReader(stream))
            {
                var json = reader.ReadToEnd();
                country = JsonConvert.DeserializeObject<County>(json);
            }
            server.Broadcast(string.Format(config.Messages["CountryMessage"], player.Name, country.country));
            if(config.BlockedCountries.Contains(country.country))
            {
                server.Broadcast(string.Format(config.Messages["CountryBlocked"], player.Name));
                player.Disconnect(true, NetError.ApprovalDenied);
            }
            

        }

        public override void DeInitialize()
        {
            Hooks.OnPlayerConnected -= OnPlayerConnected;
            Hooks.OnPlayerDisconnected -= OnPlayerDisconnected;
            Hooks.OnServerSaved -= OnSave;
            JsonHelper.SaveFile(Joined, GetAbsoluteFilePath("db_Joined.json"));
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
            get { return "PlayerConnections"; }

        }
        public override string Author
        {
            get { return "ice cold"; }
        }
        public override string Description
        {
            get { return "Advanced Connection Plugin"; }
        }
        public override Version Version
        {
            get { return new Version("1.0"); }
        }

    }
    public class County
    {
        [JsonProperty("country")]
        public string country { get; set; }
    }
    public class VPNDetector
    {
        [JsonProperty("block")]
        public int block { get; set; }
    }
}
