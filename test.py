import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from flask import Flask
import pdfconverter
from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)

ask = Ask(app, "/")
a = []
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():

    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("HelloIntent")
def next_round1():
    return new_game()

@ask.intent("StopIntent")
def stop():
    return statement("Stopping")

@ask.session_ended
def session_ended():
    return "",200
@ask.intent("MyNameIsIntent")
def getName(firstname):
    print(firstname)
    msg = firstname+" Please upload the resume , and  mention when you are ready after uploading "
    return question(msg)

def call_pdf():
    global a
    a = list(pdfconverter.ret_questions())
    print(a)

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename("uploadedFile.pdf"))
        call_pdf()
        return 'file uploaded successfully'

@ask.intent("YesIntent")
def next_round():
    if len(a) == 0:
        return statement("Well Done! Have a good time at your real interview!")
    b = a.pop()
    return question(b)

@ask.intent("NextIntent")
def new_round(answer):
    return next_round()


@ask.intent("AnswerIntent", convert={'first': str})
def answer(first):
    return statement(first)


if __name__ == '__main__':

    app.run(debug=True)