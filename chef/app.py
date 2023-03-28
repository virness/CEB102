from flask import Flask, render_template, request, render_template_string
import openai,os


openai.api_key = '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'
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/question', methods=['POST'])
def question():
    message = request.form['message']
    several = request.form['num_people']
    diet = request.form['dietary_restrictions']
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt='現在你是廚師。下面會敘述的飲食偏好，你會推薦我嘗試的食譜或是食材可以做什麼，如果後面的問題跟料理無關 請回答 這與料理無關無法回答哦 不要其他結果。我們總共有'+several+'人，'+diet+'，'+message + "。請介紹食材份量及步驟。並用繁體中文回答",
        max_tokens=2048,
        temperature=0.3,
        )
    return render_template('index.html', response=response.choices[0].text)


if __name__ == '__main__':
    app.run(port=5566)
