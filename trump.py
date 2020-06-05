import numpy as np
import random

class Card:
    def card_set(self):
        self.heart = np.arange(1, 14)
        self.clover = np.arange(1, 14)
        self.spade = np.arange(1, 14)
        self.ace = np.arange(1, 14)        

        joker=[1,2]
    def card_shuffle(self):
        np.random.shuffle(self.heart)
        np.random.shuffle(self.clover)
        np.random.shuffle(self.spade)
        np.random.shuffle(self.ace)
    def card_get(self, num):
        card_list = []
        while True:
            select = random.randint(1, 5)
            if select == 1 and self.heart.size != 0:
                card_list.append("heart_"+str(self.heart[0]))
                self.heart=np.delete(self.heart, 0)
            elif select == 2 and self.clover.size != 0:
                card_list.append("clover_"+str(self.clover[0]))
                self.clover=np.delete(self.clover, 0)
            elif select == 3 and self.spade.size != 0:
                card_list.append("spade_"+str(self.spade[0]))
                self.spade=np.delete(self.spade, 0)
            elif self.ace.size != 0:
                card_list.append("ace_"+str(self.ace[0]))
                self.ace = np.delete(self.ace, 0)
            if len(card_list) == num:
                break
        return card_list
            
        
        



            
    
    







