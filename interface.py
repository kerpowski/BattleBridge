# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 22:36:12 2014

@author: kerpowski
"""
from collections import namedtuple
from enum import Enum
from functools import total_ordering
from game_logging import log

SUITS = ('c', 'd', 'h', 's')
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
BIDDING_SUITS = ('c', 'd', 'h', 's', 'nt')
BID_TYPE = ('bid', 'pass', 'double', 'redouble')   


@total_ordering
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def __str__(self):
        return self.value + self.suit
        
    def __lt__(self, other):
        return RANKS.index(self.value) < RANKS.index(other.value)
            
    def __eq__(self, other):
         return RANKS.index(self.value) == RANKS.index(other.value)
         
@total_ordering
class Bid:
    def __init__(self, playerID, bidValue, bidSuit, bidType): 
        self.bidValue = bidValue
        self.bidSuit = bidSuit
        self.bidType = bidType
        self.playerID = playerID
    
    def __lt__(self, other):
        return ((self.bidValue, BIDDING_SUITS.index(self.bidSuit)) <
            (other.bidValue, BIDDING_SUITS.index(other.bidSuit)))
            
    def __eq__(self, other):
         return ((self.bidValue, BIDDING_SUITS.index(self.bidSuit)) ==
            (other.bidValue, BIDDING_SUITS.index(other.bidSuit)))
    
    def __str__(self):
        if self.bidType == 'bid':
            return str(self.bidValue) + self.bidSuit
            
        return self.bidType

    @staticmethod
    def won_bid_delta(bidValue, bidSuit):
        if bidSuit in ['c', 'd']:
            return bidValue * 20
        if bidSuit in ['h', 's']:
            return bidValue * 30
        if bidSuit == 'nt':
            return 40 + (bidValue - 1) * 30
            
class RubberState:
    def __init__(self, aboveTheLine, belowTheLine, isVulnerable):
        self.aboveTheLine = aboveTheLine
        self.belowTheLine = belowTheLine
        self.isVulnerable = isVulnerable
        
    def __str__(self):
        retVal = "Above: " + str(self.aboveTheLine) 
        retVal += ", Below: " + str(self.belowTheLine)
        retVal += ", Vulnerable: " + str(self.isVulnerable)
        return retVal
     
    def __add__(self, other):
        return RubberState(self.aboveTheLine + other.aboveTheLine, self.belowTheLine + other.belowTheLine, self.isVulnerable)
        
class Bot:
    def start(self, cards, ourRubberState, theirRubberState):
        """Invoked on each bot at the start of a new game."""
        pass
    
    def play_card(self, playedCards, dummyHand):
        """Invoked when the bot has an opportunity to play a card"""
        pass
    
    def notify_played_card(self, actor, card):
        """Invoked for each bot after a card is played"""
        pass

    def bid(self, currentBids):
        """Invoked for each bot when it has an option of bidding."""           
        return False

    def notify_bid(self, identifier, bid):
        """Invoked for each bot after a bid.  Currently not implemented"""
        pass

    def notify_end_bidding(self, declarerID, winningBid, biddingSequence):
        """Invoked for each bot after a bid"""
        pass
    
    def notify_end(self):
        """Invoked for each bot after a match is finished; for debugging."""
        pass
    
    def score_hand(self, cards):
        return None

    