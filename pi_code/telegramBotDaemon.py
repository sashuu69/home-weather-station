from flask import Flask, request
import telegram

# from dotenv import load_dotenv  # for accessing environment (.env) file
# import os  # for supporting dotenv

TOKEN = "1309397081:AAFOR5ybQZzXbNcKN3-WYhZJ5okatgk2nUE" #os.getenv("telegramAPI")
bot_user_name = "HomeWeatherStationBot" #os.getenv("botUserName")
URL = "https://sashuu6-home-weather-station.herokuapp.com/"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)

   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)
   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
       # print the welcoming message
       bot_welcome = """
       HOME WEATHER STATION
       --------------------
       Welcome to my home weather station.
       Use the following commands to get values from the bot.
       1. /getAllValues - Gives all the currrent values collected by the device.
       2. /AQI - Air Quality Index
       3. /CNG - Compressed Natural Gas
       4. /HI - Heat Index
       5. /HUM - Humidity
       6. /TEM - Temperature
       7. /LPG - Liquid Petroleum Gas
       8. /RAIN - Analog Value from Rain Sensor
       9. /SMKE - SMOKE

       Note : More comming soon. The gas sensors values are not accurate yet. Still under calibration.
       """
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

   else:
       try:
           # clear the message we got from any non alphabets
           text = re.sub(r"\W", "_", text)
           # create the api link for the avatar based on http://avatars.adorable.io/
           url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
           # reply with a photo to the name the user sent,
           # note that you can send photos by url and telegram will fetch it for you
           bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
       except Exception:
           # if things went wrong
           bot.sendMessage(chat_id=chat_id, text="Please send a valid command", reply_to_message_id=msg_id)

   return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'
if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)
