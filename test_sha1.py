import unittest
import subprocess
import hashlib
import random
import string


class TestSHA1(unittest.TestCase):
    def test_comparison(self):
        print('\n>>> test_comparison')
        msg = get_random_string()

        custom_sha1 = run_go_sha1(msg)
        lib_sha1 = hashlib.sha1(msg.encode()).hexdigest()

        print('... test_comparison: checking for identical digests (random string)')
        self.assertEqual(custom_sha1, lib_sha1)
        print('... test_comparison: success')

        tests = ('abc', '', 'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq',
                 'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu',
                 'a' * 1000000)

        print('... test_comparison: checking for identical digests (test cases)')
        for test in tests:
            print('... test: ', test if len(test) < 10**6 else 'a (1,000,000 repetitions)')
            custom_sha1 = run_go_sha1(test)
            lib_sha1 = hashlib.sha1(test.encode()).hexdigest()
            self.assertEqual(custom_sha1, lib_sha1)
        print('... test_comparison: success')


def get_random_string():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(10, 10 ** 5)))


def run_go_sha1(msg):
    process = subprocess.Popen(['./sha1_executable', '--input', msg],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                               cwd='E:\\goLangProject\\crypto')
    output, _ = process.communicate()
    return output.strip()

if __name__ == '__main__':
    unittest.main()