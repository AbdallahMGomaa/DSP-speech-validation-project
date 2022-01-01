from loadMFCC import loadUser, loadReferences
import matplotlib.pyplot as plt
import pandas as pd,numpy as np
from calculateThreshold import calculateThreshold
import timeit
from featureScale import scale
from os.path import exists
from calculateJudgements import calculateJudgement,drawMismatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure
indices = pd.read_csv("words.csv",header=None, encoding="utf-8-sig").to_numpy()

Types = [
    'M',
    'F',
    'C'
]

Sources = [
    'C',
    'M',
    'W'
]

from tkinter import *
from tkinter import ttk
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=0)
# selectUserFrame = ttk.Frame(mainFrame)
# ttk.Label(selectUserFrame,text="select user").grid(column=0,row=0)
# root.update()
# for i,user in enumerate(users):
#     ttk.Button(selectUserFrame, text=str(user)).grid(column=0,row=i+1)

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Speech validation system")
        self.geometry("500x500")
        self.resizable(True,True)
        self._frame = None
        self.switch_frame(StartPage)
    def switch_frame(self, frame_class,*args):
        if len(args) == 0:
            new_frame = frame_class(self)
        else:
            new_frame = frame_class(self,args)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Label(self,text="reading files...").pack(side=TOP)
        self.update()
        references = loadReferences('reference')
        users = loadUser('users')
        Label(self,text="loaded {} users!".format(len(users))).pack(side=TOP)
        Label(self,text=" input data scaled...").pack(side=TOP)
        self.update()
        users,references = scale(users,references)
        for reference in references:
            reference.setTestUtterence()
        # Label(self,text="setting test utterences for references...").grid(column=0,row=2)
        # self.update()
        # for reference in references:
        #     reference.setTestUtterence()
        # Label(self,text="calculating references for users...").grid(column=0,row=3)
        # self.update()
        # for user in users:
        #     user.setTestUtterence()
        #     user.calculateReference(references)
        if exists("thresholds.csv"):
            Label(self,text="loaded thresholds...").pack(side=TOP)
            self.update()
            thresholds = pd.read_csv("thresholds.csv",header=None).to_numpy()
        else:
            Label(self,text="calculated thresholds...").pack(side=TOP)
            self.update()
            nums = set(np.random.randint(low=0, high=len(users), size=150)) #generate some more for the duplicates
            nums = list(nums)[:20]
            thresholdUsers = np.take(users,nums,axis=0)
            for user in thresholdUsers:
                if user.testUtterence is None:
                    user.setTestUtterence()
                if user.reference == None:
                    user.calculateReference(references)
            thresholds = calculateThreshold(thresholdUsers,references)
            pd.DataFrame(thresholds).to_csv('thresholds.csv', index=False, header=False)
        Button(self,text="proceed",command=lambda: parent.switch_frame(SelectUser,users,references,thresholds)).pack(side=TOP)

class SelectUser(Canvas):
    def __init__(self,parent,args):
        Canvas.__init__(self,parent)
        users, references, thresholds = args
        lbl = Label(self,text="select user")
        lbl.pack(side=TOP)
        Button(self,text="add user",command=lambda: parent.switch_frame(AddUser,args)).pack(side=TOP)
        scrollbar = Scrollbar(self,orient=VERTICAL,command=self.yview)
        self.selected = IntVar()
        for i,user in enumerate(users):
            btn = Radiobutton(self, text=str(user),value=i,variable=self.selected,command=lambda: lbl.config(text="user "+str(users[self.selected.get()])+" is selected"))
            self.create_window(0,i*50,window=btn,anchor="nw",height=50)
        self.configure(yscrollcommand=scrollbar.set,scrollregion=self.bbox("all"))
        scrollbar.pack(side=RIGHT, fill=Y)
        Button(self,text="proceed",command=lambda: self.select(parent,users,references,thresholds)).pack(side=TOP)
        self.pack(fill="both",expand=True,side=LEFT)
    def select(self,parent,users,references,thresholds):
        parent.switch_frame(ShowJudgements,self.selected.get(),users,references,thresholds)
