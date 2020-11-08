from cryptography.exceptions import InvalidSignature
import logging as log
from jwcrypto import jwk, jwe
from flask import Flask, request, jsonify


priv = {
    "crv": "P-256",
    "d": "29FABiRtn3-GOQNEH3jTZj8KywLb38fHQAtfvWaXSC4",
    "kty": "EC",
    "size": 2048,
    "x": "2RntSELMcr5qVFmhWZiCKS0NzkZwm3f0dwbXythHYTw",
    "y": "wJgR6ZgJB6lVZFHF-vQ_biOfOAHuTZayzIE55cCbHEM"
}
private_key = jwk.JWK()
private_key.import_key(**priv)

app = Flask(__name__)


@app.route('/submit', methods=['POST'])
def login():
    jwetoken = jwe.JWE()
    try:
        jwetoken.deserialize(request.data.decode(), key=private_key)
        # payload = jwetoken.payload
        # print(payload)
        return jsonify(status='success')
    except InvalidSignature:
        return jsonify(status='bad mac'), 420
    except Exception as ex:
        log.error(request.data)
        log.error(repr(ex))
        return jsonify(status="internal error"), 500

    return jsonify(status='bad request'), 400


if __name__ == '__main__':
    app.run()
