BattleBridge
=================

Rubber bridge simulator that allows you create bots and run Monte Carlo sims.

Requirements
----------------

* Python 3.4
* Pandas

Usage
-----------------

Current usage is to derive your bot class from the Bot interface in interfaces.py and instantiate it in main.py.  

Output is a cumulative score for each partnership along with a set of csv files output to the log directory with statistics on each hand.


