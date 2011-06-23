'''
Created on Jun 22, 2011

@author: kykamath
'''
class Settings(dict):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value