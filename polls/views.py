from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def index(request):
    return HttpResponse('this is polls project page')


from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 

@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                result = forecast(event.message.text)
            
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=result)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
    
    
import twstock
from twstock import Stock   
def forecast(stockId):
    twstock.__update_codes()
    name = twstock.codes[str(stockId)].name
    stock = Stock(str(stockId))
    
    sumprice1 = sum(stock.price[-4:])
    aver_price1 = round(sumprice1/4,2)
    sumprice2 = sum(stock.price[-9:])
    aver_price2 = round(sumprice2/9,2)
    sumprice3 = sum(stock.price[-19:])
    aver_price3 = round(sumprice3/19,2)
    return f'''{name}{stockId}: 
        5日線股價: {aver_price1} 
        10日線股價: {aver_price2} 
        20日線股價: {aver_price3}'''