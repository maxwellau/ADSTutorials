using System;
using Newtonsoft.Json;
using System.Net.Http;

class telegramBot
    {
        // INITIALISE HTTP CLIENT AND CONSTRUCTOR
        HttpClient client = new HttpClient();
        public telegramBot(string botToken, string chatID)
        {
            BotToken = botToken;
            ChatID = chatID;
        }

        public string BotToken {get;set;}
        public string ChatID {get;set;}

        // GET OBJECTS FOR JSON PARSING
        public class From
        {
            public int id { get; set; }
            public bool is_bot { get; set; }
            public string first_name { get; set; }
            public string username { get; set; }
            public string language_code { get; set; }
        }

        public class Chat
        {
            public int id { get; set; }
            public string first_name { get; set; }
            public string username { get; set; }
            public string type { get; set; }
        }

        public class Message
        {
            public int message_id { get; set; }
            public From from { get; set; }
            public Chat chat { get; set; }
            public int date { get; set; }
            public string text { get; set; }
        }

        public class Result
        {
            public int update_id { get; set; }
            public Message message { get; set; }
        }

        public class Root
        {
            public bool ok { get; set; }
            public List<Result> result { get; set; }
        }

        // SENDING MESSAGE
        public async Task<string> sendMessage(string message)
        {
            var values = new Dictionary<string, string>
            {
                { "chat_id", ChatID },
                { "text", message}
            };
            var content = new FormUrlEncodedContent(values);
            string URI = string.Format($"https://api.telegram.org/bot{BotToken}/sendMessage");
            var response = await client.PostAsync(URI, content);
            var responseString = await response.Content.ReadAsStringAsync();
            return responseString;
        }

        //GET LAST MESSAGE
        public async Task<string> getLastMessage()
        {
            string URI = string.Format($"https://api.telegram.org/bot{BotToken}/getUpdates");
            var responseString = await client.GetStringAsync(URI);
            Root resp = JsonConvert.DeserializeObject<Root>(responseString);
            int respLength = resp.result.Count - 1;
            string message = resp.result[respLength].message.text;
            return message;
        }
        //GET UPDATE ID
        public async Task<int> getUpdateID()
        {
            string URI = string.Format($"https://api.telegram.org/bot{BotToken}/getUpdates");
            var responseString = await client.GetStringAsync(URI);
            Root resp = JsonConvert.DeserializeObject<Root>(responseString);
            int respLength = resp.result.Count - 1;
            int updateID = resp.result[respLength].update_id;
            return updateID;
        }
        //POLL FOR A RESPONSE
        public async Task<string> pollResponse(int seconds)
        {
            int updateIDSave = 0;
            bool receivedMessage = false;
            try
            {
                updateIDSave = await getUpdateID();
            }
            catch
            {
                updateIDSave = 0;
            }
            int updateID = 0;
            System.DateTime timeNow = System.DateTime.Now;
            System.TimeSpan duration = new System.TimeSpan(0, 0, 0, seconds);
            System.DateTime timeDelay = timeNow.Add(duration);
            while(timeDelay>System.DateTime.Now)
            {
                try
                {
                    updateID = await getUpdateID();
                }
                catch
                {
                    updateID = 0;
                }
                if(updateID != updateIDSave)
                {
                    receivedMessage = true;
                    break;
                }
            }
            if (receivedMessage == true)
            {
                string text = await getLastMessage();
                string URI = $"https://api.telegram.org/bot{BotToken}/getUpdates?offset={updateID.ToString()}";
                var responseString = await client.GetStringAsync(URI);
                return text;
            }
            else return "";
        }
    }
