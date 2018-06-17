from tkinter import *
import random
import tkinter.font as tkFont
import json
import codecs
import configparser
from functools import partial

LIMIT = 3


class App:
    def __init__(self, window):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')

        self.data_filename = cfg.get('path', 'filename')

        self.questions = json.load(codecs.open(self.data_filename, 'r', 'utf-8'))

        self.window = window
        self.cur = {}

        ft = tkFont.Font(family='Fixdsys', size=14, weight=tkFont.BOLD)

        question = Label(window, text="question..", font=ft)
        self.A = Button(window, text='A..', font=ft)
        self.B = Button(window, text='B..', font=ft)
        self.C = Button(window, text='C..', font=ft)
        self.D = Button(window, text="D..", font=ft)
        self.E = Button(window, text="E..", font=ft)

        buttons = [self.A, self.B, self.C, self.D, self.E]
        events = [partial(self.judge, button) for button in buttons]

        for button, event in zip(buttons, events):
            button['command'] = events

        question.pack(fill=BOTH, expand=YES)
        [button.pack(fill=BOTH, expand=YES) for button in buttons]

        [window.bind(char, event) for char, event in zip('12345', events)]

        window.title("({}/{})".format(
            len([i for i in self.questions if i.get('count') == 3]),
            len(self.questions)
        ))

        self.question = question
        self.buttons = buttons

        self.next_question()

    def complete_question(self):
        done = [button for button in self.buttons if button["background"] == "green"]
        return len(done) == len(self.cur['correct'])

    def miss(self):
        wrong = [button for button in self.buttons if button["background"] == "red"]
        return len(wrong)

    def set_color(self, widget, color="SystemButtonFace"):
        widget["background"] = color

    def set_text(self, widget, text):
        res = []
        step = 50
        for i in range(0, len(text), step):
            res.append(text[i:i + step])
        widget["text"] = '\n'.join(res)

    def save(self):
        json.dump(self.questions, codecs.open(self.questions_filename, 'w', 'utf-8'), ensure_ascii=False, indent=4)

    def set_title(self, done):
        title_string = "({done}/{total})".format(done=done, total=len(self.questions))
        self.window.title(title_string)

    def update_title(self):
        done = len([question for question in self.questions if question.get('count', 0) >= LIMIT])
        self.set_title(done)

    def mark_correct(self):
        self.cur['count'] = self.cur.get('count', 0) + 1

    def mark_wrong(self):
        self.cur['count'] = self.cur.get('count', 0) - 1

    def judge(self, button, e=None):
        text = button["text"].replace('\n', '')
        result_color = 'red'

        choose_correct = text in self.cur['correct']
        next_question_condition = choose_correct and self.complete_question()

        if next_question_condition:
            if self.miss():
                self.mark_wrong()
                self.update_title()
            else:
                self.mark_correct()
            self.save()
            self.next_question()
        else:
            if choose_correct:
                result_color = 'green'
            self.set_color(button, result_color)

    def empty_button(self):
        [self.set_text(button, '') for button in self.buttons]

    def restore_color(self):
        [self.set_color(button) for button in self.buttons]

    def next_question(self):
        optional_questions = [question for question in self.questions if question['count'] < LIMIT]

        if optional_questions:
            self.cur = random.choice(optional_questions)
            curcount = self.cur.get('count', 0)
        else:
            self.set_text(self.question, '全部题目已复习完成！')
            [self.set_text(button, '') for button in self.buttons]
            return

        options = self.cur['options'].copy()
        random.shuffle(options)

        self.empty_button()

        self.set_text(self.question, self.cur['question'] + '(已完成{}次)'.format(curcount))
        [self.set_text(button, option)
         for button, option in zip(self.buttons, options)]

        self.restore_color()


root = Tk()
root.geometry('600x400+50+50')
root.title("Pack - Example")
display = App(root)
root.mainloop()
