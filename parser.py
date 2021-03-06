#!/usr/bin/python
# This class handles the parsing of a midi file and builds a markov
# chain from it.

import hashlib
import mido
import argparse
import copy

from markov_chain import MarkovChain 


class Parser:

    def __init__(self, filenames, verbose=False):
        """
        This is the constructor for a Serializer, which will serialize
        a midi given the filename and generate a markov chain of the
        notes in the midi.
        """
        self.filenames = filenames
        # The tempo is number representing the number of microseconds
        # per beat.
        self.tempo = None
        # The delta time between each midi message is a number that
        # is a number of ticks, which we can convert to beats using
        # ticks_per_beat.
        self.ticks_per_beat = None
        self.markov_chain = MarkovChain()
        for i in filenames:
            self._parse(i, verbose=verbose)

    def _parse(self, filename, verbose=False):
        """
        This function handles the reading of the midi and chunks the
        notes into sequenced "chords", which are inserted into the
        markov chain.
        """
        midi = mido.MidiFile(filename)
        # print("Ticks per beat - ", midi.ticks_per_beat)
        # self.ticks_per_beat = midi.ticks_per_beat
        track = None

        for i in midi.tracks:
            for msg in i:
                if msg.type == "program_change":
                    track = i
                    break
            if track != None:
                break

        program = None
        for track in midi.tracks:
            prev=[]
            curr=[]
            index = 0
            # print("   damoi")
            while index < len(track):
                if track[index].type == "program_change":
                    program = track[index].program
                    print(program)
                    index += 1
                elif (track[index].type == "note_off"):
                    self.markov_chain.add_time(track[index].time, program)
                    index += 1
                elif track[index].type == "note_on":
                    self.markov_chain.add_time(track[index].time, program)
                    curr.append(track[index])
                    index += 1
                    while index < len(track) and track[index].type == "note_on" and track[index].time == 0:
                        curr.append(track[index])
                        index += 1
                    for vp in prev:
                        for vc in curr:
                            self.markov_chain.add(vp.bytes(), vc.bytes(), program)
                    prev = curr
                    curr = []
                else:
                    index += 1

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
    print(Parser(["COMETOGE.mid", "m1.mid"], verbose=True).markov_chain.print_as_matrix())
    # print('No issues parsing {}'.format(args.input_file))
