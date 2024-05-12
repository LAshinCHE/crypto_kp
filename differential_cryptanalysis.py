import random
import string
import logging

import bitarray
import matplotlib.pyplot as plt

import sha1



def get_random_string(N=50):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(N))


def flip_random_bit(input_string):
    index = random.randint(0, len(input_string) - 1)
    char_code = ord(input_string[index])
    bit_position = random.randint(0, 7)
    new_char_code = char_code ^ (1 << bit_position)
    new_char = chr(new_char_code)
    return input_string[:index] + new_char + input_string[index+1:]

def bitcount(n):
    return bin(n).count('1')


def mean(l):
    return [int(sum(i)/len(i)) for i in zip(*l)]


if __name__ == '__main__':
    logging.basicConfig(filename="cryptanalysis.log", level=logging.INFO)

    test_byte_diff = []
    for i in range(0, 10):

        logging.info(f"TEST NUMBER: {i + 1}")
        filename =  f"test/test_{i}.txt"
        with open(filename, "r") as f:
            data = f.read()
        changed_data = flip_random_bit(data)

        logging.info(f"CURENT STRING: {data}")
        logging.info(f"DIFFER STRING: {changed_data}")

        diffs = []
        for count_round in range(0,80 + 1, 5):
            logging.info(f"NUMBER OF ROUNDS: {count_round}")
            hash1 = sha1.sha1(data, count_round)
            hash2 = sha1.sha1(changed_data, count_round)
            logging.info(f"ORIGINAL HASH:  {hash1}")
            logging.info(f"CHANGED HASH:   {hash2}")
            diff_number = bitcount(int(hash1, 16) ^ int(hash2, 16))
            diffs.append(diff_number)
            logging.info("NUMBER OF DIFFERENT BITS: ".format(diff_number))
        logging.info("------------")
        test_byte_diff.append(diffs)

    rounds_count = [i for i in range(0, 80 + 1, 5)]
    mean_diffs = mean(test_byte_diff)

    plt.bar(rounds_count, mean_diffs, align='center')
    plt.xlabel('Count rounds')
    plt.ylabel('Count of different bits')
    plt.show()