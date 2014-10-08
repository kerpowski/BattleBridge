# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 16:52:58 2014

@author: kerpowski
"""

import nose
import nose.tools
from nose.tools import raises

from utilities import BiddingUtilities
import interface
from interface import Card, RubberState, Bid
from game import Match, Game

class TestPlaying(object):
    def setup(self):            
        pass
    
    def test_winning_cards(self):
        winning_cards = [
            (['4s', 'Ks', '3d', 'As'], 's', 'As'),
            (['4s', 'Ad', '3d', 'As'], 'nt', 'As'),
            (['4s', '4d', '4h', '4c'], 'nt', '4s'),
            (['4s', '4d', '4h', '4c'], 'c', '4c'),
            (['2s', '4d', '4h', '5h'], 'c', '2s')
        ]
        
        for played, trump, winner in winning_cards:
            played_cards = [Card.from_string(c) for c in played]
            nose.tools.assert_equal(Match.winning_card(played_cards, trump), 
                                    Card.from_string(winner), 
                                    'Error in playing sequence {0} with trump {1}'.format(played, trump))

    #TODO: Add doubled/redoubled tests
    #TODO: Add slam bonus calculation    
    def test_point_delta(self):
        """ 
            Currently tests combinations of:
              Made/lost contracts
              Vulnerable/not vulnerable 
              Undoubled contracts
              Honors bonus
              
            per test input should be:
              Test Name
              Declarer
              Bid
              Tricks
              Hands (only really care about honors)
              Current RubberStates (only really care about vulnerability?)
            
            per test output should be:
              List of two RubberStates that indicate the delta """
        
        scoring_tests = [
            {
             'name':'3nt made even',
             'declarer':0,            
             'bid':Bid(0, 3, 'nt', 'bid'),
             'tricks': 9,
             'hands':[[]*4],
             'vulnerability':[RubberState(0, 0, False), RubberState(0, 0, False)],
             'results':[RubberState(0, 100, False), RubberState(0, 0, False)]           
            },
            {
             'name':'NT set by 2, vulnerable',
             'declarer':0,            
             'bid':Bid(0, 3, 'nt', 'bid'),
             'tricks': 7,
             'hands':[[]*4],
             'vulnerability':[RubberState(0, 0, True), RubberState(0, 0, False)],
             'results':[RubberState(0, 0, False), RubberState(200, 0, False)]           
            },
            {
             'name':'major set by 4, vulnerable',
             'declarer':0,            
             'bid':Bid(0, 5, 's', 'bid'),
             'tricks': 7,
             'hands':[[]*4],
             'vulnerability':[RubberState(0, 0, True), RubberState(0, 0, False)],
             'results':[RubberState(0, 0, False), RubberState(400, 0, False)]           
            },
            {
             'name':'1c 3 overs, vulnerable',
             'declarer':0,            
             'bid':Bid(0, 1, 'c', 'bid'),
             'tricks': 10,
             'hands':[[]*4],
             'vulnerability':[RubberState(0, 0, True), RubberState(0, 0, False)],
             'results':[RubberState(60, 20, False), RubberState(0, 0, False)]           
            },
            {
             'name':'2s set by 1, not vulnerable, little honors',
             'declarer':0,            
             'bid':Bid(0, 2, 's', 'bid'),
             'tricks': 7,
             'hands':[['As', 'Ks', 'Qs', 'Js']] + [[]*3],
             'vulnerability':[RubberState(0, 0, False), RubberState(0, 0, False)],
             'results':[RubberState(100, 0, False), RubberState(50, 0, False)]           
            },
            {
             'name':'2s even, not vulnerable, doubled',
             'declarer':0,            
             'bid':Bid(0, 2, 's', 'double'),              
             'tricks': 8,
             'hands':[[]*4],
             'vulnerability':[RubberState(0, 0, False), RubberState(0, 0, False)],
             'results':[RubberState(50, 120, False), RubberState(0, 0, False)]           
            },
            {
             'name':'2s set by 1, not vulnerable, doubled',
             'declarer':0,            
             'bid':Bid(0, 2, 's', 'double'),              
             'tricks': 7,
             'hands':[[]*4],
             'vulnerability':[RubberState(0, 0, False), RubberState(0, 0, False)],
             'results':[RubberState(0, 0, False), RubberState(100, 0, False)]           
            },
            {
             'name':'4s set by 3, not vulnerable, doubled',
             'declarer':0,            
             'bid':Bid(0, 4, 's', 'double'),              
             'tricks': 7,
             'hands':[[]*4],
             'vulnerability':[RubberState(0, 0, False), RubberState(0, 0, False)],
             'results':[RubberState(0, 0, False), RubberState(500, 0, False)]           
            },
            {
             'name':'4s set by 4, not vulnerable, doubled',
             'declarer':0,            
             'bid':Bid(0, 4, 's', 'double'),              
             'tricks': 6,
             'hands':[[]*4],
             'vulnerability':[RubberState(0, 0, False), RubberState(0, 0, False)],
             'results':[RubberState(0, 0, False), RubberState(800, 0, False)]           
            },
            {
             'name':'4s set by 3, not vulnerable, redoubled',
             'declarer':1,            
             'bid':Bid(1, 4, 's', 'redouble'),              
             'tricks': 7,
             'hands':[[]*4],
             'vulnerability':[RubberState(0, 0, False), RubberState(0, 0, False)],
             'results':[RubberState(1000, 0, False), RubberState(0, 0, False)]           
            },
            {
             'name':'4s set by 4, not vulnerable, doubled',
             'declarer':1,            
             'bid':Bid(1, 4, 's', 'redouble'),              
             'tricks': 6,
             'hands':[[]*4],
             'vulnerability':[RubberState(0, 0, False), RubberState(0, 0, False)],
             'results':[RubberState(1600, 0, False), RubberState(0, 0, False)]           
            },
            {
             'name':'2nt even, vulnerable, redoubled',
             'declarer':1,            
             'bid':Bid(1, 2, 'nt', 'redouble'),              
             'tricks': 8,
             'hands':[[]*4],
             'vulnerability':[RubberState(0, 0, False), RubberState(0, 0, False)],
             'results':[RubberState(0, 0, False), RubberState(100, 280, False)]           
            }
        ]               
        
        for test in scoring_tests:
            hand_list = [[Card.from_string(c) for c in hand] for hand in test['hands']]            
            
            results = Game.calculate_point_delta(test['declarer'], 
                                                 test['bid'], 
                                                 test['tricks'], 
                                                 hand_list,
                                                 test['vulnerability'])
                                                 
            nose.tools.assert_list_equal(results, 
                                         test['results'], 
                                         'Test "{0}" failed'.format(test['name']))
            
                                    
if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs'], exit=False)
    
