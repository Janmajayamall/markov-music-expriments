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

    def get_note(self, note):
        note = note.split(":")
        new_note = []
        for i in note:
            new_note.append(int(i))
        return new_note[:3],new_note[-1]

    def _note_to_message(self, note):
        new_note,duration = self.get_note(note)
        msg = mido.parse(new_note)
        extension = [msg]
        if msg.type == 'note_on':
            extension.append( mido.Message('note_off', channel=msg.channel, note=msg.note, velocity=msg.velocity, time=duration))
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
                track.extend(self._note_to_message(new_note))
                
                # get last note
                arr = new_note.split(":")
                arr = arr[:3]
                arr_str = ""
                for i in arr:
                    if arr_str == "":
                        arr_str = i
                    else:
                        arr_str += ":" + i
                last_note = arr_str
            midi.tracks.append(track)
            midi.save(filename)

if __name__ == "__main__":
    import sys
    from parser import Parser
    chain = Parser("GG_Mean_Bean_Final.mid").get_chain()
    Generator.load(chain).generate("o1.mid")