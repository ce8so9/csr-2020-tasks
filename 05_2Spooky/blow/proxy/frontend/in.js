var jose = require('node-jose');
var http = require('http');

function encrypt(msg, callback) {
    key = {"crv":"P-256","kty":"EC","x":"2RntSELMcr5qVFmhWZiCKS0NzkZwm3f0dwbXythHYTw","y":"wJgR6ZgJB6lVZFHF-vQ_biOfOAHuTZayzIE55cCbHEM"};
    jose.JWE.createEncrypt({ format: 'compact' }, key).
        update(msg).
        final().
        then(callback);
}

window.encrypt = encrypt;