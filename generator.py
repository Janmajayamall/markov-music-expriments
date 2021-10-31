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

    def _note_to_message(self, note, durations, channel):
        note = note.split(":")
        extension = [mido.Message('note_on', channel=channel, note=int(note[0]), velocity=int(note[1]), time=durations[0]),
                        mido.Message('note_off', channel=channel, note=int(note[0]), velocity=34, time=durations[1])]
        return extension

    def generate(self, filename):
        note_off = None
        with mido.midifiles.MidiFile() as midi:
            channel = 0
            for program, chain in self.markov_chain.chains.items():
                # or (program >= 97 and program <= 128)
                # if (program >= 57 and program <= 64):
                #     continue
                if channel > 15:
                    continue
                track = mido.MidiTrack()
                track.extend([mido.MetaMessage('set_tempo', tempo=1875000, time=0)])
                track.extend([mido.Message('program_change', channel=channel, program=int(program), time=0)])
                last_note = None
                # Generate a sequence of 100 notes
                for i in range(1000):
                    note = self.markov_chain.get_next(program, last_note)
                    durations = self.markov_chain.get_time(program)
                    track.extend(self._note_to_message(note, durations, channel))
                    last_note = note
                midi.tracks.append(track)
                channel+=1
            midi.save(filename)


if __name__ == "__main__":
    import sys
    from parser import Parser
    chain = Parser(["Mario_Paint_Gnat_Attack_Boss_Theme.mid", "Mario_is_Missing_NES-New_York.mid", "MARIOBRO.mid", "sms_underground.mid"]).get_chain()
    Generator.load(chain).generate("o1.mid")