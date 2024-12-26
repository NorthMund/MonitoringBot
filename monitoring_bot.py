import telebot
import subprocess
import psutil
import re
from telebot import types
import time
from threading import Thread

#PASTE YOUR TELEGRAM BOT API TOKEN
API_token = "Your TG API token"

# How often will the bot check server statistics (in seconds)
metrics_frequency = 60

#Limits for alerting
cpu_limit=50
temp_limit=60
ram_limit=65

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



bot = telebot.TeleBot(API_token)

@bot.message_handler(commands=['stats'])
def stats(message):
    bot.reply_to(message, 
        f"<b><em>Server stats:</em></b>\n"
        f"CPU Usage: <b><em>{get_cpu_usage()}%</em></b>\n"
        f"CPU Temp: <b><em>{get_cpu_temperature()}°</em></b>\n"
        f"RAM Used: <b><em>{get_ram_percent()}%</em></b>\n"
        f"Available RAM: <b><em>{get_ram_available()}GB</em></b>\n",parse_mode='html'
    )

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
    monitor_thread = Thread(target=monitor_server, args=(chat_id,cpu_limit,temp_limit,ram_limit))
    monitor_thread.daemon = True
    monitor_thread.start()

@bot.message_handler(commands=['start_monitoring'])
def start_monitoring_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🛠️ Monitoring started.")
    start_monitoring(chat_id)    


bot.polling(none_stop=True)




