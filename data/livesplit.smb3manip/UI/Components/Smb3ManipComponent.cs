using LiveSplit.Model;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Windows.Forms;
using LiveSplit.Model.Input;
using System.Linq;

namespace LiveSplit.UI.Components
{
    public class Smb3ManipComponent : IComponent
    {
        public Smb3ManipComponent(LiveSplitState state)
        {
            VerticalHeight = 10;
            Settings = new Smb3ManipComponentSettings(state.Settings.HotkeyProfiles.First().Value.AllowGamepadsAsHotkeys);
            Cache = new GraphicsCache();
            Smb3ManipNameLabel = new SimpleLabel();
            Smb3Manip = new Smb3Manip();
            this.state = state;
            Settings.Smb3ManipReinitialiseRequired += Settings_Smb3ManipReinitialiseRequired;
            Settings.IncrementUpdateRequired += Settings_IncrementUpdateRequired;

            // Subscribe to input hooks.
            Settings.Hook.KeyOrButtonPressed += hook_KeyOrButtonPressed;
        }

        public ISmb3Manip Smb3Manip { get; set; }
        public Smb3ManipComponentSettings Settings { get; set; }

        public GraphicsCache Cache { get; set; }

        public float VerticalHeight { get; set; }

        public float MinimumHeight { get; set; }

        public float MinimumWidth
        {
            get
            {
                return Smb3ManipNameLabel.X + Smb3ManipValueLabel.ActualWidth;
            }
        }

        public float HorizontalWidth { get; set; }

        public IDictionary<string, Action> ContextMenuControls
        {
            get { return null; }
        }

        public float PaddingTop { get; set; }
        public float PaddingLeft { get { return 7f; } }
        public float PaddingBottom { get; set; }
        public float PaddingRight { get { return 7f; } }

        protected SimpleLabel Smb3ManipNameLabel = new SimpleLabel();
        protected SimpleLabel Smb3ManipValueLabel = new SimpleLabel();

        protected Font Smb3ManipFont { get; set; }

        private LiveSplitState state;

        private void DrawGeneral(Graphics g, Model.LiveSplitState state, float width, float height, LayoutMode mode)
        {
            // Set Background colour.
            if (Settings.BackgroundColor.A > 0
                || Settings.BackgroundGradient != GradientType.Plain
                && Settings.BackgroundColor2.A > 0)
            {
                var gradientBrush = new LinearGradientBrush(
                            new PointF(0, 0),
                            Settings.BackgroundGradient == GradientType.Horizontal
                            ? new PointF(width, 0)
                            : new PointF(0, height),
                            Settings.BackgroundColor,
                            Settings.BackgroundGradient == GradientType.Plain
                            ? Settings.BackgroundColor
                            : Settings.BackgroundColor2);

                g.FillRectangle(gradientBrush, 0, 0, width, height);
            }

            // Set Font.
            Smb3ManipFont = Settings.OverrideSmb3ManipFont ? Settings.Smb3ManipFont : state.LayoutSettings.TextFont;

            // Calculate Height from Font.
            var textHeight = g.MeasureString("A", Smb3ManipFont).Height;
            VerticalHeight = 1.2f * textHeight;
            MinimumHeight = MinimumHeight;

            PaddingTop = Math.Max(0, ((VerticalHeight - 0.75f * textHeight) / 2f));
            PaddingBottom = PaddingTop;

            // Assume most users won't count past four digits (will cause a layout resize in Horizontal Mode).
            float fourCharWidth = g.MeasureString("1000", Smb3ManipFont).Width;
            HorizontalWidth = Smb3ManipNameLabel.X + Smb3ManipNameLabel.ActualWidth + (fourCharWidth > Smb3ManipValueLabel.ActualWidth ? fourCharWidth : Smb3ManipValueLabel.ActualWidth);

            // Set Counter Name Labell
            Smb3ManipNameLabel.HorizontalAlignment = mode == LayoutMode.Horizontal ? StringAlignment.Near : StringAlignment.Near;
            Smb3ManipNameLabel.VerticalAlignment = StringAlignment.Center;
            Smb3ManipNameLabel.X = 5;
            Smb3ManipNameLabel.Y = 0;
            Smb3ManipNameLabel.Width = (width - fourCharWidth - 5);
            Smb3ManipNameLabel.Height = height;
            Smb3ManipNameLabel.Font = Smb3ManipFont;
            Smb3ManipNameLabel.Brush = new SolidBrush(Settings.OverrideTextColor ? Settings.Smb3ManipTextColor : state.LayoutSettings.TextColor);
            Smb3ManipNameLabel.HasShadow = state.LayoutSettings.DropShadows;
            Smb3ManipNameLabel.ShadowColor = state.LayoutSettings.ShadowsColor;
            Smb3ManipNameLabel.OutlineColor = state.LayoutSettings.TextOutlineColor;
            Smb3ManipNameLabel.Draw(g);

            // Set Smb3Manip Value Label.
            Smb3ManipValueLabel.HorizontalAlignment = mode == LayoutMode.Horizontal ? StringAlignment.Far : StringAlignment.Far;
            Smb3ManipValueLabel.VerticalAlignment = StringAlignment.Center;
            Smb3ManipValueLabel.X = 5;
            Smb3ManipValueLabel.Y = 0;
            Smb3ManipValueLabel.Width = (width - 10);
            Smb3ManipValueLabel.Height = height;
            Smb3ManipValueLabel.Font = Smb3ManipFont;
            Smb3ManipValueLabel.Brush = new SolidBrush(Settings.OverrideTextColor ? Settings.Smb3ManipValueColor : state.LayoutSettings.TextColor);
            Smb3ManipValueLabel.HasShadow = state.LayoutSettings.DropShadows;
            Smb3ManipValueLabel.ShadowColor = state.LayoutSettings.ShadowsColor;
            Smb3ManipValueLabel.OutlineColor = state.LayoutSettings.TextOutlineColor;
            Smb3ManipValueLabel.Draw(g);
        }

