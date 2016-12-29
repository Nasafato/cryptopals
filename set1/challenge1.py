#
# https://cryptopals.com/sets/1/challenges/1
# 49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d
# SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
import base64
import binascii
CODE = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

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
    if not test_base64(binascii.unhexlify(hex_string), final_result):
        print("ERROR: final base64 encoding test failed")


if __name__ == "__main__":
    main()





