using LiveSplit.Options;
using System;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using LiveSplit.Model.Input;
using System.Threading;

namespace LiveSplit.UI.Components
{
    public partial class Smb3ManipComponentSettings : UserControl
    {
        public Smb3ManipComponentSettings(bool allowGamepads)
        {
            InitializeComponent();

            Hook = new CompositeHook(allowGamepads);

            // Set default values.
            GlobalHotkeysEnabled = false;
            Smb3ManipFont = new Font("Segoe UI", 13, FontStyle.Regular, GraphicsUnit.Pixel);
            OverrideSmb3ManipFont = false;
            Smb3ManipTextColor = Color.FromArgb(255, 255, 255, 255);
            Smb3ManipValueColor = Color.FromArgb(255, 255, 255, 255);
            OverrideTextColor = false;
            BackgroundColor = Color.Transparent;
            BackgroundColor2 = Color.Transparent;
            BackgroundGradient = GradientType.Plain;
            Smb3ManipText = "Smb3Manip:";
            Port = 0;

            // Set bindings.
            //txtSmb3ManipText.DataBindings.Add("Text", this, "Smb3ManipText");
            numPort.DataBindings.Add("Value", this, "port");
            chkFont.DataBindings.Add("Checked", this, "OverrideSmb3ManipFont", false, DataSourceUpdateMode.OnPropertyChanged);
            lblFont.DataBindings.Add("Text", this, "Smb3ManipFontString", false, DataSourceUpdateMode.OnPropertyChanged);
            chkColor.DataBindings.Add("Checked", this, "OverrideTextColor", false, DataSourceUpdateMode.OnPropertyChanged);
            btnColor.DataBindings.Add("BackColor", this, "Smb3ManipTextColor", false, DataSourceUpdateMode.OnPropertyChanged);
            btnColor3.DataBindings.Add("BackColor", this, "Smb3ManipValueColor", false, DataSourceUpdateMode.OnPropertyChanged);
            btnColor1.DataBindings.Add("BackColor", this, "BackgroundColor", false, DataSourceUpdateMode.OnPropertyChanged);
            btnColor2.DataBindings.Add("BackColor", this, "BackgroundColor2", false, DataSourceUpdateMode.OnPropertyChanged);
            cmbGradientType.DataBindings.Add("SelectedItem", this, "GradientString", false, DataSourceUpdateMode.OnPropertyChanged);

            // Assign event handlers.
            cmbGradientType.SelectedIndexChanged += cmbGradientType_SelectedIndexChanged;
            chkFont.CheckedChanged += chkFont_CheckedChanged;
            chkColor.CheckedChanged += chkColor_CheckedChanged;

            Load += Smb3ManipSettings_Load;
        }

        public CompositeHook Hook { get; set; }

        public bool GlobalHotkeysEnabled { get; set; }

        public Color Smb3ManipTextColor { get; set; }
        public Color Smb3ManipValueColor { get; set; }
        public bool OverrideTextColor { get; set; }

        public string Smb3ManipFontString { get { return String.Format("{0} {1}", Smb3ManipFont.FontFamily.Name, Smb3ManipFont.Style); } }
        public Font Smb3ManipFont { get; set; }
        public bool OverrideSmb3ManipFont { get; set; }

        public Color BackgroundColor { get; set; }
        public Color BackgroundColor2 { get; set; }
        public GradientType BackgroundGradient { get; set; }
        public String GradientString
        {
            get { return BackgroundGradient.ToString(); }
            set { BackgroundGradient = (GradientType)Enum.Parse(typeof(GradientType), value); }
        }

        public string Smb3ManipText { get; set; }
        public int Port { get; set; }

        public KeyOrButton ResetKey { get; set; }

        public event EventHandler Smb3ManipReinitialiseRequired;

        public void SetSettings(XmlNode node)
        {
            var element = (XmlElement)node;
            GlobalHotkeysEnabled = SettingsHelper.ParseBool(element["GlobalHotkeysEnabled"]);
            Smb3ManipTextColor = SettingsHelper.ParseColor(element["Smb3ManipTextColor"]);
            Smb3ManipValueColor = SettingsHelper.ParseColor(element["Smb3ManipValueColor"]);
            Smb3ManipFont = SettingsHelper.GetFontFromElement(element["Smb3ManipFont"]);
            OverrideSmb3ManipFont = SettingsHelper.ParseBool(element["OverrideSmb3ManipFont"]);
            OverrideTextColor = SettingsHelper.ParseBool(element["OverrideTextColor"]);
            BackgroundColor = SettingsHelper.ParseColor(element["BackgroundColor"]);
            BackgroundColor2 = SettingsHelper.ParseColor(element["BackgroundColor2"]);
            GradientString = SettingsHelper.ParseString(element["BackgroundGradient"]);
            Smb3ManipText = SettingsHelper.ParseString(element["Smb3ManipText"]);
            Port = SettingsHelper.ParseInt(element["PortValue"]);
        }

