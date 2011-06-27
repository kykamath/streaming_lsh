'''
Created on Jun 22, 2011

@author: kykamath
'''
class Settings(dict):
    '''
    This class was obtained from Jeff McGee.
    https://github.com/jeffamcgee
    '''
    def __getattr__(self, name): return self[name]
    def __setattr__(self, name, value): self[name] = value
        
class GeneralMethods:
    callMethodEveryIntervalVariable=None
    @staticmethod
    def callMethodEveryInterval(method, interval, currentTime, **kwargs):
        if GeneralMethods.callMethodEveryIntervalVariable==None: GeneralMethods.callMethodEveryIntervalVariable=currentTime
        if currentTime-GeneralMethods.callMethodEveryIntervalVariable>=interval:
            method(**kwargs)
            GeneralMethods.callMethodEveryIntervalVariable=currentTime
            
class TwoWayDict:
    MAP_FORWARD = 1
    MAP_REVERSE = -1
    def __init__(self):
        self.data = {TwoWayDict.MAP_FORWARD: {}, TwoWayDict.MAP_REVERSE: {}}
    def set(self, mappingDirection, key, value): 
        if mappingDirection not in [TwoWayDict.MAP_FORWARD, TwoWayDict.MAP_REVERSE]: raise KeyError('Incorrect mapping direction.')
        self.data[mappingDirection][key]=value
        if mappingDirection==TwoWayDict.MAP_FORWARD: self.data[TwoWayDict.MAP_REVERSE][value]=key
        else: self.data[TwoWayDict.MAP_FORWARD][value]=key
    def get(self, mappingDirection, key): return self.data[mappingDirection][key]