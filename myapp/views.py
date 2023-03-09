from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage
from linebot.models import TextSendMessage, ImageSendMessage
import openai, os


openai.api_key = os.getenv("OPENAI_API_KEY")
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

	

	


class Dalle:  
    

    def __init__(self):
        
        self.image_url = ""



    def get_response(self, user_input):
        #import openai
        #openai.api_key = openai.api_key
        response = openai.Image.create(
            prompt = user_input,
                n=1,
            size="1024x1024"
            )
        self.image_url = response['data'][0]['url'].strip()
        print(self.image_url)


        
        return self.image_url
	



dalle = Dalle()

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
            ##############
                    user_message = event.message.text        

                                
                    #reply_dalle_url = dalle.get_response(user_message="beautiful Taiwanese girl")
                    reply_dalle_url = dalle.get_response(user_message)

                    line_bot_api.reply_message(
                        event.reply_token,
                        #TextSendMessage(text=reply_dalle_url)
                        ImageSendMessage(original_content_url=reply_dalle_url, preview_image_url=reply_dalle_url)
                        )


            ##########################

                     
                                              
                
        return HttpResponse()

    else:
        return HttpResponseBadRequest()


