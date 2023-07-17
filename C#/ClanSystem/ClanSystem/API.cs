using System;


namespace ClanSystem
{
    /// <summary>
    /// API class that allows other plugins to interact with ClanSystem
    /// </summary>
    public class API
    {
        /// <summary>
        /// Changes the FriendlyFire option between 0 and 1
        /// </summary>
        /// <param name="player"></param>
        /// <param name="mode"></param>
        public void SetFF(Fougerite.Player player, int mode)
        {
            if(ClanSystem.instance.IsInClan(player))
            {
                var clan = ClanSystem.instance.Clans[ClanSystem.instance.GetClanOfPlayer(player.SteamID)];
                clan.FF = mode;
            }
        }

    }
}
