from tkinter import *
import random
import tkinter.font as tkFont
import json
import codecs
import configparser


class App:
    def __init__(self, window):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')

        config_filename = cfg.get('path', 'filename')

        self.data = json.load(codecs.open(config_filename, 'r', 'utf-8'))
        self.hav_show = False

        question_ft = tkFont.Font(family='Fixdsys', size=14, weight=tkFont.BOLD)
        entry_ft = tkFont.Font(family='Fixdsys', size=20, weight=tkFont.BOLD)
        answer_ft = tkFont.Font(family='Fixdsys', size=60, weight=tkFont.BOLD)

        self.question = Label(window, text="question...", font=question_ft)
        self.entry = Entry(window, font=entry_ft)
        self.answer = Label(window, text="answer...", font=answer_ft)

        self.question.pack(side=TOP, fill=BOTH)
        self.entry.pack(ipady=10, pady=40)
        self.answer.pack(side=TOP, fill=BOTH, expand=YES)

        self.entry['justify'] = CENTER

        self.entry.bind('<Return>', self.enter)

        self.next_question()

    def set_text(self, widget, text):
        res = []
        step = 50
        for i in range(0, len(text), step):
            res.append(text[i:i + step])
        widget["text"] = '\n'.join(res)

    def enter(self, e=None):
        # 在输入框按下回车后
        if self.hav_show:  # 如果已经显示了答案
            self.next_question()
            self.entry.delete(0, END)
        else:
            self.set_text(self.answer, self.cur['answer'])
        self.hav_show = not self.hav_show

    def next_question(self):
        self.cur = random.choice(self.data)
        self.set_text(self.answer, '')
        self.set_text(self.question, self.cur['question'])


root = Tk()
root.geometry('600x400+50+50')
root.title("Pack - Example")
display = App(root)
root.mainloop()