        public void DrawHorizontal(Graphics g, Model.LiveSplitState state, float height, Region clipRegion)
        {
            DrawGeneral(g, state, HorizontalWidth, height, LayoutMode.Horizontal);
        }

        public void DrawVertical(System.Drawing.Graphics g, Model.LiveSplitState state, float width, Region clipRegion)
        {
            DrawGeneral(g, state, width, VerticalHeight, LayoutMode.Vertical);
        }

        public string ComponentName
        {
            get { return "Smb3Manip"; }
        }

        public Control GetSettingsControl(LayoutMode mode)
        {
            return Settings;
        }

        public System.Xml.XmlNode GetSettings(System.Xml.XmlDocument document)
        {
            return Settings.GetSettings(document);
        }

        public void SetSettings(System.Xml.XmlNode settings)
        {
            Settings.SetSettings(settings);

            // Initialise Smb3Manip from settings.
            Smb3Manip = new Smb3Manip(Settings.InitialValue, Settings.Increment);
        }

        public void Update(IInvalidator invalidator, Model.LiveSplitState state, float width, float height, LayoutMode mode)
        {
            try
            {
                if (Settings.Hook != null)
                    Settings.Hook.Poll();
            }
            catch { }

            this.state = state;

            Smb3ManipNameLabel.Text = Settings.Smb3ManipText;
            Smb3ManipValueLabel.Text = Smb3Manip.Count.ToString();

            Cache.Restart();
            Cache["Smb3ManipNameLabel"] = Smb3ManipNameLabel.Text;
            Cache["Smb3ManipValueLabel"] = Smb3ManipValueLabel.Text;

            if (invalidator != null && Cache.HasChanged)
            {
                invalidator.Invalidate(0, 0, width, height);
            }
        }

        public void Dispose()
        {
            Settings.Hook.KeyOrButtonPressed -= hook_KeyOrButtonPressed;
        }

        public int GetSettingsHashCode()
        {
            return Settings.GetSettingsHashCode();
        }

        /// <summary>
        /// Handles the Smb3ManipReinitialiseRequired event of the Settings control.
        /// </summary>
        private void Settings_Smb3ManipReinitialiseRequired(object sender, EventArgs e)
        {
            Smb3Manip = new Smb3Manip(Settings.InitialValue, Settings.Increment);
        }

        private void Settings_IncrementUpdateRequired(object sender, EventArgs e)
        {
            Smb3Manip.SetIncrement(Settings.Increment);
        }

        // Basic support for keyboard/button input.
        private void hook_KeyOrButtonPressed(object sender, KeyOrButton e)
        {
            if ((Form.ActiveForm == state.Form && !Settings.GlobalHotkeysEnabled)
                || Settings.GlobalHotkeysEnabled)
            {
                if (e == Settings.IncrementKey)
                    Smb3Manip.Increment();

                if (e == Settings.DecrementKey)
                    Smb3Manip.Decrement();

                if (e == Settings.ResetKey)
                {
                    Smb3Manip.Reset();
                }
            }
        }
    }
}
