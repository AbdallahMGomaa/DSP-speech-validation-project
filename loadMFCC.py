from os import listdir
from os.path import isfile, join
import scipy.io
from Users import User
from Utterence import Utterence

types = {
    'M':0,
    'F':1,
    'C':2
}
sources = {
    'C':0,
    'M':1,
    'W':2
}

def parseFilename(name):
    tmp = ""
    i = 1
    while name[i].isdigit():
        tmp += name[i]
        i += 1
    group = int(tmp)
    i += 1
    tmp = ""
    while name[i].isdigit():
        tmp += name[i]
        i += 1
    student = int(tmp)

    Type = types[name[i]]
    i += 1
    tmp = ""
    while name[i].isdigit():
        tmp += name[i]
        i += 1
    age = int(tmp)
    source = sources[name[i]]
    i += 2
    tmp = ""
    while name[i].isdigit():
        tmp += name[i]
        i += 1
    pair = int(tmp)
    word = int(name[i+1])
    return {'group':group,'student':student,'type':Type,'age':age,'source':source,'pair':pair,'word':word}



def loadUser(path):
    files = [(f,scipy.io.loadmat(join(path,f))['featuresMatrix']) for f in listdir(path) if isfile(join(path,f))]
    userId = 0
    utterenceData = parseFilename(files[0][0])
    firstId = utterenceData['age']+ utterenceData['type']*100+utterenceData['student']*1000+utterenceData['group']*10000
    users = []
    user = User(utterenceData['group'],utterenceData['student'],utterenceData['type'],utterenceData['age'],utterenceData['source'])
    users.append(user)
    for f,MFCC in files:
        utterenceData = parseFilename(f)
        if utterenceData['age']+ utterenceData['type']*100+utterenceData['student']*1000+utterenceData['group']*10000 != firstId:
            userId += 1
            firstId = utterenceData['age']+ utterenceData['type']*100+utterenceData['student']*1000+utterenceData['group']*10000
            user = User(utterenceData['group'],utterenceData['student'],utterenceData['type'],utterenceData['age'],utterenceData['source'])
            users.append(user)
        utterence = Utterence(utterenceData['pair'],utterenceData['word'],MFCC)
        users[userId].utterences.append(utterence)
    return users

def loadReferences(path):
    reference_male = loadUser(join(path,'male'))[0]
    reference_female = loadUser(join(path,'female'))[0]
    reference_child = loadUser(join(path,'child'))[0]
    references = [
        reference_male, 
        reference_female,
        reference_child   
    ]
    return references
