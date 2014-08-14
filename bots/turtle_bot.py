# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 16:01:04 2014

@author: jperkowski
"""

from interface import *
import random
import copy

class Turtle(Bot):
    
    @staticmethod
    def _debugPrint(string):
        if False:
            print(string)
        
    def __init__(self, identifier, partnerID):
        self.identifier = identifier
        self.partnerID = partnerID
        pass
    
    def start(self, cards, ourState, theirState):
        """Invoked on each bot at the start of a new game."""
        Turtle._debugPrint("inside start")        
        Turtle._debugPrint(', '.join(map(lambda x: str(x), cards)))
        self.cards = cards
        
        self.suitLengths = {y:len([x for x in cards if x.suit == y]) for y in SUITS} 
        self.handValue = self._countHCP()
        
        Turtle._debugPrint(self.suitLengths)
        Turtle._debugPrint("HCP Value: " + str(self.handValue))
    
    def play_card(self, playedCards, dummyHand):
        """Invoked when the bot has an opportunity to play a card"""
        chosenCard = self.cards[0]
        if(len(playedCards) > 0):      
            ledSuitCards = [x for x in self.cards if x.suit == playedCards[0].suit]
            if len(ledSuitCards) > 0:
                chosenCard = ledSuitCards[0]
            
        self.cards.remove(chosenCard)
        return chosenCard 
    
    def notify_played_card(self, actor, card):
        """Invoked for each bot after a card is played"""
        pass

    def bid(self, currentBids):
        """Invoked for each bot when it has an option of bidding."""  
        if self.handValue >= 13 and not(any(filter(lambda x: x.bidType != 'pass', currentBids))):
            longestSuit = max(self.suitLengths.items(), key=lambda x: x[1])[0]
            return Bid(self.identifier, 1, longestSuit, 'bid')
        return Bid(self.identifier, None, None, 'pass')

    def notify_bid(self, identifier, bid):
        """Invoked for each bot after a bid.  Currently not implemented"""
        pass

    def notify_end_bidding(self, declarerID, winningBid, biddingSequence):
        """Invoked for each bot after a bid"""
        pass
    
    def notify_end(self):
        """Invoked for each bot after a match is finished; for debugging."""
        pass
    
    @staticmethod
    def _cardHCPValue(card):
        return max(RANKS.index(card.value) - 8, 0)
    
    def _countHCP(self):
        return sum(map(lambda x: Turtle._cardHCPValue(x), self.cards))
        
        
    
def make_bot(identifier, partnerID):
    return Turtle(identifier, partnerID)