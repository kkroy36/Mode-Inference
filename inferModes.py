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
from builtins import object
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
    
class SetupArguments(object):
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
    def parse(predicate_string):
        """
        Input a string of the format:
           'father(harrypotter,jamespotter).'
        Ensures syntax is correct, then returns a list where [0] is the name of the literal
        and [1] is a list of variables in the rule.
           ['father', ['harrypotter', 'jamespotter']]
        """
        inspect_instance_syntax(predicate_string)
        
        predicate_list = predicate_string.replace(' ', '').split(')', 1)[0].split('(')
        predicate_list[1] = predicate_list[1].split(',')
        return predicate_list
        
class Data:

    def __init__(self, positive, negative, facts):
        self.pos_data = [self.parse(data) for data in self.read(positive)]
        self.neg_data = [self.parse(data) for data in self.read(negative)]
        self.fac_data = [self.parse(data) for data in self.read(facts)]

        self.predicate_head_index = self.build_head_index()
        self.predicate_body_index = self.build_body_index()

        """
        @batflyer: Now that I've built the inverted indexes, I can rebuild the predicates to use the number system.
        """

        # For illustrative purposes.
        updated_pos = self.format_lister(self.pos_data)
        updated_neg = self.format_lister(self.neg_data)
        updated_fac = self.format_lister(self.fac_data)

        print('Pos Before:', self.pos_data)
        print('Pos:', updated_pos)
        print('Neg:', updated_neg)
        print('Facts:', updated_fac)

        # How many predicates do we have?
        print(len(self.predicate_head_index))

        # How many objects do we have?
        print(len(self.predicate_body_index))

        # Head Set:
        # 
        
    def build_sets(self, dataset):
        """
        
        """
        # Start from the largest set with an unknown type, pick unused variable ['A', 'B', ...]:
        # for each set:
        #     If intersection: type of set2 -> type of set1
        #     Else: continue
        
        pass
        

    def format_printer(self, dataset):
        for data in dataset:
            print(str(self.predicate_head_index[data[0]]) + ',', end='')
            for b in range(len(data[1])):
                if b == (len(data[1]) - 1):
                    print(self.predicate_body_index[data[1][b]])
                else:
                    print(self.predicate_body_index[data[1][b]], end=',')

    def format_lister(self, dataset):
        predicate_list = []
        for data in dataset:
            new_predicate = ''
            new_predicate += str(self.predicate_head_index[data[0]]) + ','
            for b in range(len(data[1])):
                if b == (len(data[1]) - 1):
                    new_predicate += str(self.predicate_body_index[data[1][b]])
                else:
                    new_predicate += str(self.predicate_body_index[data[1][b]]) + ','
            predicate_list.append(new_predicate)
        return predicate_list

    def read(self, path):
        """
        Assumes that data are stored on separate lines.
        """
        try:
            with open(path) as f:
                data = f.read().splitlines()
            return data
        except:
            raise Exception('Could not open file, no such file or directory.')

    def parse(self, predicate_string):
        """
        Input a string of the format:
           'father(harrypotter,jamespotter).'
        Ensures syntax is correct, then returns a list where [0] is the name of the literal
        and [1] is a list of variables in the rule.
           ['father', ['harrypotter', 'jamespotter']]
        """
        inspect_instance_syntax(predicate_string)
        
        predicate_list = predicate_string.replace(' ', '').split(')', 1)[0].split('(')
        predicate_list[1] = predicate_list[1].split(',')
        return predicate_list

    def build_head_index(self):
        head_cnt = Counter()
        for data in self.pos_data + self.neg_data + self.fac_data:
            head_cnt[data[0]] += 1
        head_cnt_srt = sorted(head_cnt, key=head_cnt.get, reverse=True)
        index = {}
        for i in range(len(head_cnt)):
            index[head_cnt_srt[i]] = i
        return index

    def build_body_index(self):
        body_cnt = Counter()
        for data in self.pos_data + self.neg_data + self.fac_data:
            for i in data[1]:
                body_cnt[i] += 1
        body_cnt_srt = sorted(body_cnt, key=body_cnt.get, reverse=True)
        index = {}
        for i in range(len(body_cnt)):
            index[body_cnt_srt[i]] = i
        return index

class Modes:
    """
    Perform mode inference.
    """

    def __init__(self):
        pass

def Abstractify():
    pass

def __main():
    args = SetupArguments().args
    d = Data(args.positive, args.negative, args.facts)
    #print(d.fac_data)
    
if __name__ == '__main__':
    __main()
