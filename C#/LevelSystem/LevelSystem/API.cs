using Fougerite;


namespace LevelSystem
{
    public class API
    {
        
        public static void TakeXP(Fougerite.Player player, double xp)
        {
            if(LevelSystem.instance.CanTakePlayerXp(player, xp))
            {
                LevelSystem.instance.playerlevels[player.SteamID].xp -= xp;
            }
        }
        public static void AddXP(Fougerite.Player player, double xp)
        {
            LevelSystem.instance.playerlevels[player.SteamID].xp += xp;
        }
        public static double GetXP(Fougerite.Player player)
        {
            return LevelSystem.instance.playerlevels[player.SteamID].xp;
        }
        public static bool HasXP(Fougerite.Player player, double xp)
        {
            double playerxp = LevelSystem.instance.playerlevels[player.SteamID].xp;
            if (playerxp == xp || playerxp >= xp)
                return true;
            else
                return false;
        }
        public static bool HasUnlocked(Fougerite.Player player, string name)
        {
            if (LevelSystem.instance.playerlevels[player.SteamID].unlocked.ContainsKey(name))
                return true;
            return false;
        }
    }
}
