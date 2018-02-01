import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from flask import Flask
import pdfconverter

app = Flask(__name__)

ask = Ask(app, "/")
a = []
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():

    welcome_msg = render_template('welcome')
    global a
    a = list(pdfconverter.ret_questions())
    print(a)
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
    msg = "Shall we start with the interview,"+firstname
#    return statement(msg).simple_card("Hello {}".format(firstname), msg)
    return question(msg)


@ask.intent("CoolIntent")
def next_round():

    #numbers = [randint(0, 9) for _ in range(3)]
    #round_msg = render_template('round', numbers=numbers)
    #session.attributes['numbers'] = numbers[::-1]  # reverse
    b = a.pop()

    return question(b)

@ask.intent("NextIntent")
def new_round(answer):
    print (answer)
    #numbers = [randint(0, 9) for _ in range(3)]
    #round_msg = render_template('round', numbers=numbers)
    #session.attributes['numbers'] = numbers[::-1]  # reverse

    return next_round()


@ask.intent("AnswerIntent", convert={'first': str})
def answer(first):
    #Welcome to Virtual Interview System. I am here to give you a complete interview experience. Before we start, could we introduce each other. I am Alexa. Can I have your name?

    # winning_numbers = session.attributes['numbers']
    # if [first, second, third] == winning_numbers:
    #     msg = render_template('win')
    #
    # else:
    #     msg = render_template('lose')
    print(first)
    return statement(first)


if __name__ == '__main__':

    app.run(debug=True)