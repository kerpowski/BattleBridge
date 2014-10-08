import nose
import nose.tools
from nose.tools import raises

from utilities import BiddingUtilities
from interface import Bid, BIDDING_SUITS
from game import Match


class TestBidding(object):
    def setup(self):
        self.test_bid_sequences = [
            (['1s', '1c'], [True, False]),
            (['1s', '1nt', '2c', '1nt'], [True, True, True, False]),
            (['double'], [False]),
            (['1c', 'pass', 'pass', 'redouble'], [True, True, True, False]),
            (['1c', 'pass', 'double', 'redouble'], [True, True, False, True]),
            (['1c', 'double', '2c', 'redouble'], [True, True, True, False]),
            (['1c', 'double', 'redouble', 'double'], [True, True, True, False])
        ]        
        
    @raises(ValueError)
    def test_bid_parsing_low(self):    
        Bid.from_string('0s', 0)
        
    @raises(ValueError)
    def test_bid_parsing_high(self):    
        Bid.from_string('8s', 0)
        
    @raises(ValueError)
    def test_bid_parsing_novalue(self):    
        Bid.from_string('nt', 0)
        
    @raises(ValueError)
    def test_bid_parsing_invalid(self):    
        Bid.from_string('one no trump', 0)

    @raises(ValueError)    
    def test_bid_parsing_nosuit(self):    
        Bid.from_string('2', 0)

    def test_bid_parsing_valid(self):
        for i in range(1,8):
            for s in BIDDING_SUITS:
                Bid.from_string(str(i)+s, 0)
                
    def test_bid_parsing_special_bids(self):
        b = Bid.from_string('pass', 0)
        nose.tools.assert_true(b.bidType == 'pass')
        b = Bid.from_string('double', 0)
        nose.tools.assert_true(b.bidType == 'double')
        b = Bid.from_string('redouble', 0)
        nose.tools.assert_true(b.bidType == 'redouble')
        
    def test_legal_bids(self):
        for test_sequence, actual_legal in self.test_bid_sequences:
            bid_list = [Bid.from_string(b, i) for i, b in enumerate(test_sequence)]
            legal_bids = []
            for i, bid in enumerate(bid_list):
                legal_bids.append(Match.legal_bid(bid, bid_list[:i], i % 4, (i +2) % 4))
                            
            nose.tools.assert_list_equal(legal_bids, actual_legal, msg='Bid sequence {0} failed'.format(test_sequence))

if __name__ == '__main__':    
    nose.runmodule(argv=[__file__, '-vvs'], exit=False)
