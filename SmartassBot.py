import telegram
from pytube import Playlist
import youtube_dl
import os
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, ConversationHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import pandas as pd
import random
import logging

PORT = int(os.environ.get("PORT", "ENTER YOUR PORT"))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "ENTER YOUR TOKEN"
bot = telegram.Bot(TOKEN)
ONE, TWO, THREE, FOUR, FIVE = range(5)

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
def start(update, context):
    update.message.reply_text("Thank for using this bot, in here, you can try every functions provided.To see more functions, type /help")

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
def music(update, context):
    update.message.reply_text("Send youtube link here to play")
    return ONE

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
def music_reply(update, context):
    if update.message.text.startswith("/"):
        return ConversationHandler.END
    elif "youtu" not in update.message.text:
        update.message.reply_text("This is not an effective youtube link")
    else:
        single_song_downloader(update, update.message.text)

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
def single_song_downloader(update, url):
    try:            # playlist
        playlist = Playlist(url)
        global links
        links = playlist.video_urls  # lists of url
        update.message.reply_text(f"Songs in playlist: {len(links)}")
        update.message.reply_text("How many songs would you like to download? You cannot use other function until songs are all downloaded",
                              reply_markup=InlineKeyboardMarkup([
                                  [InlineKeyboardButton("5", callback_data="5"), InlineKeyboardButton("10", callback_data="10")],
                                  [InlineKeyboardButton("15", callback_data="15"), InlineKeyboardButton("20", callback_data="20")],
                                  [InlineKeyboardButton("Download all, I don't mind to wait", callback_data="all")],
                              ]))
        return ONE

    except:    # 單曲
        global name
        chat_id = update.message.from_user.id
        if "youtu" in url:
            try:
                ydl_opts = {
                    'outtmpl': '%(title)s.%(ext)s',
                    'format': 'bestaudio',
                    'noplaylist': True,
                    'writethumbnail': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '190',
                    }],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url)
                name = info['title']
                audio = open(name + '.mp3', 'r+b')
                bot.send_audio(chat_id=chat_id, audio=audio)
                audio.close()
                os.remove(name + '.mp3')
            except:
                update.message.reply_text(f"Maybe this not the good time to download this song: '\n{name}.mp3'")
        else:
            update.message.reply_text('Does not looks like an youtube link')
        update.message.reply_text("Finish!")
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★

def playlist_downloader(update, urls):    # 歌單
    global name, num
    query = update.callback_query
    query.answer("Okay")
    chat_id = query.from_user.id
    orders = [i for i in range(len(links))]
    for i in range(5):
        random.shuffle(orders)
    if query.data == "5":
        num = 5
    elif query.data == "10":
        num = 10
    elif query.data == "15":
        num = 15
    elif query.data == "20":
        num = 20
    elif query.data == "all":
        num = len(links)
    for i in range(num):
        link = links[orders[i]]
        if "youtu" in link:
            try:
                ydl_opts = {
                    'outtmpl': '%(title)s.%(ext)s',
                    'format': 'bestaudio',
                    'noplaylist': True,
                    'writethumbnail': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '190',
                    }],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link)
                name = info['title']
                # 根據youtube naming 習慣
                audio = open(name + '.mp3', 'r+b')
                bot.send_audio(chat_id=chat_id, audio=audio)
                audio.close()
                os.remove(name + '.mp3')
            except:
                query.message.reply_text("Cannot download this song")
        else:
            query.message.reply_text('Does not looks like an youtube link')
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★

def test(update, context):
    update.message.reply_text("Coming soon 🙇‍♂!!")
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★

def stock(update, context):
    update.message.reply_text("Which searching engine would you like to use?",
                              reply_markup=InlineKeyboardMarkup([
                                  [InlineKeyboardButton("Yahoo Finance", callback_data="Yahoo Finance")],
                                  [InlineKeyboardButton("Investing.com", callback_data="Investing.com")],
                                  [InlineKeyboardButton("AAStocks", callback_data="AAStocks")],
                              ]))
    return ONE
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★

