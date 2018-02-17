import sys
import unittest
# These first two lines cannot change.

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

    def test_read(self):
        """
        tests:
              InferenceUtils.read

        If the file cannot be opened, this should throw an exception.
        Otherwise it returns each line of the file as a string in a list.
        """
        # Normally, these files should not exist.
        with self.assertRaises(Exception):
            InferenceUtils.read('/file/does/not/exist.txt')
        with self.assertRaises(Exception):
            InferenceUtils.read('/neither/does/this/file.txt')

        # The first line of this file should be 'import sys'
        self.assertEqual(InferenceUtils.read('tests/tests.py')[0], 'import sys')
        self.assertEqual(InferenceUtils.read('tests/tests.py')[1], 'import unittest')
        

    def test_setup_arguments(self):
        """
        tests:
              SetupArguments

        These tests mostly focus on whether the default arguments are consistent.
        """
        test_args = SetupArguments().args

        self.assertTrue('verbose' in test_args)
        self.assertTrue('negative' in test_args)
        self.assertTrue('positive' in test_args)
        self.assertTrue('facts' in test_args)

        self.assertEqual(test_args.verbose, False)
        self.assertEqual(test_args.negative, None)
        self.assertEqual(test_args.positive, None)
        self.assertEqual(test_args.facts, None)

if __name__ == '__main__':
    unittest.main()
