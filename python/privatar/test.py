"""Unit test for privatar.py"""

import privatar
import unittest

import json

# check the xor code
class XORValues(unittest.TestCase):                          

    known_values = json.loads( open('test_data/xor_samples.json').read() )
    p = privatar.privatar()

    def test_xor_samples(self):                          
        """test xor using known values and check it roundtrips correctly"""
        for test in self.known_values:

            in_md5  = test['in']
            out_md5 = test['out']
            key     = test['key']

            result = self.p.xor_md5s(key, in_md5)                    
            self.assertEqual(out_md5, result)                  

            new_output = self.p.xor_md5s(key, out_md5)                    
            self.assertEqual(in_md5, new_output)                  

if __name__ == "__main__":
    unittest.main()   
