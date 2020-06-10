# python-telegram-bot, emoji 설치
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from emoji import emojize
from bs4 import BeautifulSoup
import time
import requests
import cv2
import datetime
import schedule
#cctv를 위해서
import threading
import numpy


g_bot = None
g_chat_id = None


updater = Updater(token='1116500098:AAGchtRuPtr3C5K8OboGZtUt4Q_Yu1G00iE')
dispatcher = updater.dispatcher
updater.start_polling()


run_thread = False
# 스케줄러 메세지 전송 여부
send_tag =  False




def handler(bot, update):
  text = update.message.text
  chat_id = update.message.chat_id
  global run_thread, send_tag


  if '검색' in text or '순위' in text:
    print('검색순위')
    bot.send_message(chat_id=chat_id, text=search_rank())

  elif '날씨' in text:
      bot.send_message(chat_id=chat_id, text=weather())

  elif '이모티콘' in text:
      print('이모티콘')
      bot.send_message(chat_id=chat_id, text=emojize('아잉:heart_eyes:', use_aliases=True))
    
  elif '사진' in text:
      bot.send_photo(chat_id=chat_id,photo=open('test.jpg','rb'))

  elif 'start' in text:
        if not run_thread:
            
            run_thread=True
            global g_bot, g_chat_id
            g_bot = bot
            g_chat_id = chat_id
            # # 주간보고
            # t = threading.Thread(target=hmx_Report_scheduler, args=(bot, chat_id, 100000))
            # t.daemon=True
            # t.start()
            # # 근태
            # t1 = threading.Thread(target=hmx_Break_scheduler, args=(bot, chat_id,100000))
            # t1.daemon=True
            # t1.start()

            # 스케줄러 동작시킬 Thread
            t = threading.Thread(target=hmx_thread, args=(bot, chat_id, 100000))
            t.daemon=True
            t.start()


            bot.send_message(chat_id, "스케줄러를 시작했습니다.")
        else:
            bot.send_message(chat_id, "스케줄러를 작동중인 상태입니다.")   

  elif 'end' in text:

      run_thread=False
      bot.send_message(chat_id, "스케줄러를 종료합니다.")   

  else:
      print('몰라')
      bot.send_message(chat_id=chat_id, text='몰라')
   





# #####################################################################################################################################



# 스케줄러(주간보고) 함수
def hmx_Report_scheduler():
    print('hmx_Report_scheduler')
    try:
        if run_thread:
            global g_bot, g_chat_id
            hmx_message_send(g_bot, g_chat_id,'수요일 15시까지 change request에 금주/차주 내용 작성 부탁 드립니다. ' + emojize(':smiley:', use_aliases=True))
            hmx_message_send(g_bot, g_chat_id,'그리고 15시에 회의 있습니다.')

    except Exception as e:
        print(e)   


# 밥 주문 함수
def hmx_Food():
    print('hmx_Report_scheduler')
    try:
        if run_thread:
            global g_bot, g_chat_id
            hmx_message_send(g_bot, g_chat_id,'밥 주문하기')

    except Exception as e:
        print(e)           

# 근태 함수
def hmx_Break_scheduler():
    print('hmx_Break_scheduler')
    try:
        if run_thread:
            global g_bot, g_chat_id
            hmx_message_send(g_bot, g_chat_id, "다음달 근태정보 hitops 등록 부탁드립니다.")

    except Exception as e:
        print(e)   


def hmx_message_send(bot, chat_id, msg):
    bot.send_message(chat_id, msg)


# 교통비


# 스케줄러 설정
# 근태 매월 25일 13:15
# schedule.every().day.at("13:15").do(hmx_Break_scheduler)
# schedule.every(25).at("13:15").do(hmx_Break_scheduler)
# 주간보고 매주 13:15
schedule.every().wednesday.at("13:15").do(hmx_Report_scheduler)
schedule.every().days.at("09:15").do(hmx_Food)
# schedule.every(15).seconds.do(hmx_Report_scheduler)
# schedule.every(5).seconds.do(hmx_Break_scheduler)

def hmx_thread(bot, chat_id, tm):
    while run_thread:
        schedule.run_pending() 
        time.sleep(1)


# #####################################################################################################################################


def weather():
    daum_url = requests.get('https://www.daum.net/').text
    daum_p = BeautifulSoup(daum_url, 'html.parser')

    daum_location = daum_p.select('span.txt_part')
    daum_weather = daum_p.select('em.screen_out')

    weather = "다음 날씨 \n"

    for temp in range(0,len(daum_location)):
        print(daum_location[temp].text+" 온도 : ", daum_weather[temp].text)
        weather+= daum_location[temp].text+" 온도 : "+ daum_weather[temp].text + "\n"    
    return weather


def search_rank():
    json = requests.get('https://www.naver.com/srchrank?frm=main').json()

    # json 데이터에서 "data" 항목의 값을 추출test test
    data = json["data"]
    searchList =""

    # 해당 값은 리스트 형태로 제공되기에 리스트만큼 반복
    for temp in data:
        print("rank : ", temp["rank"],' keyword : ', temp["keyword"])
        searchList += "rank : "+ str(temp["rank"])+' keyword : '+temp["keyword"]+"\n"
    return searchList



echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)







