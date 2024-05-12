import unittest
import subprocess
import hashlib

import sha1

ROUNDS = 80

class TestSHA1(unittest.TestCase):
    def test_comparison(self):
        print('\n>>> test_comparison')
        for i in range(10):
            filename = f"test/test_{i}.txt"
            with open(filename, "r") as f:
                data = f.read()
                custom_sha1 = sha1.sha1(data, ROUNDS)
                lib_sha1 = hashlib.sha1(data.encode()).hexdigest()
                self.assertEqual(custom_sha1, lib_sha1)
                print('custom_sha1:', custom_sha1)
                print('lib_sha1:', lib_sha1)
                print(f'test_{i}: success')


if __name__ == '__main__':
    unittest.main()