import telebot
import subprocess
import psutil
import re
from telebot import types
import time
from threading import Thread
import os


# How often will the bot check server statistics (in seconds)
metrics_frequency = 20

#Limits for alerting
cpu_limit=60
temp_limit=60
ram_limit=80

#Variable to check if monitoring already enabled
is_monitoring_enabled=False

#Path to file with token. Default: ./token
token_file_path="token"

def get_token():
    global API_token
    if not os.path.exists(token_file_path):
        with open(token_file_path, "w") as file:
            file.write("PUT YOUR TG API TOKEN HERE")

    with open(token_file_path, "r") as file:
        API_token = file.read().strip()
get_token()

def bytes_to_gigabytes(value):
    return round(value/1024**3,2)

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_cpu_temperature():
    temps = []
    try:
        sensors_output = subprocess.check_output(['sensors'], encoding='utf-8')
        for line in sensors_output.splitlines():
            if 'Core' in line:
                parts = line.split()
                for part in parts:
                    tmpre = '^\+(\d{1,2}(\.\d{1,2})?)°C$'
                    if re.match(tmpre,part):
                        part = part.replace("°", "").replace("C", "")
                        part = float(part)
                        temps.append(part)
        average_temp = sum(temps)/len(temps)
        return round(average_temp,1)
    except subprocess.CalledProcessError:
        return "Error getting CPU temp"
    
def get_ram_percent():
    memory = psutil.virtual_memory()
    return memory.percent

def get_ram_available():
    memory = psutil.virtual_memory()
    return bytes_to_gigabytes(memory.available)

if not API_token=="":
    bot = telebot.TeleBot(API_token)
else:
    print(f"Put your TG bot token in {token_file_path} file!")

@bot.message_handler(commands=['limits'])
def limits(message):
        chat_id = message.chat.id
        response = (
            f"🛠️ CPU usage threshhold: {cpu_limit}%\n"
            f"🛠️ CPU temperature threshhold: {temp_limit}°\n"
            f"🛠️ RAM usage threshhold: {ram_limit}%\n"
        )
        bot.send_message(chat_id,response,parse_mode='html')

@bot.message_handler(commands=['stats'])
def stats(message):
    response = (
        f"<b><em>Server stats:</em></b>\n"
        f"CPU Usage: <b><em>{get_cpu_usage()}%</em></b>\n"
        f"CPU Temp: <b><em>{get_cpu_temperature()}°</em></b>\n"
        f"RAM Used: <b><em>{get_ram_percent()}%</em></b>\n"
        f"Available RAM: <b><em>{get_ram_available()}GB</em></b>"
    )
    if is_monitoring_enabled:
        response+="\n\n<b><em>🟢 Monitoring enabled.</em></b>"
    bot.reply_to(message, response,parse_mode='html')

def monitor_server(chat_id, cpu_limit, temp_limit, ram_limit):
    while True:
        cpu_usage = get_cpu_usage()
        cpu_temp = get_cpu_temperature()
        ram_usage = get_ram_percent()

        if cpu_usage > cpu_limit:
            bot.send_message(chat_id, f"⚠️ High CPU usage: {cpu_usage}%!")
        if cpu_temp and cpu_temp > temp_limit:
            bot.send_message(chat_id, f"⚠️ High CPU temp: {cpu_temp}°C!")
        if ram_usage > ram_limit:
            bot.send_message(chat_id, f"⚠️ High RAM usage: {ram_usage}%!")


        time.sleep(metrics_frequency)


def start_monitoring(chat_id):
    global is_monitoring_enabled
    if is_monitoring_enabled:
        bot.send_message(chat_id, "🛠️ Monitoring already started.")
    elif not is_monitoring_enabled:
        monitor_thread = Thread(target=monitor_server, args=(chat_id,cpu_limit,temp_limit,ram_limit))
        monitor_thread.daemon = True
        monitor_thread.start()
        bot.send_message(chat_id, "🛠️ Monitoring started.")
        is_monitoring_enabled=True


@bot.message_handler(commands=['start_monitoring'])
def start_monitoring_handler(message):
    chat_id = message.chat.id
    start_monitoring(chat_id)    


bot.polling(none_stop=True)




