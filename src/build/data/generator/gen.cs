using System;
using MSCaptcha;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Text;
// using System.Drawing;
// using System.Drawing.Imaging;
using System.Web;
using System.Web.SessionState; 

namespace gen
{
    class gen
    {
        static void Main(string[] args)
        {
            CaptchaImage cac = new CaptchaImage();
            for (int i=0; i<(1<<17); i++){
                cac.Width = 250;
                cac.Height = 60;
                cac.TextLength = 6;
                cac.FontColor = Color.FromArgb(84, 156, 0); // (100, 100, 100)
                cac.LineNoise = CaptchaImage.lineNoiseLevel.None;
                cac.BackgroundNoise = CaptchaImage.backgroundNoiseLevel.Low;
                Bitmap bm = cac.RenderImage();
                bm.Save("tmp/" + cac.Text + i.ToString() + ".png", ImageFormat.Png);
                if (i % 1000 == 0){
                    Console.WriteLine(i);
                }
            }
        }
    }
}

// csc -reference:MSCaptcha.dll -target:exe -out:gen.exe gen.cs