def stock_agent(update, context):
    global Agent
    query = update.callback_query
    query.answer("Okay")
    if query.data == "Yahoo Finance":
        Agent = "Yahoo Finance"
        query.message.reply_text("Send me the code or name of the stock")

    elif query.data == "Investing.com":
        Agent = "Investing.com"
        query.message.reply_text("Send me the code or name of the stock")

    elif query.data == "AAStocks":
        Agent = "AAStocks"
        query.message.reply_text("Send me the code or name of the stock")
    return TWO
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★

def stock_reply(update, context):
    if not update.message.text.startswith("/"):
        update.message.reply_text(f"Checking: {update.message.text}")
        if Agent == "Yahoo Finance":
            yahoo_stock(update, update.message.text)

        elif Agent == "Investing.com":
            investing_stock(update, update.message.text)

        elif Agent == "AAStocks":
            aastocks_stock(update, update.message.text)
    else:
        return ConversationHandler.END
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★

def yahoo_stock(update, stock_code):
    try:
        url = f"https://partner-query.finance.yahoo.com/v8/finance/chart/{stock_code}?range=1d&comparisons=undefined&includePrePost=false&interval=2m&corsDomain=tw.stock.yahoo.com&.tsrc=yahoo-tw"
        # 模擬瀏覽器, 避免http error[403]
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'}
        response = requests.get(url, headers=headers)
        json_data = response.json()

        open_ = json_data['chart']['result'][0]['meta']['chartPreviousClose']  # 開市價
        close_ = json_data['chart']['result'][0]['meta']['regularMarketPrice']  # 收市價
        current_price_ = json_data['chart']['result'][0]['indicators']['quote'][0]['close'][-1]  # 目前價位
        high_ = max(json_data['chart']['result'][0]['indicators']['quote'][0]['high'])  # 最高位
        low_ = min(json_data['chart']['result'][0]['indicators']['quote'][0]['low'])  # 最低位

        update.message.reply_text(
            f"Current: ${round(current_price_, 2)},    Open: $ {round(open_, 2)},    Close: ${round(close_, 2)}, \nHighest price: ${round(high_, 2)},    Lowest price: ${round(low_, 2)}")

        price_level = json_data['chart']['result'][0]['indicators']['quote'][0]['close']  # 價位s
        timestamp = json_data['chart']['result'][0]['timestamp']  # 時間軸s

        df = pd.DataFrame({'timestamp': timestamp, 'price_level': price_level})
        df['timestamp'] = pd.to_datetime(df['timestamp'] + 3600 * 8, unit='s')  # 時區為 +8 , 所以 8 * 60秒 * 60分鐘

        # x-axis, y-axis
        fig = df.plot("timestamp", "price_level", figsize=(12, 8)).get_figure()
        fig.savefig('stock.png')
        img = 'stock.png'
        chat_id = update.message.from_user.id
        bot.send_photo(chat_id=chat_id, photo=open(img, "r+b"))

    except:
        update.message.reply_text("You have enter the wrong code, Please try again.")
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★

def investing_stock(update, stock_code):
    update.message.reply_text("Coming Soon")
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★

def aastocks_stock(update, stock_code):
    try:
        url = f"http://www.aastocks.com/tc/usq/quote/quote.aspx?symbol={stock_code}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'}
        response = requests.get(url, headers=headers)

    except:
        update.message.reply_text("You have enter the wrong code, Please try again.")

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★

def weather(update, context):
    update.message.reply_text("Type the area or region you want to check")
    return ONE
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★

def weather_reply(update, context):
    if not update.message.text.startswith("/"):
        weatherReport(update, context, update.message.text)
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★

