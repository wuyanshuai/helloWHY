from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])

def get_tip():
  url = "http://api.tianapi.com/tianqi/index?key=d728c6d14fdbbdb364f0409fdacd398e&city=杭州市"
  res = requests.get(url).json()
  tip = res['newslist'][0]['tips']
  return tip

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, low, high = get_weather()
def get_cloth():
  if temperature >= 25:
    return "宝宝记得穿短袖"
  elif temperature > 15 and temperature <= 24:
    return "宝宝记得穿外套和牛仔裤"
  elif temperature > 0 and  temperature <= 15: 
    return "宝宝记得穿羊毛大衣"
  else : return "宝宝记得穿羽绒服"
data = {"weather":{"value":wea, "color":get_random_color()},"low":{"value":low, "color":get_random_color()},"high":{"value":high, "color":get_random_color()} ,"cloth":{"value":get_tip(), "color":get_random_color()}, "love_days":{"value":get_count(), "color":get_random_color()},"birthday_left":{"value":get_birthday(), "color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
