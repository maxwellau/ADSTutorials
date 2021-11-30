using System;
using TwinCAT.Ads;
namespace main{
    class Program
    {
        public static async Task Main()
        {
            string resp;
            // Initialise Telegram Bot
            telegramBot bot = new telegramBot(botToken: "2117034745:AAEKKB-RV1l_vZr17NH9GNEZhBBG3HwKMIQ", chatID: "1124730952");
            System.Console.WriteLine("Bot has been started");

            // Initialise TCADS Client (Default for TC3 is 851)
            AdsClient myClient = new AdsClient();
            myClient.Connect(AmsNetId.Local, 851);
            System.Console.WriteLine("ADS Client started");

            await bot.sendMessage("TCADS and Telebot has been initialised\n\n/turnon\n\n/turnoff\n\n/readState"); // await is necessary because it is an async task

            while(true)
            {
                resp = await bot.pollResponse(seconds:10);
                if(resp=="/turnon")
                {
                    await bot.sendMessage("which one?\n\n/bTeleRun");
                    resp = await bot.pollResponse(seconds:70);
                    if(resp =="/bTeleRun")
                    {
                        myClient.WriteAny(myClient.CreateVariableHandle("test1.bTeleRun"), true);
                    }
                }
                else if(resp=="/turnoff")
                {
                    await bot.sendMessage("which one?\n\n/bTeleRun");
                    resp = await bot.pollResponse(seconds:10);
                    if(resp =="/bTeleRun")
                    {
                        myClient.WriteAny(myClient.CreateVariableHandle("test1.bTeleRun"), false);
                    }
                }
                else if(resp=="/readState")
                {
                    await bot.sendMessage("which one?\n\n/bTeleRun");
                    resp = await bot.pollResponse(seconds:10);
                    if(resp =="/bTeleRun")
                    {
                        var state = myClient.ReadAny(myClient.CreateVariableHandle("test1.bTeleRun"), typeof(bool));
                        System.Console.WriteLine(state.GetType());
                        string stateString = state.ToString();
                        await bot.sendMessage($"bTeleRun is currently on {stateString}");
                    }
                }
            }

            // Create variable:
            //  var mainRun = myClient.CreateVariableHandle("MAIN.Run");
            // Read Variable:
            //  var read = myClient.ReadAny(mainRun, typeof(bool));
            // Write Variable:
            //  myClient.WriteAny(mainRun, true);
        }
    }
}
