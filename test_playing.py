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
from interface import Card
from game import Match

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
                                    
                                    
if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs'], exit=False)
    