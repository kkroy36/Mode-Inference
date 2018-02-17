"""inferModes.py: A prototype Python package for minimizing the size of datasets,
                  inferring datatypes, and converting them into a relational schema.

BSD 2-Clause License

Copyright (c) 2018, Alexander L. Hayes
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""



from __future__ import print_function
from collections import Counter
import argparse
import re



__author__ = "Alexander L. Hayes (@batflyer)"
__copyright__ = "Copyright 2018, Alexander L. Hayes"
__credits__ = ["Alexander L. Hayes", "Kaushik Roy", "Sriraam Natarajan"]

__license__ = "BSD 2-Clause"
__version__ = "0.1.0"
__maintainer__ = "Alexander L. Hayes (@batflyer)"
__email__ = "alexander@batflyer.net"
__status__ = "Prototype"



# A regular expression which verifies whether or not modes are formatted properly.
_instance_re = re.compile(r'[a-zA-Z0-9]*\(([a-zA-Z0-9]*,( )*)*[a-zA-Z0-9]*\)\.')



class SetupArguments:
    """
    @batflyer: I am maintaining these as classes in the event that this reaches a point where I convert it into a package.
    """

    def __init__(self, verbose=False, positive=None, negative=None, facts=None):
    
        parser = argparse.ArgumentParser(description='Minimizing positives, negatives, and facts, and performing mode inference', epilog="Copyright 2018 Alexander L. Hayes. BSD 2-Clause. A full copy of the license is available at the head of the source. The text can also be found online <https://opensource.org/licenses/BSD-2-Clause>.")
        parser.add_argument("-v", "--verbose", help="Increase verbosity to help with debugging.", default=verbose, action="store_true")
        parser.add_argument("-pos", "--positive", help="Path to positive examples.", type=str, default=positive)
        parser.add_argument("-neg", "--negative", help="Path to negative examples.", type=str, default=negative)
        parser.add_argument("-fac", "--facts", help="Path to relational facts.", type=str, default=facts)
        
        self.args = parser.parse_args()


        
class InferenceUtils:

    def __init__(self):
        pass

    @staticmethod
    def inspect_instance_syntax(example):
        """
        Uses a regular expression to check whether or not a mode is formatted correctly.
          Example:
             friends(Alice, Bob).   :::   pass
             friends(Bob, Alice).   :::   pass
             smokes(Bob).           :::   pass
        
             useStdLogicVariables   :::   fail
             friends).              :::   fail
        """
        if not _instance_re.search(example):
            raise Exception('Error when checking ground instances; incorrect syntax: ' + example)

    @staticmethod
    def parse(predicate_string):
        """
        Input a string of the format:
           'father(harrypotter,jamespotter).'
        Ensures syntax is correct, then returns a list where [0] is the name of the literal
        and [1] is a list of variables in the rule.
           ['father', ['harrypotter', 'jamespotter']]
        """
        InferenceUtils.inspect_instance_syntax(predicate_string)
        
        predicate_list = predicate_string.replace(' ', '').split(')', 1)[0].split('(')
        predicate_list[1] = predicate_list[1].split(',')
        return predicate_list

    @staticmethod
    def read(path):
        """
        Reads the data from file located at 'path', returns a list of strings where each
        string contains the information on that particular line.
        """
        try:
            with open(path) as f:
                data = f.read().splitlines()
            return data
        except:
            raise Exception('Could not open file, no such file or directory.')

    @staticmethod
    def ground_predicate_strings_to_ground_predicate_lists(list_of_strings):
        """
        Convert a list of strings into a list of lists.
        
        For example:
             ['f(a1,a2).', 'f(a2,a3).', ...] ==> [['f', ['a1', 'a2']], ['f', ['a2', 'a3']]]
        """
        return list(map(InferenceUtils.parse, list_of_strings))

    @staticmethod
    def sort_keys(pos, neg, fac):
        """
        pos: a list of lists representing positive literals.
        neg: a list of lists representing negative literals.
        fac: a list of lists representing facts.

        Counts the number of occurances of each item in the head and body of the ground predicates.
        
        Returns two dictionaries:
        1. predicate_head_index: 
        2. predicate_body_index: 
        """

        # Count each grounding in the head and body.
        def invert_keys():
            head_cnt = Counter()
            body_cnt = Counter()
            
            for data in pos + neg + fac:
                head_cnt[data[0]] += 1
                for i in data[1]:
                    body_cnt[i] += 1

            # Invert the counts: that which is most common gets the lowest number.
            head_cnt_srt = sorted(head_cnt, key=head_cnt.get, reverse=True)
            body_cnt_srt = sorted(body_cnt, key=body_cnt.get, reverse=True)

            clause_head = {}
            clause_body = {}

            # Turn this order into a dictionary so we can query it later.
            for i in range(len(head_cnt)):
                clause_head[head_cnt_srt[i]] = i
            for i in range(len(body_cnt)):
                clause_body[body_cnt_srt[i]] = i
            return clause_head, clause_body

        predicate_head_index, predicate_body_index = invert_keys()
        return predicate_head_index, predicate_body_index

    @staticmethod
    def compress_ground_predicates(dataset, predicate_head_index, predicate_body_index):
        """
        Compress the clauses into a list that can be written to a file.
        """
        ground_predicate_list = []
        for data in dataset:
            new_predicate = ''
            new_predicate += str(predicate_head_index[data[0]]) + ','
            for b in range(len(data[1])):
                if b == (len(data[1]) - 1):
                    new_predicate += str(predicate_body_index[data[1][b]])
                else:
                    new_predicate += str(predicate_body_index[data[1][b]]) + ','
            ground_predicate_list.append(new_predicate)
        return ground_predicate_list
    
def compress_clauses(pos, neg, fac):

    """
    positive: a list of strings representing positive literals.
    negative: a list of strings representing negative literals.
    facts: a list of strings representing facts.
    """

    predicate_head_index, predicate_body_index = InferenceUtils.sort_keys(pos, neg, fac)
    
    new_pos = InferenceUtils.compress_ground_predicates(pos, predicate_head_index, predicate_body_index)
    new_neg = InferenceUtils.compress_ground_predicates(neg, predicate_head_index, predicate_body_index)
    new_fac = InferenceUtils.compress_ground_predicates(fac, predicate_head_index, predicate_body_index)

    return new_pos, new_neg, new_fac

def __main():

    # Read the arguments from the commandline.
    args = SetupArguments().args
    
    # Use the 'read' utility to read positives, negatives, and facts.
    pos = InferenceUtils.read(args.positive)
    neg = InferenceUtils.read(args.negative)
    fac = InferenceUtils.read(args.facts)

    # Use the 'ground_predicate_strings_to_ground_predicate_lists' utility to convert them.
    pos = InferenceUtils.ground_predicate_strings_to_ground_predicate_lists(pos)
    neg = InferenceUtils.ground_predicate_strings_to_ground_predicate_lists(neg)
    fac = InferenceUtils.ground_predicate_strings_to_ground_predicate_lists(fac)

    pos, neg, fac = compress_clauses(pos, neg, fac)
    print('Pos', pos)
    print('Neg', neg)
    print('Fac', fac)
    
if __name__ == '__main__':
    __main()
