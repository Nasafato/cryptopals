# Single-byte XOR cipher
# The hex encoded string:

# 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
# ... has been XOR'd against a single character. Find the key, decrypt the message.

# You can do this by hand. But don't: write code to do it for you.

# How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.

import string
import binascii
from collections import namedtuple, defaultdict

Result = namedtuple("Result", "chiSquared key string")

FREQS = [
    0.0651738, 0.0124248, 0.0217339, 0.0349835,  # 'A', 'B', 'C', 'D',...
    0.1041442, 0.0197881, 0.0158610, 0.0492888,
    0.0558094, 0.0009033, 0.0050529, 0.0331490,
    0.0202124, 0.0564513, 0.0596302, 0.0137645,
    0.0008606, 0.0497563, 0.0515760, 0.0729357,
    0.0225134, 0.0082903, 0.0171272, 0.0013692,
    0.0145984, 0.0007836, 0.1918182
]


def score(message):
    score = 0
    char_count = [0 for i in range(len(FREQS))]
    ascii_plus_space = string.ascii_lowercase + " "
    ignored_table = defaultdict(int)
    upperA = ord(b'A')
    upperZ = ord(b'Z')
    lowerZ = ord(b'a')
    lowerA = ord(b'z')
    space = ord(b' ')

    for c in message:
        if upperA <= c <= upperZ:
            char_count[c - upperA] += 1
        elif lowerA <= c <= lowerZ:
            char_count[c - lowerA] += 1
        elif c == space:
            char_count[-1] += 1
        else:
            ignored_table[c] += 1

    ignored_count = ignored_table.values()
    total = sum(char_count) + sum(ignored_count)
    chi_squared = 0
    for index, count in enumerate(char_count):
        expected = FREQS[index] * total
        difference = count - expected
        chi_squared += difference * difference / expected

    for index, count in enumerate(ignored_count):
        expected = .01 / total
        difference = count - expected
        chi_squared += difference * difference / expected

    # print("{}, {}".format(chi_squared, message))
    return chi_squared

def get_likeliest_key_msg(b_array):
    candidates = []
    for c in range(0xff):
        key_byte_array = bytearray([c] * len(b_array))
        output = [x ^ y for x, y in zip(b_array, key_byte_array)]
        output_string = bytes(output)
        output_score = score(output_string)
        candidates.append(Result(output_score, c, output_string))

    result = min(candidates, key=lambda x: x.chiSquared)
    return result

def main():
    s = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    b = bytearray.fromhex(s)

    result = get_likeliest_key_msg(b)
    print(result)

if __name__ == "__main__":
    main()





