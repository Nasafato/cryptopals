# https://cryptopals.com/sets/1/challenges/6
# The big daddy of Set 1
from challenge1 import get_bit_in_byte
import pprint
from collections import namedtuple

LikelyKeysize = namedtuple("LikelyKeysize", "size normalizedDistance")

def get_byte_difference(a, b):
    difference = 0
    for i in range(8):
        if get_bit_in_byte(a, i) != get_bit_in_byte(b, i):
            difference += 1
    return difference

def hamming_distance(s1, s2):
    if len(s1) != len(s2):
        raise Exception

    zipped = zip(s1, s2)
    distance = 0
    for a, b in zipped:
        distance += get_byte_difference(a, b)

    return distance

def test_hamming_distance():
    s1 = b"this is a test"
    s2 = b"wokka wokka!!!"
    assert hamming_distance(s1, s2) == 37

def get_normalized_distance(data, keysize):
    block1 = data[:keysize]
    block2 = data[keysize:(2 * keysize)]

    assert len(block1) == len(block2)
    distance = hamming_distance(block1, block2)
    normalizedDistance = distance / keysize

    return normalizedDistance

def get_likeliest_keysizes(data, number=1):
    results = []
    for keysize in range(2, 41):
        normalizedDistance = get_normalized_distance(data, keysize)
        results.append(LikelyKeysize(keysize, normalizedDistance))

    results.sort(key=lambda x: x.normalizedDistance)
    return results[:number]

def breakup_blocks(data, keysize):
    blocks = []
    index = 0
    extra_bytes = len(data) % keysize
    while index < len(data):
        prev_index = index
        index += keysize
        blocks.append(data[prev_index:index])

    # make sure the last block is equal to the last block of the data
    if extra_bytes == 0:
        assert blocks[-1] == data[-keysize:]

    print("{} blocks: {} extra bytes: data is {} bytes on keysize {}".format(len(blocks), extra_bytes, len(data), keysize))
    return [bytes(b'asdf')]

def transpose_blocks(blocks, keysize):
    return [bytes(b'asdf')]

def get_single_byte_keys(tranposed_blocks):
    return b'asdf'


def get_likeliest_keys(data, potential_keysizes):
    keys = []
    pprint.pprint(potential_keysizes)
    for result in potential_keysizes[:1]:
        keysize = result.size
        blocks = breakup_blocks(data, keysize)
        transposed_blocks = transpose_blocks(blocks, keysize)
        single_byte_keys = get_single_byte_keys(transposed_blocks)
        keys.append(bytes(single_byte_keys))

    return keys

def main():
    test_hamming_distance()
    with open("c6.txt", "rb") as f:
        data = f.read()

    likeliest_keysizes = get_likeliest_keysizes(data, number=3)
    likeliest_keys = get_likeliest_keys(data, likeliest_keysizes)
    print(likeliest_keys)




if __name__ == "__main__":
    main()
