import requests
import time

FLAG = str(open("flag.txt", "r").read())

while True:
    try:
        requests.post("http://server/", {"echo":FLAG}, timeout=1)
    except:
        pass #server not up yet :()
    time.sleep(1)