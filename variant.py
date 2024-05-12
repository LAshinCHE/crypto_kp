from pygost import gost34112012256

try:
    data = "Черевичин Егор Викторович"  
    encoded_data = data.encode("utf-8")  
    hash_object = gost34112012256.new(encoded_data)
    hash_result = hash_object.digest()
    print(hash_result)
except Exception as e:
    print("An error occurred:", e)