def mood(update, context):
    global mood
    mood = True
    update.message.reply_text("Tell me your feeling at this moment", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Positive😀", callback_data="Positive")],
        [InlineKeyboardButton("Negative😟", callback_data="Negative")],
        [InlineKeyboardButton("Just give me a random song🙏", callback_data="Random")],
    ]))
    return ONE
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★

def mood1(update, context):
    query = update.callback_query
    query.answer("Great")
    if query.data == "Positive":
        query.message.reply_text("★━━━━━━━━━━━━━━━━━━━━━━━━━━★")
        query.message.reply_text("Which emotion best describe you?", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Happy😆", callback_data="Happy")],
            [InlineKeyboardButton("Exciting🥳", callback_data="Exciting")],
            [InlineKeyboardButton("Surprised🤩", callback_data="Surprised")],
        ]))
    elif query.data == "Negative":
        query.message.reply_text("★━━━━━━━━━━━━━━━━━━━━━━━━━━★")
        query.message.reply_text("Which emotion best describe you?", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Uncertain😖", callback_data="Uncertain")],
            [InlineKeyboardButton("Sad😢", callback_data="Sad")],
            [InlineKeyboardButton("Angry😡", callback_data="Angry")],
            [InlineKeyboardButton("Upset😢", callback_data="Upset")],
        ]))
    else:
        link = "https://www.youtube.com/watch?v=ru0K8uYEZWw&list=PLW9z2i0xwq0F3-8LieqflLLWLWZQgvhEX"
        mood_song_downloader(update, link)
    return TWO
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★

