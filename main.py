# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 16:39:38 2014

@author: jperkowski
"""

from game_logging import log
import os
from game import Match
import time
import sys

def main(argv):
    d = os.path.dirname('logs')
    print(d)
    print(os.getcwd())
    if not os.path.exists(d):
        os.makedirs('logs')
        
    log.verbose = True
    
    names = [x[:-3] for x in os.listdir("bots") if x[-3:] == ".py"]
    names.remove("__init__")
    
    started = time.clock()
    
    bots = ["kerpowski_bot", "turtle_bot", "kerpowski_bot", "turtle_bot"]
    sys.path.append("bots")
    battle = Match([__import__(x) for x in bots])
    battle.play(1)
    print("")
    print("Completed in", str(int(time.clock() - started)), "seconds")

            
if __name__ == "__main__":
    sys.exit(main(sys.argv))