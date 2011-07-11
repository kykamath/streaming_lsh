'''
Created on Jun 22, 2011

@author: kykamath
'''
from datetime import timedelta, datetime
import time, random

class Settings(dict):
    '''
    Part of this class was obtained from Jeff McGee.
    https://github.com/jeffamcgee
    '''
    def __getattr__(self, name): return self[name]
    def __setattr__(self, name, value): self[name] = value
    def convertToSerializableObject(self): return Settings.getSerialzedObject(self)
    @staticmethod
    def getSerialzedObject(map):
        returnData = {}
        for k, v in map.iteritems():
            if isinstance(v, timedelta): returnData[k]=v.seconds
            elif type(v) in [int, float, str, dict, list, tuple]: returnData[k]=v
        return returnData
    
class FixedIntervalMethod:
    def __init__(self, method, interval):
        self.lastCallTime=None
        self.method=method
        self.interval=interval
    def call(self, currentTime, **kwargs):
        if self.lastCallTime==None: self.lastCallTime=currentTime
        if currentTime-self.lastCallTime>=self.interval:
            self.method(**kwargs)
            self.lastCallTime=currentTime
        
class GeneralMethods:
    @staticmethod
    def reverseDict(map): 
        dictToReturn = dict([(v,k) for k,v in map.iteritems()])
        if len(dictToReturn)!=len(map): raise Exception()
        return dictToReturn
    @staticmethod
    def getEpochFromDateTimeObject(dateTimeObject): return time.mktime(dateTimeObject.timetuple())
    @staticmethod
    def getRandomColor(): return '#'+''.join(random.choice('0123456789abcdef') for i in range(6))
    @staticmethod
    def approximateToNearest5Minutes(dateTimeObject):return datetime(dateTimeObject.year, dateTimeObject.month, dateTimeObject.day, dateTimeObject.hour, 5*(dateTimeObject.minute/5))

class TwoWayMap:
    '''
    A data strucutre that enables 2 way mapping.
    '''
    MAP_FORWARD = 1
    MAP_REVERSE = -1
    def __init__(self): self.data = {TwoWayMap.MAP_FORWARD: {}, TwoWayMap.MAP_REVERSE: {}}
    def set(self, mappingDirection, key, value): 
        if value in self.data[-1*mappingDirection]: self.remove(mappingDirection, self.data[-1*mappingDirection][value])
        if key in self.data[mappingDirection]: self.remove(mappingDirection, key)
        self.data[mappingDirection][key]=value
        self.data[-1*mappingDirection][value]=key
    def get(self, mappingDirection, key): return self.data[mappingDirection][key]
    def remove(self, mappingDirection, key):
        if key in self.data[mappingDirection]:
            value = self.data[mappingDirection][key]
            del self.data[mappingDirection][key]; del self.data[-1*mappingDirection][value]
    def getMap(self, mappingDirection): return self.data[mappingDirection]
    def contains(self, mappingDirection, key): return  key in self.data[mappingDirection]
    def __len__(self): return len(self.data[TwoWayMap.MAP_FORWARD])