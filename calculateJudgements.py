from loadMFCC import loadUser, loadReferences
import matplotlib.pyplot as plt
import pandas as pd,numpy as np
from calculateThreshold import calculateThreshold
import timeit
from featureScale import scale
from os.path import exists

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


# calculate the judgements for a set of users
def calculateJudgement(users, references,thresholds,words=122,types=3,print_results=False):
    judgements = np.zeros((types,words,5),dtype=int)
    for i,user in enumerate(users):
        start = timeit.default_timer()
        print('calculating judgement for user: {}, group: {}, student: {}, type: {}, age: {}, source: {}'.format(i+1,user.group, user.student, Types[user.Type], user.age, Sources[user.source]),end=" ")
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
        pd.DataFrame([indices,judgements[0,:,:]]).to_csv(csvfile+"_male.csv", index=False, header=["word","other","word2","word1","correct","wrong"], encoding="utf-8-sig")
        pd.DataFrame([indices,judgements[1,:,:]]).to_csv(csvfile+"_female.csv", index=False, header=["word","other","word2","word1","correct","wrong"], encoding="utf-8-sig")
        pd.DataFrame([indices,judgements[2,:,:]]).to_csv(csvfile+"_child.csv", index=False, header=["word","other","word2","word1","correct","wrong"], encoding="utf-8-sig")
    return judgements

def drawMismatches(users,numberOfMismatches=5, plot_results=False,save_results=False,print_judgements=False):  
    plt.rcParams["figure.autolayout"] = True
    for user in users:
        name = "G{}S{}{}{}{}".format(user.group,user.student,Types[user.Type],user.age,Sources[user.source])
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
        if print_judgements:
            csvfile = name+".csv"
            pd.DataFrame([indices,user.judgements]).to_csv("judgements/"+csvfile, index=False, header=["word","other","word2","word1","correct","wrong"], encoding="utf-8-sig")
        
if __name__=="__main__":
    # loading reference MFCCs and user MFCCs
    print("reading files...")
    references = loadReferences('reference')
    users = loadUser('users')
    print("loaded {} users!".format(len(users)))

    # scaling input data
    print("scaling input data...")
    users,references = scale(users,references)

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
    if exists("thresholds.csv"):
        print("loading thresholds...")
        thresholds = pd.read_csv("thresholds.csv",header=None).to_numpy()
    else:
        print("calculating thresholds...")
        nums = set(np.random.randint(low=0, high=len(users), size=150)) #generate some more for the duplicates
        nums = list(nums)[:20]
        thresholdUsers = np.take(users,nums,axis=0)
        thresholds = calculateThreshold(thresholdUsers,references)
        pd.DataFrame(thresholds).to_csv('thresholds.csv', index=False, header=False)
    print("calculating judgements...")

    start = timeit.default_timer()
    judgements = calculateJudgement(users, references,print_results=True)
    stop = timeit.default_timer()
    print("total time for judgement: ", stop-start)

    drawMismatches(users,numberOfMismatches=11, plot_results=False,save_results=True,print_judgements=True)