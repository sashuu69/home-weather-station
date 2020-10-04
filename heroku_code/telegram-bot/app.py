import re
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,URL


global bot
global TOKEN
TOKEN = bot_token
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

   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
       bot_welcome = """
       HOME WEATHER STATION
       
       Welcome to Sashwat's Home Weather Station. Use the following commands for stats:-
       1. /stats - Gives all values
       2. /AQI (MQ-135) - Air Quality Index in PPM
       3. /CNG (MQ-4) - Compressed Natural Gas in PPM
       4. /HI (DHT22) - Heat Index in Celsius
       5. /HUM (DHT22) - Humidity in Percentage
       6. /TEM (DHT22) - Temperature in Celsius
       7. /LPG (MQ-5) - LPG in PPM
       8. /RAIN - Analog Value
       9. /SMKE (MQ-2) - Smoke in in PPM
       
       NOTES:-
       1. Project under development.
       2. Gas sensors need Calibration.
       3. More features will be added soon.

       Features:-
       1. Get Latest sensor values from sensors.

       GITHUB PROJECT LINK - https://github.com/sashuu6/home-weather-station
       """
       
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    if text == "/start":

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
           bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

   return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
   if s:
       return "HOME WEATHER STATION WEBHOOK WORKING PROPERLY. STATUS: 200"
   else:
       return "HOME WEATHER STATION WEBHOOK ERROR. STAUS: 400"

@app.route('/')
def index():
   return '.'


if __name__ == '__main__':
   app.run(threaded=True)