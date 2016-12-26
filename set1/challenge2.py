# Fixed XOR
# Write a function that takes two equal-length buffers and produces their XOR combination.

# If your function works properly, then when you feed it the string:

# 1c0111001f010100061a024b53535009181c
# ... after hex decoding, and when XOR'd against:

# 686974207468652062756c6c277320657965
# ... should produce:

# 746865206b696420646f6e277420706c6179
import binascii

def xor_byte(b1, b2):
    return b1 ^ b2

def fixed_xor(b1, b2):
    if len(b1) != len(b2):
        raise Exception

    b1 = bytearray.fromhex(b1)
    b2 = bytearray.fromhex(b2)

    b3 = bytearray([xor_byte(a, b) for a, b in zip(b1, b2)])
    print(binascii.hexlify(b3))

def main():
    b1 = "acac"
    b2 = "caca"
    fixed_xor(b1, b2)

    b1 = "1c0111001f010100061a024b53535009181c"
    b2 = "686974207468652062756c6c277320657965"

    fixed_xor(b1, b2)
    b3 = "746865206b696420646f6e277420706c6179"




main()


