import tkinter as tk
import pandas as pd
import mysql.connector
import tkinter.messagebox
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from math import *
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="classmate1234",
  database="textcheck"
)

class TextCheck(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True, pady=100, padx=100)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage,Registration,PageOne,PageTwo):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=1, sticky="nsew")


        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def fuc(self,parent,controller):
        mycursor = mydb.cursor()
        username_info = self.userna.get()
        password_info = self.passwo.get()
        sql = ("SELECT password_ FROM student WHERE username_ = %s;")

        mycursor.execute(sql,[username_info])

        myresult= mycursor.fetchall()
        strresult = str(myresult)
        print(myresult)
        finalstr=strresult[3:len(strresult)-4]
        if finalstr==password_info:
            controller.show_frame(PageOne)
        else:
            tk.messagebox.showinfo('verificaion 1', 'UserName or Password Incorrect')

    def fuc2(self,parent,controller):
        mycursor = mydb.cursor()
        username_info = self.userna.get()
        password_info = self.passwo.get()
        sql = ("SELECT password_ FROM admin_ Where username_ = %s")

        mycursor.execute(sql,[username_info])

        myresult = str(mycursor.fetchall())
        finalstr = myresult[3:len(myresult)-4]
        if finalstr==password_info:
            controller.show_frame(PageTwo)
        else:
            tk.messagebox.showinfo('verificaion 1', 'UserName or Password Incorrect')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #self.config(bg="blue")
        l1 = tk.Label(self,text="Enter you user username").grid(row=1,column=1)
        l2 = tk.Label(self, text="Enter you user password").grid(row=2, column=1)
        self.userna = tk.StringVar()
        self.passwo = tk.StringVar()
        e1 = tk.Entry(self, textvariable=self.userna).grid(row=1,column=2)
        e2 = tk.Entry(self,textvariable=self.passwo,show="*").grid(row=2,column=2)
        c = tk.Checkbutton(self, text="Keep me logged in").grid(row=3, column=1,columnspan=2)
        b = tk.Button(self,text="Log in as student",command = lambda :self.fuc(parent,controller)).grid(row=4,column=1)
        b2 = tk.Button(self,text="Register",command = lambda : controller.show_frame(Registration)).grid(row=4,column=3)
        b1 = tk.Button(self,text="Log in as teacher",command = lambda : self.fuc2(parent,controller)).grid(row=4,column=2)


class PageTwo(tk.Frame):
    def fun1(self,parent,controller):
        sql1 = "select * from result"
        myresult = pd.read_sql(sql1,mydb)

        for i, rows in myresult.iterrows():
            #print(rows['cho1'],rows['cho2'],rows['cho3'],rows['cho4'])
            mystr = (rows['roll_no'])
            mystr1 = (rows['marks'])
            print(mystr)
            if(mystr==self.roll.get()):
                tk.messagebox.showinfo("Result", f"The student scored - {mystr1}% marks")

    def fun2(self,parent,controller):
        master = tk.Toplevel(self)

        l21 = tk.Label(master,text="Ans 1 - Python is a reliable language. It is also easy to implement. It is also robust. It has huge number of libraries").pack()
        l22 = tk.Label(master,text="Ans 2 - A few GUI libraries in python are Tkiner, Flexx, CEF Python, Dabo, Kivy, Pyforms, PyGObject, PyQt, PySide, PyGUI, libavg, PYGTK").pack()
        l23 = tk.Label(master,text="Ans 3 - Various fields of machine learning include Artificial Intelligence, Neural Networks, Deep Learning, Data Analysis").pack()
        master.mainloop()

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.roll = tk.IntVar()
        l1 = tk.Label(self,text="Input the roll no of the student whose record needs to be checked").grid(row=0,column=0)
        e1 = tk.Entry(self,textvariable=self.roll).grid(row=0,column=1)
        b1= tk.Button(self,text="Check result",command = lambda: self.fun1(parent,controller)).grid(row=1,column=0,pady=5)
        b2 = tk.Button(self,text="Check Answers",command = lambda: self.fun2(parent,controller)).grid(row=1,column=1,pady=5,padx=5)


