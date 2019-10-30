import Crypto.Util.number as cry
import gmpy
import random

def generate_keys(nbits):
    p = cry.getPrime(nbits//2)
    q = cry.getPrime(nbits//2)
    n = p*q
    g = n+1
    l = (p-1)*(q-1)
    mu = gmpy.invert(((p-1)*(q-1)), n)
    return (n, g, l, mu)

def encrypt(key, msg, rand):
    n_sqr = key[0]**2
    return (pow(key[1], msg, n_sqr)*pow(rand, key[0], n_sqr) ) % n_sqr

def decrypt(key, cipher):
    return (((pow(cipher, key[2], key[0]*key[0]) - 1)// key[0]) * key[3]) % key[0]

def get_random_number(n):
    return random.randint(n//2, n*2)

def decrypt2(key, cipher):
    n_sqr = key.modulus * key.modulus
    # Remove random factor from the encryption.
    noise = pow(RANDOM, key.modulus, n_sqr)
    invnoise = gmpy.invert(noise, n_sqr)
    normalized = (cipher * invnoise) % n_sqr
    # The n^2 modulus isn't a hard case of the discrete logarithm problem.
    return ((normalized-1)//key.modulus) // ((key.generator-1)//key.modulus)

def paillier_poc():
    N_BITS = 1024
    MSG = 1337

    key = generate_keys(N_BITS)
    rand = get_random_number(N_BITS)

    cipher = encrypt(key, MSG, rand)
    decipher = decrypt(key, cipher)

    print("The message is {}\n".format(MSG))
    print("The cipher is {}\n".format(cipher))
    print("The decipher is {}\n".format(decipher))

if __name__ == '__main__':
    paillier_poc()

