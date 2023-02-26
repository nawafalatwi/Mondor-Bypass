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
            for (int i=0; i<65536; i++){
                CaptchaImage cac = new CaptchaImage();
                cac.Width = 105;
                cac.Height = 32;
                cac.TextLength = 6;
                cac.FontColor = Color.FromArgb(100, 100, 100); // (100, 100, 100)
                cac.LineNoise = CaptchaImage.lineNoiseLevel.High;
                cac.BackgroundNoise = CaptchaImage.backgroundNoiseLevel.None;

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
