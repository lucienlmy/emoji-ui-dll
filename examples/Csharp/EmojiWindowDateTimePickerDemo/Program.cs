using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowDateTimePickerDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new DateTimePickerDemoApp().Run();
        }
    }

    internal sealed class DateTimePickerDemoApp : DemoApp
    {
        private IntPtr _picker;
        private EmojiWindowNative.ValueChangedCallback _valueChangedCallback;

        public DateTimePickerDemoApp()
            : base("EmojiWindow DateTimePicker Demo - C# .NET 4.0", 900, 500)
        {
        }

        protected override void Build()
        {
            CreateHeader("DateTimePicker Demo", "Read and update date/time values.");

            CreateGroupBox(WindowHandle, "DateTimePicker Stage", 18, 84, 850, 160, ColorPrimary);
            _picker = EmojiWindowNative.CreateD2DDateTimePicker(WindowHandle, 52, 173, 320, 38, EmojiWindowNative.DatePrecisionYmdHm, ColorText, ColorWhite, ColorBorder, FontYaHei, FontYaHei.Length, 12, false, false, false);
            EmojiWindowNative.SetD2DDateTimePickerDateTime(_picker, 2026, 3, 31, 15, 20, 0);

            _valueChangedCallback = new EmojiWindowNative.ValueChangedCallback(OnValueChanged);
            EmojiWindowNative.SetD2DDateTimePickerCallback(_picker, _valueChangedCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "DateTimePicker Actions", 18, 264, 850, 150, ColorSuccess);
            AddButton(ops, "R", "Read", 24, 46, 110, 34, ColorPrimary, ReadDateTime);
            AddButton(ops, "P", "Precision", 148, 46, 110, 34, ColorSuccess, ChangePrecision);
            AddButton(ops, "C", "Colors", 272, 46, 110, 34, ColorWarning, Recolor);
            AddButton(ops, "N", "New Year", 396, 46, 110, 34, ColorDanger, SetNewYear);
        }

        private void ReadDateTime()
        {
            int year;
            int month;
            int day;
            int hour;
            int minute;
            int second;
            EmojiWindowNative.GetD2DDateTimePickerDateTime(_picker, out year, out month, out day, out hour, out minute, out second);
            SetStatus(year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second);
        }

        private void ChangePrecision()
        {
            int precision = EmojiWindowNative.GetD2DDateTimePickerPrecision(_picker);
            EmojiWindowNative.SetD2DDateTimePickerPrecision(_picker, precision == EmojiWindowNative.DatePrecisionYmdHm ? EmojiWindowNative.DatePrecisionYmdHms : EmojiWindowNative.DatePrecisionYmdHm);
            SetStatus("Current precision=" + EmojiWindowNative.GetD2DDateTimePickerPrecision(_picker));
        }

        private void Recolor()
        {
            EmojiWindowNative.SetD2DDateTimePickerColors(_picker, ColorPrimary, ColorCard, ColorPrimary);
            SetStatus("DateTimePicker colors updated.");
        }

        private void SetNewYear()
        {
            EmojiWindowNative.SetD2DDateTimePickerDateTime(_picker, 2027, 1, 1, 9, 30, 0);
            SetStatus("Set to 2027-01-01 09:30.");
        }

        private void OnValueChanged(IntPtr hwnd)
        {
            SetStatus("DateTimePicker callback triggered.");
        }
    }
}
