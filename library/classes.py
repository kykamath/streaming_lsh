'''
Created on Jun 22, 2011

@author: kykamath
'''

UNIQUE_LIBRARY_KEY = '::ilab::'

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
            
#class PatternMap(dict):
#    '''
#    Accepts key with a specific pattern only
#    '''
#    def __setitem__(self, key, value): 
#        if isinstance(key, str) and key.startswith(UNIQUE_LIBRARY_KEY): super(PatternMap, self).__setitem__(key, value)
#        else: raise KeyError('Key does not match required pattern. It cannot be set directly.')
#    def setdefault(self, key, value=None):
#        if key not in self:
#            self[key] = value
#        return self[key]

#class TwoWayMap:
#    '''
#    A data strucutre that enables 2 way mapping. This is designed
#    such that it individual maps are read only, but values can be set 
#    through the methods exposed in the class
#    '''
#    MAP_FORWARD = 1
#    MAP_REVERSE = -1
#    def __init__(self): self.data = {TwoWayMap.MAP_FORWARD: PatternMap(), TwoWayMap.MAP_REVERSE: PatternMap()}
#    @staticmethod
#    def keyTransform(key): return UNIQUE_LIBRARY_KEY+str(key)
#    def set(self, mappingDirection, key, value): 
#        self.data[mappingDirection][key)]=value
#        if mappingDirection==TwoWayMap.MAP_FORWARD: self.data[TwoWayMap.MAP_REVERSE][value)]=key
#        else: self.data[TwoWayMap.MAP_FORWARD][value)]=key
#    def get(self, mappingDirection, key): return self.data[mappingDirection][key)]
#    def remove(self, mappingDirection, key):
#        value = self.data[mappingDirection][key)]
#        del self.data[mappingDirection][key)]
#        if mappingDirection==TwoWayMap.MAP_FORWARD: del self.data[TwoWayMap.MAP_REVERSE][value)]
#        else: del self.data[TwoWayMap.MAP_FORWARD][value)]
#    def getMap(self, mappingDirection): return self.data[mappingDirection]
#    def contains(self, mappingDirection, key): return  key) in self.data[mappingDirection]
#    def __len__(self): return len(self.data[TwoWayMap.MAP_FORWARD])


class TwoWayMap:
    '''
    A data strucutre that enables 2 way mapping.
    '''
    MAP_FORWARD = 1
    MAP_REVERSE = -1
    def __init__(self): self.data = {TwoWayMap.MAP_FORWARD: {}, TwoWayMap.MAP_REVERSE: {}}
    def set(self, mappingDirection, key, value): 
        self.data[mappingDirection][key]=value
        if mappingDirection==TwoWayMap.MAP_FORWARD: self.data[TwoWayMap.MAP_REVERSE][value]=key
        else: self.data[TwoWayMap.MAP_FORWARD][value]=key
    def get(self, mappingDirection, key): return self.data[mappingDirection][key]
    def remove(self, mappingDirection, key):
        value = self.data[mappingDirection][key]
        del self.data[mappingDirection][key]
        if mappingDirection==TwoWayMap.MAP_FORWARD: del self.data[TwoWayMap.MAP_REVERSE][value]
        else: del self.data[TwoWayMap.MAP_FORWARD][value]
    def getMap(self, mappingDirection): return self.data[mappingDirection]
    def contains(self, mappingDirection, key): return  key in self.data[mappingDirection]
    def __len__(self): return len(self.data[TwoWayMap.MAP_FORWARD])