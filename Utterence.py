from dtw import dtw

class Utterence:
    def __init__(self,pair,word,MFCC) -> None:
        self.pair = pair
        self.word = word
        self.MFCC = MFCC
        self.correct = None
    def distance(self,reference):
        d = dtw(reference.MFCC,self.MFCC,reconstruct=False)
        return d

    def reconstruct(self,reference):
        d,reconstructed,distances = dtw(reference.MFCC,self.MFCC,reconstruct=True)
        return d,reconstructed,distances
        