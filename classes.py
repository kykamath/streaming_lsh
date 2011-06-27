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
            
class TwoWayMap:
    MAP_FORWARD = 1
    MAP_REVERSE = -1
    def __init__(self):
        self.data = {TwoWayMap.MAP_FORWARD: {}, TwoWayMap.MAP_REVERSE: {}}
    @staticmethod
    def validMappingDirection(mappingDirection):
        if mappingDirection not in [TwoWayMap.MAP_FORWARD, TwoWayMap.MAP_REVERSE]: raise KeyError('Incorrect mapping direction.')
        return True
    def set(self, mappingDirection, key, value): 
        if TwoWayMap.validMappingDirection(mappingDirection):
            self.data[mappingDirection][key]=value
            if mappingDirection==TwoWayMap.MAP_FORWARD: self.data[TwoWayMap.MAP_REVERSE][value]=key
            else: self.data[TwoWayMap.MAP_FORWARD][value]=key
    def get(self, mappingDirection, key): 
        if TwoWayMap.validMappingDirection(mappingDirection): return self.data[mappingDirection][key]
    def getMap(self, mappingDirection):
        if TwoWayMap.validMappingDirection(mappingDirection): return self.data[mappingDirection]