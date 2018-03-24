import pprint
import binascii
from collections import namedtuple
from challenge3 import get_likeliest_key_msg

RealResult = namedtuple("RealResult", "index result")

def get_chi_squared(data):
    result = get_likeliest_key_msg(data)
    return result

def main():
    with open("c4.txt", "r", encoding="ascii") as f:
        lines = [l.strip() for l in f.readlines()]
        data = [bytearray.fromhex(l.strip()) for l in lines]
    chi_squared_and_keys = [RealResult(i, get_chi_squared(line)) for i, line in enumerate(data)]
    result = min(chi_squared_and_keys, key=lambda x: x.result.chiSquared)
    result_string = str(binascii.hexlify(data[result.index]), "utf-8")

    assert(lines[result.index] == result_string)

main()
