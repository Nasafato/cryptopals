#
# https://cryptopals.com/sets/1/challenges/1
# 49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d
# SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
import base64
import binascii
import cProfile
import array
CODE = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
CHAR_TO_INT = dict([(c, i) for i, c in enumerate(CODE)])

def get_bit_in_byte(b, index, startFromMsb=False):
    if index > 7:
        raise IndexError

    max_index = 7
    if startFromMsb:
        target_index = max_index - index
    else:
        target_index = index

    max_index = 7
    return int((1 << target_index) & b != 0)

def get_bit_in_byte_array(byte_array, index):
    byte_index =  index // 8
    bit_index_in_byte = index % 8
    target_byte = byte_array[byte_index]
    bit = get_bit_in_byte(target_byte, bit_index_in_byte, startFromMsb=True)
    return bit

def base64encode(byte_array):
    output_chars = []
    num_bytes = len(byte_array)
    num_bits = 8 * num_bytes

    code_index = 0
    bits_counted = 0

    # for every block of 6 bits, we're going to turn the number represented by those
    # 6 bits into a character in the base64 alphabet represented in CODE
    # Basically, 2^6 = 64, so every 6 bits will definitely be <= 64.
    # We can easily come up with 64 printable characters, so base64 encoding is a way of making sure
    # that any binary data we have, we can always turn it into an ASCII-printable representation,
    # either for visualization's sake or for use with data transmission protocols that are reliant on
    # transmitting ASCII characters
    # So, we transform a block of 6 bits into an index - we then get CODE[index] to get the character we'll
    # use to represent those 6 bits.
    for index in range(num_bits):
        bit = get_bit_in_byte_array(byte_array, index)
        if bit:
            code_index += int(pow(2, 5 - bits_counted))
        bits_counted += 1
        if bits_counted % 6 == 0:
            output_chars.append(CODE[code_index])
            code_index = 0
            bits_counted = 0

    return bytes(output_chars)

def int_to_bits(num):
    result = [get_bit_in_byte(num, i, startFromMsb=True) for i in range(2, 8)]
    return result

# Each block should be 4 characters
def char_block_to_byte_block(block):
    byte_array = [0x00] * 3
    bits = [i for six_bits in [int_to_bits(CHAR_TO_INT[c]) for c in block] for i in six_bits]
    for i, bit in enumerate(bits):
        if bit == 0:
            continue
        byte_index = i // 8
        bit_index = i % 8
        from_msb_index = 7 - bit_index
        byte_array[byte_index] = byte_array[byte_index] | (1 << from_msb_index)

    # return b_array.extend([int_to_bits(CHAR_TO_INT[c]) for c in block])
    return bytes(byte_array)

# To reverse a base 64 encoding, we can go character by character. We get the index of the character to get
# the 6 bits we'll need
# Now, with these 6 bits, we need to somehow turn them into bytes again
# We need to first make sure that there are the correct number of bits - since we'll be turning these
# characters into bytes, every character is 3/4 of a byte (6 bits when a byte is 8 bits)
# Thus, we need to make sure that when we multiply the length of the base64-encoded string by 6, it comes out
# to a multiple of 8, which will tells us that we can evenly fit all the bits into bytes
# Every 4 characters is 3 bytes, so we should be taking this input array in groups of 4
def base64decode(byte_array):
    # are these equivalent? Yes, I believe so
    assert len(byte_array) * 6 % 8 == 0
    assert len(byte_array) % 4 == 0

    index = 4
    blocks = []
    while index <= len(byte_array):
        blocks.append(byte_array[index - 4:index])
        index += 4

    assert len(blocks) == len(byte_array) // 4

    byte_blocks = [char_block_to_byte_block(block) for block in blocks]

    return bytes([b for byte_block in byte_blocks for b in byte_block])

def test_index(binary_string, b_array, index):
    test_result = get_bit_in_byte_array(b_array, index)
    answer = int(binary_string[index])
    if test_result != answer:
        return False
    return True

def test_simple_base64(b_array):
    result = base64encode(b_array)
    if result != b'YWJj':
        return False
    return True

def test_base64(b_array, solution):
    result = base64encode(b_array)
    if result != solution:
        return False
    return True

def main():
    hex_string = b"49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

    # test_string = "abc"
    # binary_string = ''.join(format(ord(c), '08b') for c in test_string)
    # b_array = bytes(test_string, 'ascii')

    # for index in range(len(binary_string)):
    #     if not test_index(binary_string, b_array, index):
    #         print("ERROR: get_bit_at_index test failed")
    #         break

    # if not test_simple_base64(b_array):
    #     print("ERROR: simple base64 encoding test failed")

    final_result = b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    unhexlified_input_string = binascii.unhexlify(hex_string)
    assert base64encode(unhexlified_input_string) == final_result

    decode_result = base64decode(final_result)
    hexlified_decode_result = binascii.hexlify(base64decode(final_result))
    assert hexlified_decode_result == hex_string


if __name__ == "__main__":
    cProfile.run('main()')
    # main()





