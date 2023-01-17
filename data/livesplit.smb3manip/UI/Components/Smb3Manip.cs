using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace LiveSplit.UI.Components
{
    public class Smb3Manip
    {
        private const int DEFAULT_PORT = 25345;
        private const long EPOCH_OFFSET = 1673989120228;
        private const string LOG_PATH = "Components/smb3manip.log";
        private const double NES_MS_PER_FRAME = 1000.0 / (1008307711.0 / 256.0 / 65536.0);
        private int port = DEFAULT_PORT;
        protected static Thread UpdateThread { get; private set; }
        public static volatile UInt32 lagFrames = 0;
        public static volatile UInt32 startTimeMs = 0;

        public Smb3Manip(int port = DEFAULT_PORT)
        {
            this.port = port;
            if (UpdateThread == null)
            {
                UpdateThread = new Thread(new ThreadStart(UDPListen));
                UpdateThread.IsBackground = true;
                UpdateThread.Start();
            }
        }

        public void SetPort(int port)
        {
            this.port = port;
        }

        public string GetCurrentStr()
        {
            var epoch_modified = DateTimeOffset.Now.ToUnixTimeMilliseconds() - EPOCH_OFFSET;
            var currentFrame = (epoch_modified - startTimeMs) / NES_MS_PER_FRAME;
            return "Frame: " + Math.Round(currentFrame, 1) + " Lag: " + lagFrames;
        }

        public void UDPListen()
        {
            try
            {
                File.AppendAllText(LOG_PATH, "Listening on port " + port + "\n");
                UdpClient udpClient = new UdpClient();
                udpClient.Client.Bind(new IPEndPoint(0, port));
                var from = new IPEndPoint(0, 0);
                while (true)
                {
                    var receivedResult = udpClient.Receive(ref from);
                    var packetType = BitConverter.ToInt16(receivedResult, 0);
                    if (packetType == 1)
                    {
                        startTimeMs = BitConverter.ToUInt32(receivedResult, 2);
                        File.AppendAllText(LOG_PATH, "Received startTimeMs=" + startTimeMs + "\n");
                    }
                    else if (packetType == 2)
                    {
                        lagFrames = BitConverter.ToUInt16(receivedResult, 2);
                        File.AppendAllText(LOG_PATH, "Received lagFrames=" + lagFrames + "\n");
                    }
                }
            }
            catch(Exception e) {
                File.AppendAllText(LOG_PATH, "Exception " + e + "\n");
            }
        }
    }
}