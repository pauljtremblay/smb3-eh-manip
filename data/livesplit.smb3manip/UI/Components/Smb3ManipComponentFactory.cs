using LiveSplit.Model;
using System;

namespace LiveSplit.UI.Components
{
    public class Smb3ManipComponentFactory : IComponentFactory
    {
        public string ComponentName => "Smb3Manip";

        public string Description => "An integreation with the smb3 manip tool to render helpful info.";

        public ComponentCategory Category => ComponentCategory.Other;

        public IComponent Create(LiveSplitState state) => new Smb3ManipComponent(state);

        public string UpdateName => ComponentName;

        public string XMLURL => "http://livesplit.org/update/Components/update.LiveSplit.Smb3Manip.xml";

        public string UpdateURL => "http://livesplit.org/update/";

        public Version Version => Version.Parse("1.0.0");
    }
}
