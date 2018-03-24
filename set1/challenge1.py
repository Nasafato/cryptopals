import unittest
# https://cryptopals.com/sets/1/challenges/1

# So given a string, I need to turn it into base64
# The problem is - does this mean I need to convert the string into raw bytes? Or 
# is this conversion just pretty-printing them?
# It seems like I'm just supposed to turn one string into another

# I guess it doesn't matter if the input string is unicode or whatever -- 
# just turn it into bytes

class Converter:
    def hex_to_base64(self, hex_string):
        raw_bytes = bytes(hex_string, encoding='utf-8')

        encoded_strings = []
        for set_of_3_index in range(len(raw_bytes) // 3, step=3):
            bytes_to_encode = raw_bytes[set_of_3_index:set_of_3_index+3]
            encoded_strings.append(self.triplet_to_base64(bytes_to_encode))

        return "".join(encoded_strings)

    def triplet_to_base64(self, set_of_3):
        needs_padding = len(set_of_3) % 3 > 0
        if needs_padding:
            num_bytes_to_pad = 3 - len(set_of_3)
            set_of_3 += bytes([0 for i in range(num_bytes_to_pad)])
        
        



class TestConverter(unittest.TestCase):
    def test_basic(self):
        string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        solution = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        converter = Converter()
        self.assertEqual(converter.hex_to_base64(string), solution)

if __name__ == "__main__":
    unittest.main()