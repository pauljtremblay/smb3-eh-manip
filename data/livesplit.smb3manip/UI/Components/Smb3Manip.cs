using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Threading.Tasks;

namespace LiveSplit.UI.Components
{
    public class Smb3Manip
    {
        private const int DEFAULT_PORT = 25345;
        private int port = DEFAULT_PORT;
        private string currentStr = "nil";
        private Thread trd = null;

        public Smb3Manip(int port = DEFAULT_PORT)
        {
            this.port = port;
            SetCurrentStr(0, 0);
        }

        public void Reset()
        {
            SetCurrentStr(0, 0);
            StartUpdateThread();
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
            if (trd != null && trd.IsAlive)
                trd.Abort();
            trd = new Thread(new ThreadStart(ThreadTask))
            {
                IsBackground = true
            };
            trd.Start();
        }

        private void ThreadTask()
        {
            var from = new IPEndPoint(0, 0);
            using (var udpClient = new UdpClient(port))
            {
                while (true)
                {
                    var receivedResult = udpClient.Receive(ref from);
                    int currentFrame = System.BitConverter.ToInt32(receivedResult, 0);
                    int lagFrames = System.BitConverter.ToInt32(receivedResult, 4);
                    SetCurrentStr(currentFrame, lagFrames);
                }
            }
        }
    }
}