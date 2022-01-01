import numpy as np

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
        self.judgements = None
        self.isScaled = False
        
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


    def getJudgements(self,references,thresholds):
        judgements = np.zeros((len(self.utterences),5),dtype=int)
        pairs = len(self.utterences)//2
        for i in range(pairs):
            d11 = self.utterences[i*2].distance(references[self.reference].utterences[i*2])
            d12 = self.utterences[i*2].distance(references[self.reference].utterences[i*2+1])
            d21 = self.utterences[i*2+1].distance(references[self.reference].utterences[i*2])
            d22 = self.utterences[i*2+1].distance(references[self.reference].utterences[i*2+1])
            if d11<=thresholds[2*i] or d12<=thresholds[2*i]:
                if d11<=d12:
                    judgements[i*2][2] += 1
                    judgements[i*2][3] += 1
                    self.utterences[i*2].correct = True
                elif d12<=d11:
                    judgements[i*2][1] += 1
                    judgements[i*2][4] += 1
                    self.utterences[i*2].correct = False
            else:
                judgements[i*2][0] += 1
                judgements[i*2][4] += 1
                self.utterences[i*2].correct = False
            if d21<=thresholds[2*i+1] or d22<=thresholds[2*i+1]:
                if d22<=d21:
                    judgements[i*2+1][1] += 1
                    judgements[i*2+1][3] += 1
                    self.utterences[i*2+1].correct = True
                elif d21<=d22:
                    judgements[i*2+1][2] += 1
                    judgements[i*2+1][4] += 1
                    self.utterences[i*2+1].correct = False
            else:
                judgements[i*2+1][0] += 1
                judgements[i*2+1][4] += 1
                self.utterences[i*2+1].correct = False
        self.judgements = judgements
        return judgements

    def getMismatches(self,references):
        mismatches = []
        for i in range(len(self.utterences)):
            _,_,distances = self.utterences[i].reconstruct(references[self.reference].utterences[i])
            mismatches.append(distances)
        return mismatches
    def __str__(self) -> str:
        return "G{}S{}{}{}{}".format(self.group,self.student,Types[self.Type],self.age,Sources[self.source])