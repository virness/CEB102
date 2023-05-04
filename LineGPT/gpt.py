from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, AudioSendMessage
from flask import Flask, request, abort
import os,openai,requests,json,base64,time,yating_tts_sdk

app = Flask(__name__)

# 設置 Line Bot API 和 WebhookHandler
line_bot_api = LineBotApi('your line token')
handler = WebhookHandler('your line secret')
openai.api_key ='your openai api key'

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 Line 的簽名，驗證訊息是否來自 Line
    signature = request.headers['X-Line-Signature']

    # 取得訊息內容
    body = request.get_data(as_text=True)

    # 進行簽名驗證
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def translate_to_voice(text_input):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        temperature=0.3,
    )
    content = response['choices'][0]['message']['content'].strip()

    input_obj = {
        "input": {
            "text": content,
            "type": "text"
        },
        "voice": {
            "model": "zh_en_female_1"
        },
        "audioConfig": {
            "encoding": "LINEAR16",
            "sampleRate": "16K"
        }
    }

    input_json = json.dumps(input_obj)
    audio_bytes = yating_tts_sdk.synthesize(api_key='your-api-key', input_json=input_json)

    # 將音訊檔存起來
    audio_filename = f'output_{time.time()}.wav'
    with open(audio_filename, 'wb') as f:
        f.write(audio_bytes)

    return audio_filename

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # 發送聲音消息
    audio_message = AudioSendMessage(
        original_content=audio_filename,
        duration=audio_duration
    )
    line_bot_api.push_message(user_id, audio_message)


if __name__ == "__main__":
    app.run()
