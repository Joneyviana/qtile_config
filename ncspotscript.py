from subprocess import *
import os
import time
(r1, w1) = os.pipe2(0) 
(r2, w2) = os.pipe2(0) 

process = Popen(["nc -U ~/.cache/ncspot/ncspot.sock"], stdin=r1, stdout=w2, encoding='utf8', shell=True)
outfile = os.fdopen(w1, 'w', buffering=1)
time.sleep(10)
print("pause", file=outfile)
print("move down", file=outfile)
print("play", file=outfile)
process.wait()
