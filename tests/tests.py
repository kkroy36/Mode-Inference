import sys
import unittest

sys.path.append('./')
from inferModes import *

class mode_inference_tests(unittest.TestCase):

    def test_inspect_instance_syntax(self):
        """
        tests:
              inspect_instance_syntax
        
        Raises nothing if the example passes, otherwise raises an exception.
        """

        # The following cases should raise exceptions.
        with self.assertRaises(Exception):
            inspect_instance_syntax('smokes).')
        with self.assertRaises(Exception):
            inspect_instance_syntax(')*#c.')
        with self.assertRaises(Exception):
            inspect_instance_syntax('(D*ccc!.')
        with self.assertRaises(Exception):
            inspect_instance_syntax('smokes(asdf)')
        with self.assertRaises(Exception):
            inspect_instance_syntax('ccccc)(.')
        with self.assertRaises(Exception):
            inspect_instance_syntax(['smokes(Ron).'])
        with self.assertRaises(Exception):
            inspect_instance_syntax(1)
        with self.assertRaises(Exception):
            inspect_instance_syntax('1a1(  3  , 83     , 18A).')
        with self.assertRaises(Exception):
            inspect_instance_syntax('fr ( harry , ron , herm ) .')

        # The following cases should return the default type (None).
        self.assertEqual(None, inspect_instance_syntax('smokes(Ron).'))
        self.assertEqual(None, inspect_instance_syntax('father(jamespotter, harrypotter).'))
        self.assertEqual(None, inspect_instance_syntax('friends(harry, ron, hermione).'))
        self.assertEqual(None, inspect_instance_syntax('1(2,3,4).'))
        self.assertEqual(None, inspect_instance_syntax('1(2,3,4,5,6).'))
        self.assertEqual(None, inspect_instance_syntax('1a1(383,A83, 918B).'))
        self.assertEqual(None, inspect_instance_syntax('1a1(383,       A83, 918B).'))
        self.assertEqual(None, inspect_instance_syntax('1a1(383,  A83,     918B).'))
    
    def test_parse(self):
        """
        tests:
              InferenceUtils.parse

        Definitions also calls inspect_instance_syntax, improper format raises an exception.
        """
        self.assertEqual(InferenceUtils.parse('father(harrypotter,jamespotter).'), \
                         ['father', ['harrypotter', 'jamespotter']])
        self.assertEqual(InferenceUtils.parse('father(jamespotter, harrypotter).'), \
                         ['father', ['jamespotter', 'harrypotter']])
        self.assertEqual(InferenceUtils.parse('smokes(bob).'), \
                         ['smokes', ['bob']])

if __name__ == '__main__':
    unittest.main()
