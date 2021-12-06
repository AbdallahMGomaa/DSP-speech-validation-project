import numpy as np
class User():
    def __init__(self, group, student,Type,age,source):
        self.group = group
        self.student = student
        self.Type = Type
        self.age = age
        self.source = source
        self.utterences = []
        self.reference = None
        self.testUtterence = None
        
    def calculateReference(self,references):
        assert self.testUtterence is not None
        d_male = self.testUtterence.distance(references[0].testUtterence)
        d_female = self.testUtterence.distance(references[1].testUtterence)
        d_child = self.testUtterence.distance(references[2].testUtterence)
        if d_male<=d_female and d_male<=d_child:
            self.reference = 0
        if d_female<=d_male and d_female<=d_child:
            self.reference = 1
        if d_child<=d_male and d_child<=d_female:
            self.reference = 2
    def setTestUtterence(self):
        if not (len(self.utterences) == 123 and self.testUtterence is None):
            print("utterences size is {} group = {} student = {} type = {} age = {}".format(len(self.utterences),self.group,self.student,self.Type,self.age))
        self.testUtterence = self.utterences[-1]
        self.utterences.pop()

    
    # def splitToPairs(self,pairs=61,words=2):
    #     self.pairs = []
    #     for i in range(pairs):
    #         wordsList = []
    #         for j in range(words):
    #             wordsList.append(self.utterences[i*words+j])
    #         self.pairs.append(wordsList)

    def calculateJudgements(self,judgements,references,threshold=np.inf):
        pairs = len(self.utterences)//2
        for i in range(pairs):
            d11 = self.utterences[i*2].distance(references[self.reference].utterences[i*2])
            d12 = self.utterences[i*2].distance(references[self.reference].utterences[i*2+1])
            d21 = self.utterences[i*2+1].distance(references[self.reference].utterences[i*2])
            d22 = self.utterences[i*2+1].distance(references[self.reference].utterences[i*2+1])
            if d11<=d12 and d11<=d21 and d11<=d22 and d11<=threshold:
                judgements[self.reference][i*2][2] += 1
                judgements[self.reference][i*2][3] += 1
                self.utterences[i*2].predicted = 1
            elif d12<=d11 and d12<=d21 and d12<=d22 and d12<=threshold:
                judgements[self.reference][i*2][1] += 1
                judgements[self.reference][i*2][4] += 1
                self.utterences[i*2].predicted = 2
            else:
                judgements[self.reference][i*2][0] += 1
                judgements[self.reference][i*2][4] += 1
                self.utterences[i*2].predicted = 0
            if d22<=d11 and d22<=d12 and d22<=d21 and d22<=threshold:
                judgements[self.reference][i*2+1][1] += 1
                judgements[self.reference][i*2+1][3] += 1
                self.utterences[i*2+1].predicted = 2
            elif d21<=d11 and d21<=d12 and d21<=d22 and d21<=threshold:
                judgements[self.reference][i*2+1][2] += 1
                judgements[self.reference][i*2+1][4] += 1
                self.utterences[i*2+1].predicted = 1
            else:
                judgements[self.reference][i*2+1][0] += 1
                judgements[self.reference][i*2+1][4] += 1
                self.utterences[i*2+1].predicted = 0