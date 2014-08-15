# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 00:47:20 2014

@author: jperkowski
"""
from enum import Enum
import pandas as pd
import os


class Log:
    def __init__(self, fileName):
        self.fileName = fileName
        self.verbose = False
        self._eventList = []
    
    def _logEvent(self, severity, logString):
        logEvent = {'severity':severity, 'message':logString}
        self._eventList.append(logEvent)        
        
    def warn(self, *args):
        logString = "Warning: " + self._format(*args)
        print(logString)
        self._logEvent('warning', logString)
                
    def event(self, *args):
        if self.verbose:
            logString = self._format(*args)
            print(logString)
            self._logEvent('info', logString)

    def summary(self, *args):
        logString = self._format(*args)
        print(logString)
        self._logEvent('summary', logString)

    def dump_log(self, fileName = None):
        if fileName == None:
            fileName = self.fileName
            
        if fileName is not None:
            logFrame = pd.DataFrame(self._eventList)
            logFrame.to_csv(fileName, index=False)
        
        self._eventList = []

              
    def _format(self, *args):
        parts = []
        for arg in args:
            if isinstance(arg, Enum):
                parts.append(arg.name.capitalize())
            else:
                parts.append(str(arg))
        return " ".join(parts)
    
log = Log('./logs/event_log.csv')
log.verbose = False


class GameStatsLog:
    def __init__(self, fileName):
        self.fileName = fileName
        self._gameList = []
        
    def log(self, declarerID, winningBid, takenTricks, players):
        gameResults = {'declarerID':declarerID, 
            'bid_suit':winningBid.bidSuit, 
            'bid_value':winningBid.bidValue, 
            'bid_type': winningBid.bidType, 
            'player_0_points':players[0].score_hand(),
            'player_1_points':players[1].score_hand(),
            'player_2_points':players[2].score_hand(),
            'player_3_points':players[3].score_hand(),
            'player_0_tricks':takenTricks[0],
            'player_1_tricks':takenTricks[1],
            'player_2_tricks':takenTricks[2],
            'player_3_tricks':takenTricks[3]}
            
        self._gameList.append(gameResults)
        
    def dump_log(self, fileName = None):
        if fileName == None:
            fileName = self.fileName
            
        if fileName is not None:
            logFrame = pd.DataFrame(self._gameList)
            logFrame.to_csv(fileName, index=False)
        
        self._gameList = []
        
        
gameStatsLog = GameStatsLog('./logs/game_log.csv')

class MatchStatsLog:
    def __init__(self, fileName):
        self.fileName = fileName
        self._matchList = []
        
    def log(self, scores):
        matchResults = {
            'team_0_score': scores[0],
            'team_1_score': scores[1]}
        
        self._matchList.append(matchResults)
        
    def dump_log(self, fileName = None):
        if fileName == None:
            fileName = self.fileName
            
        if fileName is not None:
            logFrame = pd.DataFrame(self._matchList)
            logFrame.to_csv(fileName, index=False)
        
        self._matchList = []  

matchStatsLog = MatchStatsLog('./logs/match_log.csv')