def mood2(update, context):
    global link
    query = update.callback_query
    query.answer("Command received, please wait...")
    if query.data == "Happy":
        link = "https://www.youtube.com/watch?v=ru0K8uYEZWw&list=PLW9z2i0xwq0F3-8LieqflLLWLWZQgvhEX"

    elif query.data == "Exciting":
        link = "https://www.youtube.com/watch?v=hT_nvWreIhg&list=PLhGO2bt0EkwvRUioaJMLxrMNhU44lRWg8"

    elif query.data == "Surprised":
        link = "https://www.youtube.com/watch?v=TEAylKJb-to&list=PL468A17AB960732DE"

    elif query.data == "Uncertain":
        link = "https://www.youtube.com/watch?v=RgKAFK5djSk&list=PLeCdlPO-XhWFzEVynMsmosfdRsIZXhZi0"

    elif query.data == "Sad":
        link = "https://www.youtube.com/watch?v=UAWcs5H-qgQ&list=PLukmLBQXntBmFhTcYnxJ6RcEjp80HvaLk"

    elif query.data == "Angry":
        link = "https://www.youtube.com/watch?v=gNi_6U5Pm_o&list=PL7v1FHGMOadBhCjuh_ljEEhqrQKCBsoIn"

    elif query.data == "Upset":
        link = "https://www.youtube.com/watch?v=uWRlisQu4fo&list=PLgzTt0k8mXzHcKebL8d0uYHfawiARhQja"

    mood_song_downloader(update, link)

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
def mood_song_downloader(update, link):
    query = update.callback_query
    playlist = Playlist(link)
    links = playlist.video_urls
    chat_id = query.from_user.id
    orders = [i for i in range(len(links))]
    query.message.reply_text("★━━━━━━━━━━━━━━━━━━━━━━━━━━★")
    query.message.reply_text("I now send you 10 related songs")
    for i in range(5):
        random.shuffle(orders)
        link = links[orders[i]]
        if "youtu" in link:
            try:
                ydl_opts = {
                    'outtmpl': '%(title)s.%(ext)s',
                    'format': 'bestaudio',
                    'noplaylist': True,
                    'writethumbnail': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '190',
                    }],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link)
                name = info['title']
                # 根據youtube naming 習慣
                audio = open(name + '.mp3', 'r+b')
                bot.send_audio(chat_id=chat_id, audio=audio)
                audio.close()
                os.remove(name + '.mp3')
            except:
                query.message.reply_text("Cannot download this song")
        else:
            query.message.reply_text('Does not looks like an youtube link')

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
def help(update, context):
    update.message.reply_text(" Hi👋, I' going to guide you to use this bot🤖️\n 1. to receive psychological test🧐, \nenter command /test\n\n 2. to check the weather⛅ of a region, \nenter /weather \n\n 3. to check for stock info.👩‍💻, \nenter /stock \n\n 4. to play a song suits your mood, \nenter /mood\n\n 5. If you want listen to music,  \nenter /music \n\nIf you have any questions, \nplease contact me @ ......😆")

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
def cancel(update, context):
    update.message.reply_text('Conversation ended')
    return ConversationHandler.END

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
def weatherReport(update, context, check):
    api_url = "http://api.openweathermap.org/data/2.5/weather"
    r = requests.post(url=api_url, params={"q": check, "APPID": "YOUR API ID IN OPENWEATHER", "units": "metric"})
    data = r.json()
    global main, desc, temp, temp_max, temp_min, humidity, cloudiness, speed, deg, gust
    for i in data["weather"]:
        for k, v in i.items():
            if k == "main":
                main = v
            elif k == "description":
                desc = v

    for k, v in data["main"].items():
        if k == "temp":
            temp = v
        elif k == "temp_min":
            temp_min = v
        elif k == "temp_max":
            temp_max = v
        elif k == "humidity":
            humidity = v

    for k, v in data["clouds"].items():
        cloudiness = v

    for k, v in data["wind"].items():
        if k == "speed":
            speed = v
        elif k == "deg":
            deg = v
        elif k == "gust":
            gust = v

    name = data['name']
    update.message.reply_text(
        f"In {name},\n weather ⛅️: {main}({desc}), \n temp☀️:{temp}°C, max.🔥: {temp_max}°C, min. {temp_min}°C\n"
        f" humid.💧:{humidity}%, cloudness☁️:{cloudiness}%, \n wind-speed💨:{speed}m/sec, degree:{deg}°, wind-gust:{gust} m/sec.")

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
"""Execution part"""
updater = Updater(TOKEN)
dp = updater.dispatcher

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
"""Creating ConversationHandlers"""
# For music
conv_handler_music = ConversationHandler(
    entry_points=[CommandHandler("music", music)],
    states={
        ONE: [MessageHandler(Filters.text, music_reply), CallbackQueryHandler(playlist_downloader)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
# For weather
conv_handler_weather = ConversationHandler(
    entry_points=[CommandHandler("weather", weather)],
    states={
        ONE: [MessageHandler(Filters.text, weather_reply)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
# For stock
conv_handler_stock = ConversationHandler(
    entry_points=[CommandHandler("stock", stock)],
    states={
        ONE: [CallbackQueryHandler(stock_agent)],
        TWO: [MessageHandler(Filters.text, stock_reply)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
# For mood
conv_handler_mood = ConversationHandler(
    entry_points=[CommandHandler("mood", mood)],
    states={
        ONE: [CallbackQueryHandler(mood1)],
        TWO: [CallbackQueryHandler(mood2)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
# For psychological test: Coming Soon
conv_handler_test = ConversationHandler(
    entry_points=[CommandHandler("test", test)],
    states={},
    fallbacks=[CommandHandler("cancel", cancel)],
)

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
"""Applying Handler"""
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))

dp.add_handler(conv_handler_stock, 1)
dp.add_handler(conv_handler_mood, 1)
dp.add_handler(conv_handler_test, 1)
dp.add_handler(conv_handler_weather, 1)
dp.add_handler(conv_handler_music, 1)

# ★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★━━━━━━━━━━━━━━━━━━━━★
"""Forever running"""

updater.start_webhook(listen="0.0.0.0",
                      port=int(PORT),
                      url_path=TOKEN,
                      webhook_url="https://nameofyourapp.herokuapp.com/" + TOKEN)
updater.idle()