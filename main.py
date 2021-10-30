import mido
import hashlib


store={}

def inspect(filename):
    mid = mido.MidiFile(filename)
    # print(mid.headers)
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for message in track:
            if message.type == "set_tempo":
                print("tempo" , message.tempo)
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
    inspect("aladcrisis.mid")


# 1. Make different probability set for different instruments
# 2. Categorise data by note & velocity & program
# 3. Create different tracks for each program
# 4. Create 

    