from loadMFCC import loadUser, loadReferences
import matplotlib.pyplot as plt
import pandas as pd,numpy as np
from calculateThreshold import calculateThreshold
import timeit


types = [
    'M',
    'F',
    'C'
]

sources = [
    'C',
    'M',
    'W'
]

# loading reference MFCCs and user MFCCs
print("reading files...")
references = loadReferences('reference')
users = loadUser('users')
print("loaded {} users!".format(len(users)))
# for all references set the test reference to utterence number 123
print("setting test utterences for references...")
for reference in references:
    reference.setTestUtterence()


# for all users set the test reference to utterence number 123 and calculate the reference user
print("calculating references for users...")
for user in users:
    user.setTestUtterence()
    user.calculateReference(references)

#calculate thresholds of pairs
print("calculating thresholds...")
thresholds = calculateThreshold(users,references)

# calculate the judgements for a set of users
def calculateJudgements(users, references,words=122,types=3,labels=5 ,print_results=False):
    judgements = np.zeros((types,words,labels),dtype=int)
    for i,user in enumerate(users):
        start = timeit.default_timer()
        print('calculating judgement for user: {}, group: {}, student: {}, type: {}, age: {}, source: {}'.format(i+1,user.group, user.student, user.Type, user.age, user.source),end=" ")
        userJudgements = user.getJudgements(references,thresholds)
        stop = timeit.default_timer()
        Sum = np.sum(userJudgements,axis=0)
        print("correct = {} , wrong = {}".format(Sum[3],Sum[4]),end=" ")
        print("calculated in: ", stop-start)
        judgements[user.reference] += userJudgements
    total = [[0,0],[0,0],[0,0]]
    totalCorrect = 0
    totalWrong = 0
    for i,Type in enumerate(judgements):
        for word in Type:
            total[i][0] += word[3]
            total[i][1] += word[4]
        totalCorrect += total[i][0]
        totalWrong += total[i][1]
    totalUtterences = totalCorrect+totalWrong
    totalMale = total[0][0]+total[0][1]
    totalFemale = total[1][0]+total[1][1]
    totalChild = total[2][0]+total[2][1]
    if print_results:
        print("male: correct = {}, wrong = {}, total = {}, correct percentage = {:.2f}%, wrong percentage = {:.2f}%".format(total[0][0],total[0][1],total[0][0]+total[0][1],total[0][0]*100/totalMale,total[0][1]*100/totalMale))
        print("female: correct = {}, wrong = {}, total = {}, correct percentage = {:.2f}%, wrong percentage = {:.2f}%".format(total[1][0],total[1][1],total[1][0]+total[1][1],total[1][0]*100/totalFemale,total[1][1]*100/totalFemale))
        print("child: correct = {}, wrong = {}, total = {}, correct percentage = {:.2f}%, wrong percentage = {:.2f}%".format(total[2][0],total[2][1],total[2][0]+total[2][1],total[2][0]*100/totalChild,total[2][1]*100/totalChild))


        print('correct',totalCorrect, totalCorrect*100/totalUtterences,"%")
        print('wrong',totalWrong, totalWrong*100/totalUtterences,"%")

        csvfile = "judgements"
        pd.DataFrame(judgements[0,:,:]).to_csv(csvfile+"_male.csv", index=False, header=["other","word2","word1","correct","wrong"])
        pd.DataFrame(judgements[1,:,:]).to_csv(csvfile+"_female.csv", index=False, header=["other","word2","word1","correct","wrong"])
        pd.DataFrame(judgements[2,:,:]).to_csv(csvfile+"_child.csv", index=False, header=["other","word2","word1","correct","wrong"])
    return judgements
print("calculating judgements...")
judgements = calculateJudgements(users, references,print_results=True)

def drawMismatches(users,numberOfMismatches=5, plot_results=False,save_results=False):  
    plt.rcParams["figure.autolayout"] = True
    for user in users:
        name = "G{}S{}{}{}{}".format(user.group,user.student,types[user.Type],user.age,sources[user.source])
        rows = int(np.sqrt(numberOfMismatches))
        columns = int(np.round(numberOfMismatches/rows+0.5))
        j = 0
        for i,utterence in enumerate(user.utterences):
            _, _, distances = utterence.reconstruct(references[user.reference].utterences[i])
            if distances is not None and not user.utterences[i].correct:
                utterenceDetails = "P{}W{}".format(utterence.pair,utterence.word)
                plt.xlabel("frame")
                plt.ylabel("mismatch")
                plt.subplot(rows,columns,j+1,title=name+utterenceDetails)
                plt.plot(distances)
                j += 1
            if j == numberOfMismatches:
                break
        if save_results:
            print("saving figure:", name)
            plt.savefig("plots/"+name+".png")
        if plot_results:
            plt.show(block=False)

drawMismatches(users,numberOfMismatches=11, plot_results=False,save_results=True)