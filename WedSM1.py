import os
import requests
from telegram.ext import Updater, CommandHandler
from bs4 import BeautifulSoup
import time
import random

# أفضل 10 مواقع تواصل اجتماعي
SOCIAL_MEDIA_SITES = [
    'https://www.facebook.com',
    'https://www.youtube.com',
    'https://www.instagram.com',
    'https://www.tiktok.com',
    'https://www.twitter.com',
    'https://www.linkedin.com',
    'https://www.snapchat.com',
    'https://telegram.org',
    'https://www.pinterest.com',
    'https://www.whatsapp.com'
]

# إعدادات البروكسي
PROXIES = [
    {"http": "http://45.61.139.48:8011", "https": "http://45.61.139.48:8011"},
    {"http": "http://103.175.237.123:3128", "https": "http://103.175.237.123:3128"}
]

# استخراج التوكن من متغيرات البيئة
TOKEN = os.environ.get('BOT_TOKEN')  # التعديل الرئيسي هنا

if not TOKEN:
    raise ValueError("❗ لم يتم تعيين التوكن. يرجى إضافة BOT_TOKEN إلى متغيرات البيئة")

def get_random_proxy():
    return random.choice(PROXIES)

def get_random_user_agent():
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    ]
    return {'User-Agent': random.choice(agents)}

def scrape(bot, update):
    try:
        message = "📊 النتائج:\n\n"
        for site in SOCIAL_MEDIA_SITES:
            try:
                proxy = get_random_proxy()
                headers = get_random_user_agent()
                response = requests.get(site, proxies=proxy, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.title.string if soup.title else "لا يوجد عنوان"
                    message += f"✅ {site}\n- العنوان: {title[:50]}...\n\n"
                time.sleep(2)
            except Exception as e:
                message += f"❌ {site} - خطأ: {str(e)}\n\n"
        
        bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        bot.send_message(chat_id=update.message.chat_id, text=f"حدث خطأ: {str(e)}")

def start(bot, update):
    welcome = """
    🚀 مرحباً! أنا بوت استخراج بيانات مواقع التواصل الاجتماعي.
    الأوامر المتاحة:
    /start - عرض هذه الرسالة
    /scrape - بدء الاستخراج
    """
    bot.send_message(chat_id=update.message.chat_id, text=welcome)

# تشغيل البوت
updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("scrape", scrape))
updater.start_polling()
print("✅ البوت يعمل الآن!")
updater.idle()
