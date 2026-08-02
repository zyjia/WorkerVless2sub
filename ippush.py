import os
import re
import json
import time
import sys
import requests



# 推送信息
TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', 'xxxxxx')
TG_USER_ID = os.environ.get('TG_USER_ID', '111111')
# TG_API_HOST = os.environ.get('TG_API_HOST', 'api.telegram.org')

# 定义一些变量
desp = ""

# 保持连接,重复利用
ss = requests.session()
# 全局基础请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
}

def unix_time_to_date(t):
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)))

def log(info: str):
    print(info)
    global desp
    desp = desp + info + "\n"

def telegram():
    try:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': TG_USER_ID,
            'text': f"CloudFlare优选IP推送\n{desp}",
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=data)
        if response.status_code != 200:
            log('Telegram Bot 推送失败')
        else:
            log('Telegram Bot 推送成功')
    except Exception as e:
        log(f"Telegram推送时出错: {str(e)}")


    
if __name__ == "__main__":
    response = requests.get('https://box.zyjia.pp.ua/app/warp/ipush.php')
    # data = response.json()
    desp = response.text

    # 消息推送
    if TG_BOT_TOKEN and TG_USER_ID and len(desp) > 0:
        telegram()
        sys.exit(0)
