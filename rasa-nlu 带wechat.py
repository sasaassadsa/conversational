import requests
from bs4 import BeautifulSoup
import urllib
from wxpy import *
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
def get_weather(city):
    apikey='6f2bdd393ff28ee9fd2ef02a318c7f44'
    url='http://apis.juhe.cn/simpleWeather/query?city='+city+'&key='+apikey
    weather=requests.get(url).json()
    now_weather = weather['result']['realtime']
    temperature = now_weather['temperature']
    humidity = now_weather['humidity']
    info = now_weather['info']
    wid = now_weather['wid']
    direct = now_weather['direct']
    power = now_weather['power']
    aqi = now_weather['aqi']
    result='温度：%s\n湿度：%s\n天气：%s\n风：%s\n风向：%s\n大小：%s\n空气质量指数：%s\n'%(temperature,humidity,info,wid,direct,power,aqi)
    return result
def get_nba():
    resp = urllib.request.urlopen('https://m.hupu.com/nba/game')
    soup = BeautifulSoup(resp, 'html.parser')
    tagToday = soup.find('section', class_="match-today")
    nbaHtml = '今日NBA比赛结果：' + '\n' + '\n'
    for tag in tagToday.find_all('a', class_='match-wrap'):
        nbaHtml = nbaHtml + tag.find('div', class_='away-team').span.get_text() + '    ' + tag.find('strong',
                                                                                                    class_='').span.get_text() + '    ' + tag.find(
            'div', class_='home-team').span.get_text() + '  (' + tag.find('div',
                                                                          class_='match-status-txt').get_text() + ')' + '\n'

    return nbaHtml


def get_rank():
    resp = urllib.request.urlopen('https://m.hupu.com/nba/stats')
    soup = BeautifulSoup(resp, 'html.parser')
    east = soup.find_all('li', class_="weast")[0]
    west = soup.find_all('li', class_="weast")[1]
    rankHtml = '今日NBA东部排名：（1.排名  2.球队  3.胜负  4.胜负差  5.最近情况）' + '\n' + '\n'
    for tag in east.find_all('li', class_=''):
        list = tag.find('p', class_='right-data')
        rankHtml = rankHtml + tag.find('span', class_='rank').get_text() + '. ' + tag.find('div',
                                                                                           class_='').h1.get_text() + '    ' + \
                   list.find_all('span')[0].get_text() + '    ' + list.find_all('span')[1].get_text() + '    ' + \
                   list.find_all('span')[2].get_text() + '\n'

    rankHtml = rankHtml + '\n' + '\n' + '---------------------------------------------' + '\n' + '\n'
    rankHtml = rankHtml + '今日NBA西部排名：（1.排名  2.球队  3.胜负  4.胜负差  5.最近情况）' + '\n' + '\n'
    for tag in west.find_all('li', class_=''):
        list = tag.find('p', class_='right-data')
        rankHtml = rankHtml + tag.find('span', class_='rank').get_text() + '. ' + tag.find('div',
                                                                                           class_='').h1.get_text() + '    ' + \
                   list.find_all('span')[0].get_text() + '    ' + list.find_all('span')[1].get_text() + '    ' + \
                   list.find_all('span')[2].get_text() + '\n'

    return rankHtml
trainer = Trainer(config.load("/content/Conversational/config_spacy.yml"))
training_data = load_data('/content/Conversational/demo-rasa.json')
interpreter = trainer.train(training_data)
responses = {'greet': 'Hello you! :)',
             'thank you': 'you are very welcome',
             'affirm': 'Ok,I will do this. Please wait.',
             'goodbye': 'goodbye for now'
            }

bot = Bot()
@bot.register(Friend, TEXT)
def print_friend_msg(msg):
    print(msg.text)
    data = interpreter.parse(message)
    if data['intent']['name'] in responses.items():
        key = intents
    msg.chat.send(responses[key])
    if data['intent']['name']=='weather_search':
        get_now_weather = get_weather('南京')
        msg.chat.send(get_now_weather)
    if data['intent']['name']=='team_search':
        b = get_rank()
        msg.chat.send(b)
    if data['intent']['name']=='result_search':
        a = get_nba()
        msg.chat.send(a)
bot.join()


