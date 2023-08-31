## The Premise
The nonce ($k$) used in ECDSA is surprisingly fragile!

Give away the nonce associated with one (1) signature? Bam, you just your private key!

Reuse a nonce across two different signatures? Bam, you just lost your private key [just like the PS3!](https://en.wikipedia.org/wiki/PlayStation_3_homebrew)

Use an LCG to generate nonces? [You will probably lose your private key](https://research.kudelskisecurity.com/2023/03/06/polynonce-a-tale-of-a-novel-ecdsa-attack-and-bitcoin-tears/)!

Use a biased RNG that fixes a couple bits in your nonces? [You will probably lose your private key!](https://cryptopals.com/sets/8/challenges/62.txt)

So maybe you use a good RNG, like `/dev/urandom`, or just ditch random numbers altogether and deterministically generate nonces using something like [RFC 6979](https://datatracker.ietf.org/doc/html/rfc6979)

Good job! But wait, how did you implement elliptic curve point multiplication? If you're like 99% of users, you probably didn't. But how did the library that you used implement it?

Some implementations, especially the most efficient/naive approaches, use a loop where the number of iterations is dependent upon the bit length of the nonce! As a result, the amount of time it takes to compute a signature will depend on the bit length of nonce, and so it will take *longer* to compute a signature with a nonce that has a longer bit length. Using this correlation, we may be able to figure out the bit length of the nonce used during signing through the amount of time it takes to compute the signature. You might be wondering why it matters if we know the bit length of the nonce during signing. Well, if we know this information for enough signatures, **we can recover the private key**.

This attack, known as [Minerva](https://minerva.crocs.fi.muni.cz/), is further progress in a long chain of cryptanalysis that uses Lattice Techniques :tm: to pwn ECDSA. Up until now, however, it was thought that one would need local access to a vulnerable device in order to perform this attack. This is because an attacker needs to obtain sufficiently many accurate timing measurements, usually through some form of power analysis, in order for the attack to work. 

However, some recent findings have extended the scope of Minerva! [This paper](https://eprint.iacr.org/2023/923.pdf) uses the **power LED** of a device as a side channel. Besides being quite impressive in its own right as a completely new frontier of cryptanalysis, it also enables us to now **remotely** obtain the timing measurements needed for Minerva. This was demonstrated in the above paper on video-based cryptanalysis, and our goal is going to be to reproduce the results.

## The Setup
We're going to be using a [pretty basic ARM Cortex-M4 based microcontroller](https://www.ti.com/tool/EK-TM4C123GXL) released by TI, pictured below:

![alt text](https://www.ti.com/content/dam/ticom/images/products/ic/processors/evm-boards/ek-tm4c123gxl-angled.png:large)

The board will be running firmware that uses the BearSSL implementation of ECDSA, which is actually very constant-time and secure. However, for the sake of the experiment, we're going to introduce a mild delay that's linearly correlated with the bit length of the nonce. This delay will be enough to introduce a timing difference of ~2ms per bit. If you were to stare at the board, you probably wouldn't immediately notice the timing difference, but a camera likely will.

