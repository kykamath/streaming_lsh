'''
Created on Jun 14, 2011

@author: kykamath
'''
import unittest
from signature import Signature

class SignatureTests(unittest.TestCase):
    
    def test_initialization(self):
        sgnt = Signature('1001011')
        self.assertEqual(sgnt.count(), 4)
        sgnt = Signature()
        self.assertEqual(sgnt.count(), 0)

if __name__ == '__main__':
    unittest.main()