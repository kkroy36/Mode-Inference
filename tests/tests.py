import sys
import unittest
# These first two lines cannot change, not only are they necessary, they are part of a unittest.

sys.path.append('./')
from inferModes import *

class mode_inference_tests(unittest.TestCase):

    def test_inspect_instance_syntax(self):
        """
        tests:
              inspect_instance_syntax
        
        Raises nothing if the example passes, otherwise raises an exception.
        """

        i = InferenceUtils()
        
        # The following cases should raise exceptions.
        with self.assertRaises(Exception):
            i.inspect_instance_syntax('smokes).')
        with self.assertRaises(Exception):
            i.inspect_instance_syntax(')*#c.')
        with self.assertRaises(Exception):
            i.inspect_instance_syntax('(D*ccc!.')
        with self.assertRaises(Exception):
            i.inspect_instance_syntax('smokes(asdf)')
        with self.assertRaises(Exception):
            i.inspect_instance_syntax('ccccc)(.')
        with self.assertRaises(Exception):
            i.inspect_instance_syntax(['smokes(Ron).'])
        with self.assertRaises(Exception):
            i.inspect_instance_syntax(1)
        with self.assertRaises(Exception):
            i.inspect_instance_syntax('1a1(  3  , 83     , 18A).')
        with self.assertRaises(Exception):
            i.inspect_instance_syntax('fr ( harry , ron , herm ) .')

        # The following cases should return the default type (None).
        self.assertEqual(None, i.inspect_instance_syntax('smokes(Ron).'))
        self.assertEqual(None, i.inspect_instance_syntax('father(jamespotter, harrypotter).'))
        self.assertEqual(None, i.inspect_instance_syntax('friends(harry, ron, hermione).'))
        self.assertEqual(None, i.inspect_instance_syntax('1(2,3,4).'))
        self.assertEqual(None, i.inspect_instance_syntax('1(2,3,4,5,6).'))
        self.assertEqual(None, i.inspect_instance_syntax('1a1(383,A83, 918B).'))
        self.assertEqual(None, i.inspect_instance_syntax('1a1(383,       A83, 918B).'))
        self.assertEqual(None, i.inspect_instance_syntax('1a1(383,  A83,     918B).'))

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
        
    def test_parse(self):
        """
        tests:
              InferenceUtils.parse
        alsotests:
              InferenceUtils.inspect_instance_syntax

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
        
    def test_ground_predicate_strings_to_ground_predicate_lists(self):
        """
        tests:
              InferenceUtils.ground_predicate_strings_to_ground_predicate_lists
        alsotests:
              InferenceUtils.parse, InferenceUtils.inspect_instance_syntax

        Returns the result of InferenceUtils.parse mapped to a list of strings.
        """

        i = InferenceUtils()

        # The following tests should work properly.
        self.assertEqual(i.ground_predicate_strings_to_ground_predicate_lists(\
                        ['f(a1,a2).', 'f(a2,a3).']), [['f', ['a1', 'a2']], ['f', ['a2', 'a3']]])
        self.assertEqual(i.ground_predicate_strings_to_ground_predicate_lists(\
                        ['1(2).']), [['1', ['2']]])
        self.assertEqual(i.ground_predicate_strings_to_ground_predicate_lists(\
                        ['1a(2b).', 'b3(Bf1, f3d, 381c).']), [['1a', ['2b']], ['b3', ['Bf1', 'f3d', '381c']]])

        # The following tests should fail.
        with self.assertRaises(Exception):
            i.ground_predicate_strings_to_ground_predicate_lists(['38'])
        with self.assertRaises(Exception):
            i.ground_predicate_strings_to_ground_predicate_lists(['f(a1,a2).', 'f(a2,a3)'])
        with self.assertRaises(Exception):
            i.ground_predicate_strings_to_ground_predicate_lists(['f{a1}.', 'g(83, 381).'])
        with self.assertRaises(Exception):
            i.ground_predicate_strings_to_ground_predicate_lists(['g(ga,      bg , 38).'])

    def test_sort_keys(self):
        """
        tests:
              InferenceUtils.sort_keys
        """
        pos = InferenceUtils.ground_predicate_strings_to_ground_predicate_lists(\
                            ['f(a1, a2).', 'f(a1, a3).'])
        neg = InferenceUtils.ground_predicate_strings_to_ground_predicate_lists(\
                            ['f(a2, a1).', 'f(a3, a1).'])
        fac = InferenceUtils.ground_predicate_strings_to_ground_predicate_lists(\
                            ['b(a1).', 'b(a2).', 'b(a3).', 'b(a4).', 'b(a3).'])
        hI, bI = InferenceUtils.sort_keys(pos, neg, fac)
        
        self.assertEqual(hI['b'], 0)
        self.assertEqual(hI['f'], 1)
        self.assertEqual(bI['a1'], 0)
        self.assertEqual(bI['a2'], 2)
        self.assertEqual(bI['a3'], 1)
        self.assertEqual(bI['a4'], 3)

    def test_compress_clauses(self):
        """
        tests:
              InferenceResults.compress_ground_predicates
        """
        i = InferenceUtils()
        
        pos = i.ground_predicate_strings_to_ground_predicate_lists(\
                            ['f(a1, a2).', 'f(a1, a3).'])
        neg = i.ground_predicate_strings_to_ground_predicate_lists(\
                            ['f(a2, a1).', 'f(a3, a1).'])
        fac = i.ground_predicate_strings_to_ground_predicate_lists(\
                            ['b(a1).', 'b(a2).', 'b(a3).', 'b(a4).', 'b(a3).'])
        hI, bI = i.sort_keys(pos, neg, fac)
        pos, neg, fac = compress_clauses(pos, neg, fac)

        self.assertEqual(pos, ['1,0,2', '1,0,1'])
        self.assertEqual(neg, ['1,2,0', '1,1,0'])
        self.assertEqual(fac, ['0,0', '0,2', '0,1', '0,3', '0,1'])
        
if __name__ == '__main__':
    unittest.main()
