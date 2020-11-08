"""
Calculate master secret from a given server private key and client public key.
"""
from tlslite.mathtls import PRF_1_2
from tlslite import keyexchange
from Crypto.Cipher import AES

SERVER_SECRET = 0x28da0b0edbce0a2cca8489b8ac7dae1baa0a40043f68b34b2052d51034d8e41a

def key_deriv(premaster_secret, client_random, server_random):
    """
    Returns master secret.
    """
    return PRF_1_2(
        premaster_secret, b"master secret",
        client_random + server_random, 48
    )


def key_expansion(master_secret, client_random, server_random, length=16*8):
    return PRF_1_2(master_secret, b"key expansion", server_random + client_random, length)


def decrypt(key, msg, nonce):
    aes = AES.new(key, AES.MODE_CCM, nonce=nonce)
    return aes.decrypt(msg)

client_random = bytes.fromhex('00000000169e0bc70b8f32d72b6f0d9f57bbe57ca665743dc5e2ebed8f5c806b')
server_random = bytes.fromhex('000000001a2cfd1e0f766148f351d7cba6dba4d3910a0cd712a28604af043dfe')

client_pub = bytes.fromhex('041d82205c3edf02361029576319b45c787f3a4a8ee9b4597cf405fecc8133797fb216eab117a4cca337fa05af3dea9e05ad7aecd6a6336d2bb2d477de5d58b5ca')


kex = keyexchange.ECDHKeyExchange(0x0017, 0x0303)
Z = kex.calc_shared_key(SERVER_SECRET, client_pub)
print(Z.hex())
master_secret = key_deriv(Z, client_random, server_random)
print('Master Secret:', master_secret.hex())
key_block = key_expansion(master_secret, client_random, server_random)

client_enc = key_block[:16]  # mac key is 20 bytes for
server_enc = key_block[16:32]
# tiny dtls expands nonce with counter
client_iv = key_block[32:32+4] + bytes.fromhex('0001000000000001')
server_iv = key_block[36:36+4] + bytes.fromhex('0001000000000001')

print(client_enc.hex())
print(client_iv.hex())

# encrypted msg from client

ENCRYPTED_CONTENT = '25d8b7bfadad92acc72dec445878596e8f9c14477dc684360b26f07d318d21267072ab'
res = bytes.fromhex(ENCRYPTED_CONTENT)
print()
DATA = bytes.fromhex('0001000000000001bb2cb9ad111cda8a8a13672aab0efecc3de4bb1c326542375679c51cef1137767f1c6e820204f51294f4705e4fb74c7dfc6acad7b49d244f1e8efda78544cc')

for i in range(len(DATA)):
    t = decrypt(client_enc, DATA[i:], client_iv)
    if t.startswith(b"CSR{"):
        print(t)
        break

