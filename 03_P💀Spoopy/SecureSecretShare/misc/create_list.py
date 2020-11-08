import hashlib

pws = [x.strip() for x in open("pws.txt").readlines()]

for pw in pws:
    print('db.secrets.insertOne({id: "%s", secret: "%s"});' % (hashlib.sha256(pw.encode()).hexdigest(), pw))
