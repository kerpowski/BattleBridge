# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 00:47:20 2014

@author: jperkowski
"""
from enum import Enum

class Log:
    def __init__(self):
        self.verbose = False
    
    def warn(self, *args):
        print("Warning: " + self._format(*args))

    def event(self, *args):
        if self.verbose:
            print(self._format(*args))

    def summary(self, *args):
        print(self._format(*args)) 
              
    def _format(self, *args):
        parts = []
        for arg in args:
            if isinstance(arg, Enum):
                parts.append(arg.name.capitalize())
            else:
                parts.append(str(arg))
        return " ".join(parts)
    
log = Log()
log.verbose = False