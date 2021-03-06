# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 22:55:33 2014

@author: kerpowski
"""
from interface import *
import random
from collections import defaultdict
from game_logging import log, gameStatsLog, matchStatsLog
from utilities import BiddingUtilities


def _try(function, *args, **kwargs):
    try:
        return function(*args, **kwargs)
    except Exception as e:
        log.warn(traceback.format_exc())

class Deck:
    """Represents a deck of cards with automatically managed shuffling."""
    
    def __init__(self):
        self._cards = [Card(value, suit) for value in RANKS for suit in SUITS]

        random.shuffle(self._cards)

    def draw(self, count=13):
        # Skip bounds checking, because the deck isn't exhaustable.
        return [self._cards.pop() for x in range(count)]
        
    def place(self, cards):
        self._cards.extend(cards)
        random.shuffle(self._cards)
        

class Player:
    """Tracks player state"""
    
    def __init__(self, identifier, partnerID, bot):
        self.identifier = identifier
        self.name = bot.__module__
        self._bot = bot
        self.cards = None        
        self.partnerID = partnerID
     
    def __str__(self):
        return self.name + '@' + str(self.identifier)
     
    def start(self, ourState, theirState):
        self._bot.start(self.cards.copy(), ourState, theirState)
        
    def bid(self, bidList):
        return self._bot.bid(bidList)
    
    def play_card(self, playedCards, dummyHand):
        return self._bot.play_card(playedCards, dummyHand)
    
    def notify_end_bidding(self, declarerID, winningBid, biddingSequence):
        self._bot.notify_end_bidding(declarerID, winningBid, biddingSequence)

    def score_hand(self):
        return self._bot.score_hand(self.cards)

class Game:
    def __init__(self, players, states, dealerID):
        self.players = players
        self.states = states
        self.dealerID = dealerID
        
    def execute_bidding(self):
        pass
    
    def execute_playing(self):
        pass
    
    @staticmethod
    def calculate_point_delta(declarerID, winningBid, tricks, playerHands, rubberStates):
        pointDeltas = [RubberState(0, 0, False), RubberState(0, 0, False)]
        
        # First check if any player was dealt honors
        for i, p in enumerate(playerHands):
            honorsCheck = set([x.value for x in p if x.suit == winningBid.bidSuit]) & set(RANKS[8:])
            if len(honorsCheck) == 5:
                pointDeltas[i % 2].aboveTheLine += 150

            if len(honorsCheck) == 4:
                pointDeltas[i % 2].aboveTheLine += 100
            
            if winningBid.bidSuit == 'nt' and [x.value for x in p].count('A') == 4:
                pointDeltas[i % 2].aboveTheLine += 150
       
        if tricks - 6 >= winningBid.bidValue:
            pointMultiplier = 1
            # set the point multiplier and add the insult bonus
            if winningBid.bidType == 'double':                
                pointMultiplier = 2
                pointDeltas[declarerID % 2].aboveTheLine += 50
            if winningBid.bidType == 'redouble':
                pointMultiplier = 4
                pointDeltas[declarerID % 2].aboveTheLine += 100
                
            pointDeltas[declarerID % 2].belowTheLine += pointMultiplier * Bid.below_point_delta(winningBid.bidValue, winningBid.bidSuit)
            pointDeltas[declarerID % 2].aboveTheLine += pointMultiplier * Bid.above_point_delta(tricks - 6 - winningBid.bidValue, winningBid.bidSuit)
        else:
            # calculate values for getting set  
            if rubberStates[declarerID % 2].isVulnerable == True:
                 if winningBid.bidType == 'bid':
                     pointDeltas[(declarerID + 1) % 2].aboveTheLine += 100 * ((winningBid.bidValue + 6) - tricks)
                 if winningBid.bidType == 'double':
                     pointDeltas[(declarerID + 1) % 2].aboveTheLine += 200 + 300 * ((winningBid.bidValue + 6) - tricks - 1)
                 if winningBid.bidType == 'redouble':
                     pointDeltas[(declarerID + 1) % 2].aboveTheLine += 400 + 600 * ((winningBid.bidValue + 6) - tricks - 1)
            else:
                 if winningBid.bidType == 'bid':
                     pointDeltas[(declarerID + 1) % 2].aboveTheLine += 50 * ((winningBid.bidValue + 6) - tricks)
                 if winningBid.bidType == 'double':
                     doublePenalties = [100,200,200] + [300] * 10
                     pointDeltas[(declarerID + 1) % 2].aboveTheLine += sum(doublePenalties[:((winningBid.bidValue + 6) - tricks)])
                 if winningBid.bidType == 'redouble':
                     redoublePenalties = [200,400,400] + [600] * 11
                     pointDeltas[(declarerID + 1) % 2].aboveTheLine += sum(redoublePenalties[:((winningBid.bidValue + 6) - tricks)])
                 
        
        for i, delta in enumerate(pointDeltas):
            log.event("Point delta for Team " + str(i) + "... " + str(delta))       
        return pointDeltas
            
                
    def play(self):
        deck = Deck()
        for i, p in enumerate(self.players):
            p.cards = deck.draw()
            log.event('Player ' + str(p) + ' dealt: ' + ' '.join(map(lambda x: str(x), p.cards)))
            p.start(self.states[i % 2], self.states[(i+1) % 2])
            
        bidList=[]
        i = [x.identifier for x in self.players].index(self.dealerID)
        while not Match._bidding_complete(bidList):
            bid = self.players[i].bid(bidList)
            log.event('Player ' + str(self.players[i]) + ' bids: ' + str(bid))
            
            #TODO: handle illegal bids            
            if Match.legal_bid(bid, bidList, self.players[i].identifier, self.players[i].partnerID):
                bidList.append(bid)
            else:
                raise ValueError("{0} is not a valid bid after [{1}]".format(bid, ','.join((str(x) for x in bidList))))
            
            i = (i + 1) % 4
        
        declarerID = None
        winningBid = None        
        
        valueBids = [x for x in bidList if x.bidType == 'bid']
        if len(valueBids) > 0:
            winningBid = valueBids[-1]
            log.event("Final bid is: " + str(winningBid))
            partnershipBids = [x for x in valueBids if x.bidSuit == valueBids[-1].bidSuit]
            declarerID = partnershipBids[0].playerID
            log.event("Declarer is: Player " + str(self.players[declarerID]))
            
        else:
            log.event("Hand was passed out")
        
        # bidding is complete, now lets play
        if declarerID is not None:            
            for player in self.players:
                player.notify_end_bidding(declarerID, winningBid, bidList)
                
            activePlayer = (declarerID + 1) % 4
            takenTricks = defaultdict(int)
            
            for i in range(13):
                playedCards = []
                dummyHand = self.players[self.players[declarerID].partnerID].cards
                for j in range(4):
                    player = self.players[(activePlayer + j) % 4]
                    
                    #TODO: handle illegal throws
                    card = player.play_card(playedCards, dummyHand)
                    log.event("Player " + str(player) + " plays: " + str(card))
                    playedCards.append(card)
               
                trumpSuit = winningBid.bidSuit
                if winningBid.bidSuit == 'nt':
                    trumpSuit = playedCards[0].suit
                    
                winningCard = Match.winning_card(playedCards, trumpSuit)
                    
                log.event("Winning card is: " + str(winningCard))
                activePlayer = (activePlayer + playedCards.index(winningCard)) % 4
                takenTricks[activePlayer] += 1
                
            for player in self.players:
                log.event("Player " + str(player) + " took " + str(takenTricks[player.identifier]) + " tricks")
                
            declarerTricks = takenTricks[declarerID] + takenTricks[self.players[declarerID].partnerID]
            log.event("Declarer needed {0} tricks and took {1}".format(str(winningBid.bidValue + 6), declarerTricks))
            gameStatsLog.log(declarerID, winningBid, takenTricks, self.players)            
            
            pointDeltas = Game.calculate_point_delta(declarerID, 
                                                     winningBid, 
                                                     declarerTricks,
                                                     [x.cards for x in self.players], 
                                                     self.states)
            return pointDeltas
            
        
class Match:
    """A set of bots in a fixed table order playing a series of rounds."""
    def __init__(self, bot_modules):
        if len(bot_modules) != 4:
            raise ValueError("bot_modules should have 4 entries, received " + str(len(bot_modules)))
            
        self._bots = []
        self.teamStates = [RubberState(0, 0, False), RubberState(0, 0, False)]
        self.teamPoints = [0, 0]
        
        for index, module in enumerate(bot_modules):
            self._bots.append(module.make_bot(index, (index + 2 % 4)))
    
    def _update_match_points(self, result):
        newGame = False
        newRubber = False
        
        for i, x in enumerate(result):
            self.teamPoints[i] += (x.aboveTheLine + x.belowTheLine)
            self.teamStates[i] += x
            
            if self.teamStates[i].belowTheLine >= 100:
                if self.teamStates[i].isVulnerable == True:
                    newGame = True
                    if self.teamStates[(i + 1) % 2].isVulnerable == True:
                        self.teamStates[i].aboveTheLine += 500
                        self.teamPoints[i] += 500
                    else:
                        self.teamStates[i].aboveTheLine += 700
                        self.teamPoints[i] += 700
                else:
                    newRubber = True
                    self.teamStates[i].isVulnerable = True
            
        if newRubber:
            for x in self.teamStates:
                x.belowTheLine = 0
        if newGame:
            self.teamStates = [RubberState(0, 0, False), RubberState(0, 0, False)] 
            
        return (newGame, newRubber)
        
    def play(self, rubbers=1):
        self.players = [Player(i, (i+2)%4, x) for i, x in enumerate(self._bots)]        
        dealerID = self.players[0].identifier
        currentHand = 0

        for rubber in range(rubbers):
            newRubber = False 
            hands = 0
            while newRubber == False or hands < 20:
                dealerID = self.players[rubber % 4].identifier
                log.event("Start hand " + str(currentHand))
                game = Game(self.players, self.teamStates, dealerID)
                result = game.play()
                if result is not None:
                    newGame, newRubber = self._update_match_points(result)
                    for i, state in enumerate(self.teamStates):
                        log.event("Current state for Team {0}... {1}".format(i,state))
                    log.event("Hand complete, current score: {0} vs {1}".format(self.teamPoints[0], self.teamPoints[1]))
                    if newGame:
                        log.summary("Game complete, current score: {0} vs {1}".format(self.teamPoints[0], self.teamPoints[1]))
                        matchStatsLog.log(self.teamPoints)
                hands += 1                    
                currentHand += 1
            log.summary("Rubber {0} complete".format(rubber))
        gameStatsLog.dump_log()
        matchStatsLog.dump_log()
        return self.teamPoints
           
    # TODO: move to utilities or Game?
    @staticmethod
    def winning_card(cards, trump):
        trumpsPlayed = [x for x in cards if x.suit == trump]
        if len(trumpsPlayed) > 0:
            return max(trumpsPlayed)
        
        ledSuitPlayed = [x for x in cards if x.suit == cards[0].suit]
        return max(ledSuitPlayed)
    
    # TODO: move to utilities?
    @staticmethod            
    def _bidding_complete(bids):
        return len(bids) >= 4 and all(map(lambda x: x.bidType == 'pass', bids[-3:]))

    # TODO: move to utilities or Game?        
    @staticmethod
    def legal_bid(currentBid, bids, playerID, partnerID):
        lastValueBid = BiddingUtilities.highest_current_bid(bids)
        lastNonPassBid = BiddingUtilities.last_nonpass_bid(bids)

        if currentBid.bidValue is not None and (currentBid.bidValue > 7 or currentBid.bidValue < 1):
            return False
        
        if currentBid.bidType != 'bid' and (currentBid.bidValue is not None or currentBid.bidSuit is not None):
            return False
        
        if currentBid.bidType == 'bid':
            return lastValueBid is None or currentBid > lastValueBid
        
        if currentBid.bidType == 'double':
            return (lastNonPassBid is not None 
                and lastNonPassBid.playerID not in [playerID, partnerID]
                and lastNonPassBid.bidType == 'bid')
        
        if currentBid.bidType == 'redouble':
            return (lastNonPassBid is not None and 
                lastNonPassBid.bidType == 'double' and
                lastNonPassBid.playerID not in [playerID, partnerID])
                
        # pass is always legal
        return True
    
    # TODO: move to utilties
    @staticmethod
    def _legal_throw(card, playedCards, hand):
        ledSuit = None
        if len(playedCards) > 0:
            ledSuit = playedCards[0].suit
            
        if card.suit != ledSuit and len([x for x in hand if x.suit == ledSuit]) > 0:
            return False
            
        return True
    



   