from jwcrypto import jwk, jwe

pub = {"crv":"P-256","kty":"EC","x":"2RntSELMcr5qVFmhWZiCKS0NzkZwm3f0dwbXythHYTw","y":"wJgR6ZgJB6lVZFHF-vQ_biOfOAHuTZayzIE55cCbHEM"}

public_key = jwk.JWK()
public_key.import_key(**pub)


def encrypt(msg):
    jwetoken = jwe.JWE(
        msg.encode(),
        recipient=public_key,
        protected={
            "alg": "ECDH-ES",
            "enc": "A256CBC-HS512",
            "typ": "JWE",
            "kid": public_key.thumbprint(),
        }
    )
    return jwetoken.serialize(compact=True)

msgs = [
    'kowu doesnt really know how to pwn',
    'lukas2511 just pretends to know networking stuff',
    'manf is actually good in math',
    'CSR{N11111111111111C3_W00rK_Y0u_Curvy_B4st4rd}'
]

f = open('frontend/juicy.logs', 'w')
for m in msgs:
    f.write(encrypt(m) + "\n")
