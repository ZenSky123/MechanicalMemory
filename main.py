from tkinter import *
import random
import tkinter.font as tkFont
import json
import codecs


class App:
    def __init__(self, window):
        self.window = window
        self.data = json.load(codecs.open('data.json', 'r', 'utf-8'))
        self.cur = {}

        ft = tkFont.Font(family='Fixdsys', size=14, weight=tkFont.BOLD)

        self.problem = Label(window, text="problem..", font=ft)
        self.A = Button(window, text='A..', command=self.chooseA, font=ft)
        self.B = Button(window, text='B..', command=self.chooseB, font=ft)
        self.C = Button(window, text='C..', command=self.chooseC, font=ft)
        self.D = Button(window, text="D..", command=self.chooseD, font=ft)
        self.E = Button(window, text="E..", command=self.chooseE, font=ft)

        self.problem.pack(fill=BOTH, expand=YES)
        self.A.pack(fill=BOTH, expand=YES)
        self.B.pack(fill=BOTH, expand=YES)
        self.C.pack(fill=BOTH, expand=YES)
        self.D.pack(fill=BOTH, expand=YES)
        self.E.pack(fill=BOTH, expand=YES)

        window.bind("1", self.chooseA)
        window.bind("2", self.chooseB)
        window.bind("3", self.chooseC)
        window.bind("4", self.chooseD)
        window.bind("5", self.chooseE)

        window.title("({}/{})".format(
            len([i for i in self.data if i.get('count') == 3]),
            len(self.data)
        ))

        self.nextProblem()

    @property
    def isDone(self):
        widgets = [self.A, self.B, self.C, self.D, self.E]
        done = [widget for widget in widgets if widget["background"] == "green"]
        return len(done) == len(self.cur['correct'])

    @property
    def haveWrong(self):
        widgets = [self.A, self.B, self.C, self.D, self.E]
        wrong = [widget for widget in widgets if widget["background"] == "red"]
        return len(wrong)

    def setColor(self, widget, color="red"):
        widget["background"] = color

    def setText(self, widget, text):
        widget["text"] = text

    def chooseA(self, event=None):
        self.judge(self.A)

    def chooseB(self, event=None):
        self.judge(self.B)

    def chooseC(self, event=None):
        self.judge(self.C)

    def chooseD(self, event=None):
        self.judge(self.D)

    def chooseE(self, event=None):
        self.judge(self.E)

    def save(self):
        json.dump(self.data, codecs.open('data.json', 'w', 'utf-8'), ensure_ascii=False, indent=4)

    def judge(self, widget):
        text = widget["text"]
        if text in self.cur['correct']:
            if self.isDone:
                if not self.haveWrong:
                    self.cur["count"] = self.cur.get("count", 0) + 1
                    self.window.title("({}/{})".format(
                        len([i for i in self.data if i.get('count') == 3]),
                        len(self.data)
                    ))
                else:
                    self.cur["count"] = self.cur.get("count", 0) - 1
                self.save()
                self.nextProblem()
            else:
                self.setColor(widget, 'green')
        else:
            self.setColor(widget)

    def nextProblem(self):
        self.cur = random.choice(self.data)
        curcount = self.cur.get('count', 0)
        while curcount >= 3:
            self.cur = random.choice(self.data)
            curcount = self.cur.get('count', 0)

        options = self.cur['options'].copy()
        if options:
            random.shuffle(options)
            options.extend(['', '', '', '', ''])
        else:
            options = ['√', '×', '', '', '']

        widgets = [self.A, self.B, self.C, self.D, self.E]
        for widget, option in zip(widgets, options):
            self.setText(widget, option)
        self.setText(self.problem, self.cur['problem'] + '(已完成{}次)'.format(curcount))

        for widget in widgets:
            widget["background"] = "SystemButtonFace"


root = Tk()
root.geometry('600x400+50+50')
root.title("Pack - Example")
display = App(root)
root.mainloop()
