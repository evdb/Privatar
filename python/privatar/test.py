"""Unit test for privatar.py"""

from privatar import privatar
import unittest

import json

# check the xor code
class XORValues(unittest.TestCase):                          

    known_values = json.loads( open('test_data/xor_samples.json').read() )

    def test_xor_samples(self):                          
        """test xor using known values and check it roundtrips correctly"""
        for test in self.known_values:

            in_md5  = test['in']
            out_md5 = test['out']
            key     = test['key']

            result = privatar.xor_md5s(key, in_md5)                    
            self.assertEqual(out_md5, result)                  

            new_output = privatar.xor_md5s(key, out_md5)                    
            self.assertEqual(in_md5, new_output)

class URLCreation(unittest.TestCase):

    test_data = json.loads( open('test_data/url_creation.json').read(), encoding='ASCII' )
    _privatar = False

    def privatar(self):
        if not self._privatar:
            config = self.test_data['config']
            self._privatar = privatar( site_key=config['site_key'], shared_secret=config['shared_secret'] )
        return self._privatar
     

    def test_url_creation(self):
        """test that urls are generated as expected"""
        for test in self.test_data['tests']:
            u_args = test['args']

            # convert keys to ascii because python gets all tarty
            args = dict((k.encode('ascii'), v) for (k, v) in u_args.items())

            url = self.privatar().url( **args );
            self.assertEqual( url, test['urls']['http'] )

            secure_url = self.privatar().url( secure=True, **args );
            self.assertEqual( secure_url, test['urls']['https'] )                    

if __name__ == "__main__":
    unittest.main()   