class ShowJudgements(Frame):
    def __init__(self,parent,args):
        Frame.__init__(self,parent)
        selected, users, references, thresholds = args
        user = users[selected]
        Label(self,text="user: {}".format(str(user))).pack(side=TOP)
        tree = ttk.Treeview(self,columns=("word","other","word2","word1","correct","wrong"),show="headings")
        
        if user.testUtterence is None:
            user.setTestUtterence()
        if user.reference == None:
            user.calculateReference(references)
        judgements = user.getJudgements(references,thresholds)
        
        tree.column("#1", anchor=CENTER,width=60)
        tree.heading("#1", text="Word")
        tree.column("#2", anchor=CENTER,width=60)
        tree.heading("#2", text="Other")
        tree.column("#3", anchor=CENTER,width=60)
        tree.heading("#3", text="Word2")
        tree.column("#4", anchor=CENTER,width=60)
        tree.heading("#4", text="Word1")
        tree.column("#5", anchor=CENTER,width=60)
        tree.heading("#5", text="Correct")
        tree.column("#6", anchor=CENTER,width=60)
        tree.heading("#6", text="Wrong")
        for i,row in enumerate(judgements):
            val = [indices[i,0]]+row.tolist()
            tree.insert("", END, values=val)
        total = ["Total"]+np.sum(judgements,axis=0).tolist()
        tree.insert("", END, values=total)
        tree.pack(side=TOP)
        Label(self,text="accuracy = {:.2f}%".format(100*total[4]/(total[4]+total[5]))).pack(side=TOP)
        Button(self,text="show mismatches",command=lambda: parent.switch_frame(ShowMismatches,user,users,references,thresholds)).pack(side=TOP)
        Button(self,text="back",command=lambda: parent.switch_frame(SelectUser,users,references,thresholds)).pack(side=TOP)

class ShowMismatches(Canvas):
    def __init__(self,parent,args):
        Canvas.__init__(self,parent)
        user,users, references, thresholds = args
        if user.testUtterence is None:
            user.setTestUtterence()
        if user.reference == None:
            user.calculateReference(references)
        Label(self,text="user: {}".format(str(user))).pack(side=TOP)
        mismatches = user.getMismatches(references)
        lbl = Label(self,text="select mismatched word")
        scrollbar = Scrollbar(self,orient=VERTICAL,command=self.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.selected = IntVar()
        for i,_ in enumerate(mismatches):
            if not user.utterences[i].correct:
                name = "P{}W{}".format(user.utterences[i].pair,user.utterences[i].word)
                btn = Radiobutton(self, text=name,value=i,variable=self.selected,command=lambda: lbl.config(text="word "+name+" is selected"))
                self.create_window(0,i*50,window=btn,anchor="nw",height=50)
        
        self.configure(yscrollcommand=scrollbar.set,scrollregion=self.bbox("all"))
        scrollbar.pack(side=RIGHT, fill=Y)
        self.pack(fill="both",expand=True,side=LEFT)
        i = self.selected.get()
        name = "P{}W{}".format(user.utterences[i].pair,user.utterences[i].word)
        Button(self,text="proceed",command=lambda: self.select(parent,name,mismatches[self.selected.get()],user,users,references,thresholds)).pack(side=TOP)
        Button(self,text="back",command=lambda: parent.switch_frame(SelectUser,users,references,thresholds)).pack(side=TOP)
    def select(self,parent,name,mismatch,user,users,references,thresholds):
        parent.switch_frame(DisplayMismatch,name,mismatch,user,users,references,thresholds)
class DisplayMismatch(Frame):
    def __init__(self,parent,args):
        Frame.__init__(self,parent)
        Button(self,text="back",command=lambda: parent.switch_frame(SelectUser,users,references,thresholds)).pack(side=TOP)
        name,d,user,users, references, thresholds = args
        fig = Figure(figsize=(4,5),dpi=100)
        plt1 = fig.add_subplot(111)
        plt1.plot(d)
        plt1.set_title(str(user)+name)
        plt1.set_xlabel("frame")
        plt1.set_ylabel("mismatch/distance")
        canvas = FigureCanvasTkAgg(fig,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=True)
        

class AddUser(Frame):
    def __init__(self,parent,args):
        Frame.__init__(self,parent)
        users,references,thresholds = args
        

if __name__=="__main__":
    app = App()
    app.mainloop()