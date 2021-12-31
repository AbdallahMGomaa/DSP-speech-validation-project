"""
    main function:
    - read the input MFCC files
    - split the input MFCC files into u users, p pairs, and 2 words each of
    - detect the reference for each user by using the 122th MFCC vector
    - for each word in pair in user detect whether it is pronounced correctly or not.
    - calculate the accuracy of the system
    - plot where are the differences in frames of an utterence (for n mismatched utterences)
"""
from loadMFCC import loadUser, loadReferences
import matplotlib.pyplot as plt
import pandas as pd,numpy as np
from calculateThreshold import calculateThreshold
import timeit
from featureScale import scale
from os.path import exists
from calculateJudgements import calculateJudgement




from tkinter import *

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
        self._frame.grid()

class StartPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Label(self,text="reading files...").grid(column=0,row=0)
        self.update()
        references = loadReferences('reference')
        users = loadUser('users')
        Label(self,text="loaded {} users!".format(len(users))).grid(column=0,row=0)
        Label(self,text="scaling input data...").grid(column=0,row=1)
        self.update()
        users,references = scale(users,references)
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
            Label(self,text="loading thresholds...").grid(column=0,row=4)
            self.update()
            thresholds = pd.read_csv("thresholds.csv",header=None).to_numpy()
        else:
            for user in users:
                if user.testUtterence is None:
                    user.setTestUtterence()
                if user.reference == None:
                    user.calculateReference(references)
            Label(self,text="calculating thresholds...").grid(column=0,row=4)
            self.update()
            nums = set(np.random.randint(low=0, high=len(users), size=150)) #generate some more for the duplicates
            nums = list(nums)[:20]
            thresholdUsers = np.take(users,nums,axis=0)
            thresholds = calculateThreshold(thresholdUsers,references)
            pd.DataFrame(thresholds).to_csv('thresholds.csv', index=False, header=False)
        Button(self,text="proceed",command=lambda: parent.switch_frame(SelectUser,users,references,thresholds)).grid(column=0,row=5)

class SelectUser(Frame):
    def __init__(self,parent,args):
        Frame.__init__(self, parent)
        users = args[0]
        references = args[1]
        thresholds = args[2]
        Label(self,text="select user").grid(column=0,row=0)
        self.selected = None
        for i,user in enumerate(users):
            Radiobutton(self, text=str(user),value=i,indicator=0, command=lambda: self.select(i)).grid(column=0, row=i+1)
        if self.selected is not None:
            Button(self,text="show results",command=lambda : parent.switch_frame(ShowJudgements,users[self.selected],references,thresholds)).grid(column=0,row=1)
    def select(self,val):
        self.selected = val
class ShowJudgements(Frame):
    def __init__(self,parent,args):
        Frame.__init__(self,parent)
        user = args[0]
        references = args[1]
        thresholds = args[2]
        Label(self,text="user: {}".format(user.name)).grid(column=0,row=0)
        if user.testUtterence is None:
            user.setTestUtterence()
        if user.reference == None:
            user.calculateReference(references)
        judgements = calculateJudgement(user,references,thresholds)

if __name__=="__main__":
    app = App()
    app.mainloop()