import mido
import hashlib


store={}

def inspect(filename):

     


    mid = mido.MidiFile(filename)
    # print(mid.headers)
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for message in track:
            print(message)
            print(message.bytes())
            # arr = message.bytes()
            # string=""
            # for val in arr:
            #     if (string==""):
            #         string = str(val)
            #     else:
            #         string=string+","+str(val)
            # string_hash = hashlib.sha256(string.encode()).hexdigest()
            # if string_hash not in store:
            #     store[string_hash] = 0
            # store[string_hash] += 1

            # print(string.encode())
            # if message.type == "set_tempo":
            #     print("TYOYOY")
    # for key, val in store.items():
    #     print(key, val)

if __name__ == '__main__':
    inspect("GG_Mean_Bean_Final.mid")
    