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
        private const string LOG_PATH = "Components/smb3manip.log";
        private int port = DEFAULT_PORT;
        protected static Thread UpdateThread { get; private set; }
        public static volatile uint currentFrame = 0, lagFrames = 0;

        public Smb3Manip(int port = DEFAULT_PORT)
        {
            this.port = port;
            if (UpdateThread == null)
            {
                UpdateThread = new Thread(new ThreadStart(ReadCommands));
                //UpdateThread.IsBackground = true;
                UpdateThread.Start();
            }
        }

        public void SetPort(int port)
        {
            this.port = port;
        }

        public string GetCurrentStr()
        {
            return "Frame: " + currentFrame + " Lag: " + lagFrames;
        }

        public void ReadCommands()
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
                    currentFrame = BitConverter.ToUInt32(receivedResult, 0);
                    lagFrames = BitConverter.ToUInt16(receivedResult, 4);
                    File.AppendAllText(LOG_PATH, "Received " + currentFrame + " | " + lagFrames + "\n");
                }
            }
            catch(Exception e) {
                File.AppendAllText(LOG_PATH, "Exception " + e + "\n");
            }
        }
    }
}