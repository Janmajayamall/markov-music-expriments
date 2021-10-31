#!/usr/bin/python
# This class handles the storage and manipulation of a markov chain of notes.

from collections import Counter, defaultdict, namedtuple

import random

Note = namedtuple('Note', ['note', 'duration'])

class MarkovChain:

    def __init__(self):
        self.chains = {}
        self.sums = {}
        self.times = {}

    @staticmethod
    def create_from_dict(dict):
        m = MarkovChain()
        # bugged!
        for from_note, to_notes in dict.items():
            for k, v in to_notes.items():
                m.add(from_note, k, v)
        return m

    def _serialize(self, note, duration):
        return Note(note, duration)

    def __str__(self):
        return str(self.get_chain())

    def format_val(self, val):
        string = ""
        val = val[1:]
        for i in val:
            if string == "":
                string = str(i)    
            else:
                string += ":"+str(i)
        return string
    
    def add(self, from_, to_, program):
        print(from_, to_, program)
        _from = self.format_val(from_)
        _to = self.format_val(to_)

        if program not in self.chains:
            self.chains[program] = {}
        
        if _from not in self.chains[program]:
            self.chains[program][_from] = {}
        
        if _to not in self.chains[program][_from]:
            self.chains[program][_from][_to] = 0

        self.chains[program][_from][_to] += 1

        if program not in self.sums:
            self.sums[program] = {}
        
        if _from not in self.sums[program]:
            self.sums[program][_from] = 0

        self.sums[program][_from] += 1
        
        
    
    def add_time(self, duration, program):
        if program not in self.times:
            self.times[program] = []
        self.times[program].append(duration)

    def get_next(self, program, seed_note):
        chain = self.chains[program]

        if seed_note is None or seed_note not in chain:
            print("Random")
            random_chain = chain[random.choice(list(chain.keys()))]
            return random.choice(list(random_chain.keys()))
        print("Random1")
        next_note_counter = random.randint(0, self.sums[program][seed_note])
        for note, frequency in chain[seed_note].items():
            next_note_counter -= frequency
            if next_note_counter <= 0:
                return note
            
    def get_time(self, program):
        time = self.times[program]
        return [random.choice(time),random.choice(time)]

    def merge(self, other):
        assert isinstance(other, MarkovChain)
        self.sums = defaultdict(int)
        for from_note, to_notes in other.chain.items():
            self.chain[from_note].update(to_notes)
        for from_note, to_notes in self.chain.items():
            self.sums[from_note] = sum(self.chain[from_note].values())

    def get_chain(self):
        return {k: dict(v) for k, v in self.chain.items()}

    def print_as_matrix(self, limit=1000):
        out = ''
        for program, program_dict in self.chains.items():
            out += '\n ----------------'
            out += str(program)
            out += '---------------- \n'
            index = 0
            for from_note, to_notes in program_dict.items():
                out += '\n'
                out += from_note
                out += " && "
                for note in to_notes:
                    out += note
                    out += "--" 
                    out += str(to_notes[note])
                    out += "-- " 
                out += "\n"
                index += 1
                # if index >= limit :
                #     break
        print(out)

        # _col = lambda string: '{}'.format(string)
        # _note = lambda note: '{}:{}'.format(note.note, note.duration)
        # out = ' '
        # out += ''.join([_col(_note(note)) for note in columns[:limit]]) + '\n'
        # for from_note, to_notes in self.chain.items():
        #     out += _col(from_note)
        #     for note in columns[:limit]:
        #         out += _col(to_notes[note])
        #     out += '\n'
        # print(out)

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2 and sys.argv[1] == 'test':
        m = MarkovChain()
        m.add(12, 14, 200)
        m.add(12, 15, 200)
        m.add(14, 25, 200)
        m.add(12, 14, 200)
        n = MarkovChain()
        n.add(10, 13, 100)
        n.add(12, 14, 200)
        m.merge(n)
        print(m)
        m.print_as_matrix()