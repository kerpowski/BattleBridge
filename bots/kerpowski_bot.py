# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 16:01:04 2014

@author: jperkowski
"""

from interface import *
import random
import copy
from game import Match
from utilities import BiddingUtilities
from collections import defaultdict

class Kerpowski(Bot):
    
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
        Kerpowski._debugPrint("inside start")        
        Kerpowski._debugPrint(', '.join(map(lambda x: str(x), cards)))
        self.cards = cards
        
        self.suitLengths = defaultdict(int, {y:len([x for x in cards if x.suit == y]) for y in SUITS}) 
        self.handValue = self._countHCP(self.cards)
        
        Kerpowski._debugPrint(self.suitLengths)
        Kerpowski._debugPrint("HCP Value: " + str(self.handValue))
    
    def play_card(self, playedCards, dummyHand):
        """Invoked when the bot has an opportunity to play a card"""
        chosenCard = max(self.cards, key=lambda x: x.value)
        
        if(len(playedCards) > 0):      
            ledSuitCards = [x for x in self.cards if x.suit == playedCards[0].suit]
            trumpCards = [x for x in self.cards if x.suit == self.winningBid.bidSuit]
            nonTrumpCards = [x for x in self.cards if x.suit != self.winningBid.bidSuit]
            
            topCard = Match._winning_card(playedCards, self.winningBid.bidSuit)
                  
            if len(ledSuitCards) > 0:
                if len(playedCards) >= 2:
                    if playedCards.index(topCard) == (len(playedCards) - 2):
                        # Don't overthrow our partner
                        chosenCard = min(ledSuitCards, key=lambda x: x.value)
                    else:
                        # If we're not winning try to take it
                        chosenCard = max(ledSuitCards, key=lambda x: x.value)
            else:
                if playedCards.index(topCard) == (len(playedCards) - 2):
                    # Don't trump in on our partner if he's winning
                    if len(nonTrumpCards) > 0:
                        chosenCard = min(nonTrumpCards, key=lambda x: x.value)
                else:
                    # Trump in if he isn't
                    if len(trumpCards) > 0:
                        chosenCard = min(trumpCards, key=lambda x: x.value)
                    
        self.cards.remove(chosenCard)
        return chosenCard 
    
    def notify_played_card(self, actor, card):
        """Invoked for each bot after a card is played"""
        pass

    def bid(self, currentBids):
        """Invoked for each bot when it has an option of bidding."""  
        highestCurrentBid = BiddingUtilities.highest_current_bid(currentBids)
        
        potentialBid = Bid(self.identifier, None, None, 'pass')
        if self.handValue >= 10 and not(any(filter(lambda x: x.bidType != 'pass', currentBids))):
            longestSuit = max(self.suitLengths.items(), key=lambda x: x[1])[0]
            longestSuit = 'nt'            
            return Bid(self.identifier, 1, longestSuit, 'bid')

        if self.handValue >= 11 and not BiddingUtilities.has_partnership_bid(currentBids):            
            longestSuit = max(self.suitLengths.items(), key=lambda x: x[1])[0]
            longestSuit = 'nt'
            potentialBid = Bid(
                self.identifier, 
                BiddingUtilities.next_legal_bid(highestCurrentBid, longestSuit), 
                longestSuit, 
                'bid')
        
        if len(currentBids) > 2 and currentBids[-2].bidValue is not None and currentBids[-2].bidValue < 2:
            if self.handValue > 6 and currentBids[-2].bidSuit is not None and self.suitLengths[currentBids[-2].bidSuit] > 2:
                potentialBid = Bid(
                    self.identifier, 
                    BiddingUtilities.next_legal_bid(highestCurrentBid, currentBids[-2].bidSuit), 
                    currentBids[-2].bidSuit, 
                    'bid')
                
        return potentialBid

    def notify_bid(self, identifier, bid):
        """Invoked for each bot after a bid.  Currently not implemented"""
        pass

    def notify_end_bidding(self, declarerID, winningBid, biddingSequence):
        """Invoked for each bot after a bid"""
        self.winningBid = winningBid
        pass
    
    def notify_end(self):
        """Invoked for each bot after a match is finished; for debugging."""
        pass
    
    def score_hand(self, cards):
        return self._countHCP(cards)
        
    @staticmethod
    def _cardHCPValue(card):
        return max(RANKS.index(card.value) - 8, 0)
    
    def _countHCP(self, cards):
        return sum(map(lambda x: Kerpowski._cardHCPValue(x), cards))
        
        
    
def make_bot(identifier, partnerID):
    return Kerpowski(identifier, partnerID)