class PageOne(tk.Frame):

    def fun1(self,parent,controller):
        self.ps=PorterStemmer()
        self.finaltotal=0
        self.finalsum=0
        self.ta1 = "Python is a reliable language. It is also easy to implement. It is also robust. It has huge number of libraries"
        self.ta2 = "Tkiner, Flexx, CEF Python, Dabo, Kivy, Pyforms, PyGObject, PyQt, PySide, PyGUI, libavg, PYGTK"
        self.ta3 = "Artificial Intelligence, Neural Networks, Deep Learning, Data Analysis"
        self.stop_words = set(stopwords.words('english'))
        for i in range(3):
            self.check1 = self.ta1.lower()
            self.check2 = str(self.ans1.get())
            self.check2 = self.check2.lower()
            self.sen1 = sent_tokenize(self.check1)
            self.sen2 = sent_tokenize(self.check2)
            self.punct = ['.', '!', ',', '?', ':', ";"]
            self.total_words = []
            for i in self.sen1:
                self.words = word_tokenize(i)
                for j in self.words:
                    if j not in self.stop_words and j not in self.punct:
                        self.total_words.append(j)
            self.total = len(self.total_words)
            self.sum= 0
            for S in self.sen2:

                self.count = 0
                self.maxim = 0
                self.word1 = word_tokenize(S)
                self.word1l = []
                for i in self.word1:
                    if i not in self.stop_words:
                        self.word1l.append(self.ps.stem(i))
                for S1 in self.sen1:
                    self.word2 = word_tokenize(S1)
                    self.word2l = []
                    self.count = 0
                    for i in self.word2:
                        if i not in self.stop_words:
                            self.word2l.append(self.ps.stem(i))
                    for W in self.word1l:
                        if W in self.word2l:
                            self.count += 1
                    if self.maxim < self.count:
                        self.maxim = self.count
                print(self.maxim)
                self.sum += self.maxim
            self.finalsum+=self.sum
            self.finaltotal+=self.total

        #print(self.finalsum)
        #print(self.finaltotal)
        self.per = self.finalsum/self.finaltotal
        self.per=self.per*100
        self.per=ceil(self.per)
        mycursor = mydb.cursor()
        sql = "INSERT INTO result (roll_no,marks) VALUES (%s,%s)"
        mycursor.execute(sql,(self.roll.get(),self.per))
        mydb.commit()
        tk.messagebox.showinfo("Score","You have scored - {}%".format(self.per))


    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        l1 = tk.Label(self,text="Answer the questions given below",font="12").grid(row=0,column=0)
        l2 = tk.Label(self,text="Q1 - What are the characteristics of python language?").grid(row=2,column=0)
        self.ans1 = tk.StringVar()
        self.ans2 = tk.StringVar()
        self.ans3 = tk.StringVar()
        self.roll =tk.IntVar()
        strl = "Hint - For better score -  after each point of you answer start with a new line."
        l3 = tk.Label(self,text="HINT: For each point write a separate sentence (with a full stop to indicating its end)").grid(row=1,column=0)
        e1 = tk.Entry(self,textvariable=self.ans1,width=50).grid(row=3,column=0,ipady=10)
        l3 = tk.Label(self,text="Q2 - List some of the common GUI libraries in python.").grid(row=4,column=0)
        e2 = tk.Entry(self,textvariable=self.ans2,width=50).grid(row=5,column=0,ipady=10)
        l4 = tk.Label(self,text="Q3 - What are the various fields in machine learning?").grid(row=6,column=0)
        e3 = tk.Entry(self,textvariable=self.ans3,width=50).grid(row=7,column=0,ipady=10)
        l5 = tk.Label(self,text="Input your roll number").grid(row=8,column=0)
        e4 =tk.Entry(self,textvariable=self.roll,width=50).grid(row=9,column=0,ipady=10)
        b1 = tk.Button(self,text="Submit",command = lambda:self.fun1(parent,controller)).grid(row=10,column=0)


class Registration(tk.Frame):
    def reg(self,parent,controller):
        mycursor = mydb.cursor()

        user_info = self.user.get()
        passe_info = self.passe.get()
        sql = "insert into student (username_,password_) values (%s,%s)"

        mycursor.execute(sql, (user_info,passe_info))
        mydb.commit()
        tk.messagebox.showinfo('verification reg','User successfully registered')
        controller.show_frame(PageOne)


    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.user = tk.StringVar()
        self.passe = tk.StringVar()
        ll1 = tk.Label(self, text="Select a username").grid(row=0,column=0)
        ee1 = tk.Entry(self,textvariable = self.user).grid(row=0,column=1)
        ll2 = tk.Label(self,text="Select a password").grid(row=1,column=0)
        ee1 = tk.Entry(self,textvariable = self.passe).grid(row=1,column=1)
        bb1 = tk.Button(self,text="done",command= lambda : self.reg(parent,controller)).grid(row=2,column=0,columnspan=2)

root = TextCheck()
root.mainloop()
#123
