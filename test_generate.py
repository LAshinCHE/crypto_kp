import os 
import string
import numpy as np
import random

def generate_random_string(l : int):
    return ''.join(random.choices(string.ascii_letters + string.digits,k=l))

def make_test(test_count : int):
    if not os.path.exists("./test"):
        os.mkdir("test")
    os.chdir("test")
    for i in range(test_count):
        filename = f"test_{i}.txt"
        with open(filename, "w") as f:
            string_len = np.random.randint(100)
            f.write(generate_random_string(string_len))
        
    pass
    
if __name__ == '__main__':
    print("Enter the numbers of test: ")
    n = int(input())
    make_test(n)