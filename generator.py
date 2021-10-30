#!/usr/bin/python
# This class handles the generation of a new song given a markov chain
# containing the note transitions and their frequencies.

from markov_chain import MarkovChain

import random
import mido

class Generator:

    def __init__(self, markov_chain):
        self.markov_chain = markov_chain

    @staticmethod
    def load(markov_chain):
        assert isinstance(markov_chain, MarkovChain)
        return Generator(markov_chain)

    def get_msg(self, note):
        note = note.split(":")
        new_note = []
        for i in note:
            new_note.append(int(i))
        return mido.parse(new_note)

    def _note_to_message(self, note, duration):
        msg = self.get_msg(note)
        extension = [msg]
        extension.append(mido.Message('note_off', channel=msg.channel, note=msg.note, velocity=0, time=duration))
        return extension
        # # return [
        # #     mido.Message('note_on', channel=9, note=note.note, velocity=90,
        # #                  time=0),
        #     mido.Message('note_off', channel=9, note=note.note, velocity=0,
        #                  time=note.duration)
        # # ]

    def generate(self, filename):
        note_off = None
        with mido.midifiles.MidiFile() as midi:
            track = mido.MidiTrack()
            last_note = None
            # Generate a sequence of 100 notes
            for i in range(1000):
                new_note = self.markov_chain.get_next(last_note)
                duration = self.markov_chain.get_time()
                track.extend(self._note_to_message(new_note, duration))
                
                # get last note
                # arr = new_note.split(":")
                # arr = arr[:3]
                # arr_str = ""
                # for i in arr:
                #     if arr_str == "":
                #         arr_str = i
                #     else:
                #         arr_str += ":" + i
                last_note = new_note
            midi.tracks.append(track)
            midi.save(filename)

if __name__ == "__main__":
    import sys
    from parser import Parser
    chain = Parser("Battle_Neo_Ghetsis.mid").get_chain()
    Generator.load(chain).generate("o1.mid")