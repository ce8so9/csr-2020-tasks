TinyDTLS Exploit
================

The included dump was created using the create_dump.sh script (needs root for tcpdump), which checkouts the current master branch.

To verify the attack worked, you can check the values in the dump match the ones in the scripts.

To do the attack yourself, you have to:

- Change the variable `nonce_check` in `brute_nonce.c` to the least significant 28 bytes
of the `Random` message in the ServerHello mesage
- Copy the file brute_nonce.c into the `tinydtls/tests` folder
- compile it with `make brute_nonce`
- run it, it will output a hex encoded value of the secret scalar used
- replace the variable `SERVER_SECRET` in `decrypt_dtls.py` with the outputted secret scalar
- replace the variable `ENCRYPTED_CONTENT` with the encrypted content you wish to decrypt
- replace the variables `client_random`, `server_random` and `client_pub` (public key) with the corresponding public values of the communication
- run the script `decrypt_dtls.py` with Python 3, 
- The script outputs the master secret and the decrypted plain text
this requires tlslite, ecdsa and pycrptodome to be installed (`pip3 install pycryptodome tlslite ecdsa`)

The code is a bit messy. 
If you need a cleaner version for verification, I can clean it up by the end of the week. 