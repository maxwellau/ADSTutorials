import requests
from datetime import datetime, timedelta
class telegramBot:
    def __init__(self, botToken, chatID, graphDirectory):
        assert botToken == str(botToken), 'Name has to be a string'
        assert chatID == str(chatID), 'Color has to be a string'
        assert graphDirectory == str(graphDirectory), 'Directory has to be a string'
        self.botToken = botToken
        self.chatID = chatID
        self.graphDirectory = graphDirectory

    def sendText(self, msg):
        try:
            base_url = f'https://api.telegram.org/bot{self.botToken}/sendMessage?chat_id={self.chatID}&text={msg}'
            requests.post(base_url)  # Sending automated message
            return "Text Sent"
        except:
            return "Failed to send Text"

    def sendGraph(self, graph):
        try:
            graph.write_image(self.graphDirectory)
            imgpath = {'photo': open(self.graphDirectory, 'rb')}
            requests.post(
                f'https://api.telegram.org/bot{self.botToken}/sendPhoto?chat_id={self.chatID}',
                files=imgpath)  # Sending Automated Image
            return "Graph Sent"
        except:
            return "Failed to send Graph"

    def sendImage(self, directory):
        try:
            imgpath = {'photo': open(directory, 'rb')}
            requests.post(
                f'https://api.telegram.org/bot{self.botToken}/sendPhoto?chat_id={self.chatID}',
                files=imgpath)  # Sending Automated Image
            return "Image Sent"
        except:
            return "Failed to send Image"

    def pollResponse(self, specifity, waittime):
        assert waittime == float(waittime), 'waittime has to be a float'
        assert '-' not in self.chatID, 'ChatID is that of a Channel, unable to poll for responses'
        assert type(specifity) == bool, 'Specificity has to be a Boolean Value'
        site = f'https://api.telegram.org/bot{self.botToken}/getUpdates'
        data = requests.get(site).json()  # reads data from the url getUpdates
        try:
            lastMsg = len(data['result']) - 1
            updateIdSave = data['result'][lastMsg]['update_id']
        except:
            updateIdSave = ''
        time = datetime.now()
        waitTime = time + timedelta(seconds=waittime)

        while True:
            try:
                data = requests.get(site).json()  # reads data from the url getUpdates
                lastMsg = len(data['result']) - 1
                updateId = data['result'][lastMsg]['update_id']
                chatid = str(data['result'][lastMsg]['message']['chat']['id'])  # reads chat ID
                if specifity == True:
                    condition = self.chatID == chatid
                else:
                    condition = True
                if updateId != updateIdSave and condition:  # compares update ID
                    try:
                        text = data['result'][lastMsg]['message']['text']  # reads what they have sent\
                        break
                    except:
                        pass
                if waitTime < datetime.now():
                    text = 'null'
                    break
            except:
                pass
        requests.get(
            f'https://api.telegram.org/bot{self.botToken}/getUpdates?offset=' + str(updateId))
        return text
