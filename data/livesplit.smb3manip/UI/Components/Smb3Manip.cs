using System.IO;
using System.Net.Sockets;
using System.Threading.Tasks;

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
            StartUpdateThread();
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

        private void StartUpdateThread()
        {
            Task.Run(async () =>
            {
                File.AppendAllText("smb3manip.log", "Listening on port " + port);
                using (var udpClient = new UdpClient(port))
                {
                    while (true)
                    {
                        var receivedResult = await udpClient.ReceiveAsync();
                        int currentFrame = System.BitConverter.ToInt32(receivedResult.Buffer, 0);
                        int lagFrames = System.BitConverter.ToInt32(receivedResult.Buffer, 4);
                        File.AppendAllText("smb3manip.log", "Received " + currentFrame + " | " + lagFrames);
                        SetCurrentStr(currentFrame, lagFrames);
                    }
                }
            });
        }
    }
}