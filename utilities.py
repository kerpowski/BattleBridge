# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 22:41:49 2014

@author: kerpowski
"""

import interface
import itertools

class BiddingUtilities:
    @staticmethod
    def has_partnership_bid(currentBids):
        """ Helper method to determine if partnership has bid """
        partnershipBids = currentBids[len(currentBids) % 2::2]
        return any(filter(lambda x: x.bidType != 'pass', partnershipBids))
    
    @staticmethod
    def highest_current_bid(currentBids):
        return next(filter(lambda x: x.bidType == 'bid', reversed(currentBids)),None)
    
    @staticmethod
    def last_nonpass_bid(currentBids):
        return next(filter(lambda x: x.bidType != 'pass', reversed(currentBids)),None)
            
    @staticmethod
    def next_legal_bid(currentBid, suit):
        nextBidValue = 1        
        if currentBid is not None:
            nextBidValue = currentBid.bidValue
            if interface.BIDDING_SUITS.index(suit) <= interface.BIDDING_SUITS.index(currentBid.bidSuit):
                nextBidValue += 1
        return nextBidValue
    