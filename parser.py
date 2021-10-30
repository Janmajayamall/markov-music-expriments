#!/usr/bin/python
# This class handles the parsing of a midi file and builds a markov
# chain from it.

import hashlib
import mido
import argparse
import copy

from markov_chain import MarkovChain 


class Parser:

    def __init__(self, filename, verbose=False):
        """
        This is the constructor for a Serializer, which will serialize
        a midi given the filename and generate a markov chain of the
        notes in the midi.
        """
        self.filename = filename
        # The tempo is number representing the number of microseconds
        # per beat.
        self.tempo = None
        # The delta time between each midi message is a number that
        # is a number of ticks, which we can convert to beats using
        # ticks_per_beat.
        self.ticks_per_beat = None
        self.markov_chain = MarkovChain()
        self._parse(verbose=verbose)

    def _parse(self, verbose=False):
        """
        This function handles the reading of the midi and chunks the
        notes into sequenced "chords", which are inserted into the
        markov chain.
        """
        midi = mido.MidiFile(self.filename)
        # print("Ticks per beat - ", midi.ticks_per_beat)
        self.ticks_per_beat = midi.ticks_per_beat
        previous_chunk = []
        current_chunk = []

        for track in midi.tracks:
            index = 0
            prev=[]
            curr=[]
            for msg in track:
                if msg.type == "note_on" and msg.time != 0:
                    # make the current state
                    for vp in prev:
                        for vc in curr:
                            self.markov_chain.add(vp.bytes(), vc.bytes(), ctime)
                    prev=curr
                    curr=[]
                if msg.type == "note_off":
                    # make the current state
                if msg.type == "note_on" and msg.time == 0:
                    # carry on

                    print(msg)
                    if msg.time != 0:
                        #crete connections
                        if len(curr) != 0:
                            # print("-------")
                            # print(msg.time)
                            # print(prev)
                            # print(curr)
                            # print("-------")
                            ctime = curr[0].time
                            # print(ctime)
                            # print(curr)
                            for vp in prev:
                                for vc in curr:
                                    print("---------------------")
                                    print(vp,vc)
                                    print(vp.bytes(),vc.bytes())
                                    print("---------------------")
                                    self.markov_chain.add(vp.bytes(), vc.bytes(), ctime)
                        prev=curr
                        curr=[]
                    curr.append(msg)
            
        # for track in midi.tracks:
        #     for message in track:
        #         if verbose:
        #             print(message, midi.ticks_per_beat)
        #         if message.type == "set_tempo":
        #             self.tempo = message.tempo
        #         elif message.type != "note_off":
        #             if message.time == 0:
        #                 current_chunk.append(message.bytes())
        #             else:
        #                 current_chunk.append(message.bytes())
        #                 self._sequence(previous_chunk,
        #                                current_chunk,
        #                                message.time)
        #                 previous_chunk = current_chunk
        #                 current_chunk = []


    def _sequence(self, previous_chunk, current_chunk, duration):
        """
        Given the previous chunk and the current chunk of notes as well
        as an averaged duration of the current notes, this function
        permutes every combination of the previous notes to the current
        notes and sticks them into the markov chain.
        """
        for n1 in previous_chunk:
            for n2 in current_chunk:
                self.markov_chain.add(
                    n1, n2, self._bucket_duration(duration))

    def _bucket_duration(self, ticks):
        """
        This method takes a tick count and converts it to a time in
        milliseconds, bucketing it to the nearest 250 milliseconds.
        """
        try:
            ms = ((ticks / self.ticks_per_beat) * self.tempo) / 1000
            return int(ms - (ms % 250) + 250)
        except TypeError:
            raise TypeError(
                "Could not read a tempo and ticks_per_beat from midi")

    def get_chain(self):
        return self.markov_chain

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("input_file", help="The midi file input")
    # args = parser.parse_args()
    print(Parser("GG_Mean_Bean_Final.mid", verbose=True).markov_chain.print_as_matrix())
    # print('No issues parsing {}'.format(args.input_file))