import struct
from binascii import unhexlify, hexlify

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash

import vulnecc
from jwcrypto import jwk, jwe
from jwcrypto.common import base64url_decode


def derive_key(privkey, point_x, point_y, alg, bitsize, headers):
    # OtherInfo is defined in NIST SP 56A 5.8.1.2.1

    # AlgorithmID
    otherinfo = struct.pack('>I', len(alg))
    otherinfo += bytes(alg.encode('utf8'))

    # PartyUInfo
    apu = base64url_decode(headers['apu']) if 'apu' in headers else b''
    otherinfo += struct.pack('>I', len(apu))
    otherinfo += apu

    # PartyVInfo
    apv = base64url_decode(headers['apv']) if 'apv' in headers else b''
    otherinfo += struct.pack('>I', len(apv))
    otherinfo += apv

    # SuppPubInfo
    otherinfo += struct.pack('>I', bitsize)

    print(otherinfo)

    # no SuppPrivInfo

    # Shared Key generation

    x, y = point_x, point_y
    P = vulnecc.AffinePoint(vulnecc.curveP256_vuln, x, y)
    s = privkey
    shared = s * P
    shared_key = int.to_bytes(shared.x, 32, "big")

    ckdf = ConcatKDFHash(
        algorithm=hashes.SHA256(),
        length=bitsize // 8,
        otherinfo=otherinfo,
        backend=default_backend()
    )
    return ckdf.derive(shared_key)


def _encode_int(n, bits):
    e = '{:x}'.format(n)
    ilen = ((bits + 7) // 8) * 2  # number of bytes rounded up times 2 bytes
    return unhexlify(e.rjust(ilen, '0')[:ilen])


def _decode_int(n):
    return int(hexlify(n), 16)


priv = {"crv":"P-256","d":"29FABiRtn3-GOQNEH3jTZj8KywLb38fHQAtfvWaXSC4","kty":"EC","size":2048,"x":"2RntSELMcr5qVFmhWZiCKS0NzkZwm3f0dwbXythHYTw","y":"wJgR6ZgJB6lVZFHF-vQ_biOfOAHuTZayzIE55cCbHEM"}
pub = {"crv":"P-256","kty":"EC","x":"2RntSELMcr5qVFmhWZiCKS0NzkZwm3f0dwbXythHYTw","y":"wJgR6ZgJB6lVZFHF-vQ_biOfOAHuTZayzIE55cCbHEM"}

print(_decode_int(base64url_decode(priv['d'])))
# {"ciphertext":"BFNqIIeTIFFqzqhMTgqogYEME2osaAW_3uGQoOrrYYk","header":{"epk":{"crv":"P-256","kty":"EC","x":"9WZ2GQsgaEfyPEOM876DEHbDfQcI0HpOuZIYZls6osc","y":"eLP6pQjqyvM-jBkOIGTGd_1V5N0ELt6ITA2R4R-fTlY"}},"iv":"ZBlyAnsAGm_a6ITI2bjxsw","protected":"eyJhbGciOiJFQ0RILUVTIiwiZW5jIjoiQTI1NkNCQy1IUzUxMiIsImtpZCI6ImVmSDNxazFReHBtTnZxaFkzelhvU0VmZ21sOF83dW5Lb0tydm9ESWNCMWMiLCJ0eXAiOiJKV0UifQ","tag":"5PlTCduYuUqRl0USE-My_d5VvTB1k9szNERYELSL9DM"}

# order 3
invalid_curve_b = 40762520383452945195843938160544742543174561344916535813974395963913031940110
invalid_curve_point = [112699601695560561689738873491898987764801993883781788339365544038894281043223, 49551986547310344854660704331867483487413289303304394569830017282056791717415]

public_key = jwk.JWK()
public_key.import_key(**pub)

private_key = jwk.JWK()
private_key.import_key(**priv)

payload = "My Encrypted message"
protected_header = {
        "alg": "ECDH-ES",
        "enc": "A256CBC-HS512",
        "typ": "JWE",
        "kid": public_key.thumbprint(),
}

aes_key = derive_key(1, point_x=invalid_curve_point[0], point_y=invalid_curve_point[1], alg='A256CBC-HS512', bitsize=512, headers={'alg': 'ECDH-ES', 'enc': 'A256CBC-HS512', 'kid': 'efH3qk1QxpmNvqhY3zXoSEfgml8_7unKoKrvoDIcB1c', 'typ': 'JWE'})

print(aes_key.hex())

jwetoken = jwe.JWE(
    payload.encode(),
    recipient=public_key,
    protected=protected_header,
    point_x=invalid_curve_point[0],
    point_y=invalid_curve_point[1],
    aes_key=aes_key
)


enc = jwetoken.serialize(compact=True)
print(enc)

secret_key = _decode_int(base64url_decode('29FABiRtn3-GOQNEH3jTZj8KywLb38fHQAtfvWaXSC4'))
print(secret_key % 3)
jwetoken = jwe.JWE()
jwetoken.deserialize('eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiRUNESC1FUyIsImtpZCI6ImVmSDNxazFReHBtTnZxaFkzelhvU0VmZ21sOF83dW5Lb0tydm9ESWNCMWMiLCJlcGsiOnsia3R5IjoiRUMiLCJjcnYiOiJQLTI1NiIsIngiOiJvbVFDWWN0RmZldmo0ZjlTd1VELWUxSFNHeGV4WFZrQ1g3VnR0MlU3cFNZIiwieSI6IkhPaEpMd3RscnlpNXRuckp6aXV1WFNlRmhFSV9DdHBEUmprb1BPeEdPY0EifX0..48Ai8o46DUCTZAKUSFNf6w.PpEfH--Ev4X3dO3dqnEboA.Xcz0-mOoPrTCxVn4eyUnHg', key=private_key)
payload = jwetoken.payload

print(payload)