        public XmlNode GetSettings(XmlDocument document)
        {
            var parent = document.CreateElement("Settings");
            CreateSettingsNode(document, parent);
            return parent;
        }

        public int GetSettingsHashCode()
        {
            return CreateSettingsNode(null, null);
        }

        private int CreateSettingsNode(XmlDocument document, XmlElement parent)
        {
            return SettingsHelper.CreateSetting(document, parent, "Version", "1.0") ^
            SettingsHelper.CreateSetting(document, parent, "GlobalHotkeysEnabled", GlobalHotkeysEnabled) ^
            SettingsHelper.CreateSetting(document, parent, "OverrideSmb3ManipFont", OverrideSmb3ManipFont) ^
            SettingsHelper.CreateSetting(document, parent, "OverrideTextColor", OverrideTextColor) ^
            SettingsHelper.CreateSetting(document, parent, "Smb3ManipFont", Smb3ManipFont) ^
            SettingsHelper.CreateSetting(document, parent, "Smb3ManipTextColor", Smb3ManipTextColor) ^
            SettingsHelper.CreateSetting(document, parent, "Smb3ManipValueColor", Smb3ManipValueColor) ^
            SettingsHelper.CreateSetting(document, parent, "BackgroundColor", BackgroundColor) ^
            SettingsHelper.CreateSetting(document, parent, "BackgroundColor2", BackgroundColor2) ^
            SettingsHelper.CreateSetting(document, parent, "BackgroundGradient", BackgroundGradient) ^
            SettingsHelper.CreateSetting(document, parent, "Smb3ManipText", Smb3ManipText) ^
            SettingsHelper.CreateSetting(document, parent, "PortValue", Port) ^
            SettingsHelper.CreateSetting(document, parent, "ResetKey", ResetKey);
        }

        private string FormatKey(KeyOrButton key)
        {
            if (key == null)
                return "None";
            string str = key.ToString();
            if (key.IsButton)
            {
                int length = str.LastIndexOf(' ');
                if (length != -1)
                    str = str.Substring(0, length);
            }
            return str;
        }

        private void Smb3ManipSettings_Load(object sender, EventArgs e)
        {
            chkColor_CheckedChanged(null, null);
            chkFont_CheckedChanged(null, null);
        }

        private void ColorButtonClick(object sender, EventArgs e)
        {
            SettingsHelper.ColorButtonClick((Button)sender, this);
        }

        private void btnFont_Click(object sender, EventArgs e)
        {
            var dialog = SettingsHelper.GetFontDialog(Smb3ManipFont, 7, 20);
            dialog.FontChanged += (s, ev) => Smb3ManipFont = ((CustomFontDialog.FontChangedEventArgs)ev).NewFont;
            dialog.ShowDialog(this);
            lblFont.Text = Smb3ManipFontString;
        }

        private void chkColor_CheckedChanged(object sender, EventArgs e)
        {
            label3.Enabled = btnColor.Enabled = label5.Enabled = btnColor3.Enabled = chkColor.Checked;
        }

        void chkFont_CheckedChanged(object sender, EventArgs e)
        {
            label1.Enabled = lblFont.Enabled = btnFont.Enabled = chkFont.Checked;
        }

        void cmbGradientType_SelectedIndexChanged(object sender, EventArgs e)
        {
            btnColor1.Visible = cmbGradientType.SelectedItem.ToString() != "Plain";
            btnColor2.DataBindings.Clear();
            btnColor2.DataBindings.Add("BackColor", this, btnColor1.Visible ? "BackgroundColor2" : "BackgroundColor", false, DataSourceUpdateMode.OnPropertyChanged);
            GradientString = cmbGradientType.SelectedItem.ToString();
        }

        private void numPort_ValueChanged(object sender, EventArgs e)
        {
            Port = (int)Math.Round(numPort.Value, 0);
            Smb3ManipReinitialiseRequired(this, EventArgs.Empty);
        }
    }
}
