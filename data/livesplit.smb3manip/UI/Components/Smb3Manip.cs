namespace LiveSplit.UI.Components
{
    public class Smb3Manip
    {
        private const int DEFAULT_PORT = 25345;
        private int port = DEFAULT_PORT;
        private string currentStr = "nil";

        public Smb3Manip(int port = DEFAULT_PORT)
        {
            this.port = port;
            SetCurrentStr(0, 0);
        }

        public void Reset()
        {
            SetCurrentStr(0, 0);
        }

        public void SetPort(int port)
        {
            this.port = port;
        }

        public void SetCurrentStr(int currentFrame, int lagFrames)
        {
            currentStr = "Frame: " + currentFrame + " Lag Frames: " + lagFrames;
        }

        public string GetCurrentStr()
        {
            return currentStr;
        }
    }
}