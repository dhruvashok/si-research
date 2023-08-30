#!/usr/bin/env python3
import serial
import time
import struct
from Crypto.Util.number import bytes_to_long

sigfile = open(f"/Users/dashok/research/attack/out/sigs-{int(time.time())}.csv", "w+")
bridge = serial.Serial("/dev/cu.usbmodem0E23A6701", 115200)

pubkey = bridge.read(65)
assert bridge.read(80) == b"\xff"*80 # make sure we didn't miss anything!
print(f"[***] Board pubkey: {pubkey.hex()}\n")
sigfile.write(f"{pubkey.hex()} JUNK\n")

for _ in range(1500):
    bridge.write(bytes.fromhex("55"))
    start = time.time() # Signature begins here
    data = bridge.read(80)
    end = time.time() # Signature ends here

    # k = data[:32]
    msg = data[:16].hex()
    sig = data[16:]
    # klen = bytes_to_long(k).bit_length()
    elapsed = int((end - start) * 1000000000)
    
    print(f"[+] Msg: {msg}")
    print(f"[+] Sig: {sig.hex()}")
    # print(f"[+] k: {klen}")
    print(f"[*] Total time: {elapsed}\n")
    sigfile.write(f"{msg},{sig[:32].hex()},{sig[32:].hex()},{elapsed}\n")
    time.sleep(0.3)
    # else:
    #     bridge.write(bytes.fromhex("54"))
    #     print(bridge.read(3))
