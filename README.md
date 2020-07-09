# Plonk_TH
This repo contains my from-scratch python implementation of the PLONK protocol (zk- version) as described in the [PLONK paper](https://eprint.iacr.org/2019/953) from p.27 and an accompanying tutorial.

The PLONK implementation consists of setup.py which contains the setup phase, prover.py which contains the prover algorithm and verifier.py with the verifier algorithm. Run plonk.py for a testcase which puts everything together using the example problem
from [Vitalik's blog](https://vitalik.ca/general/2019/09/22/plonk.html) on PLONK. I have developed this for (self) educational purposes, it is not secure or efficient.

The accompanying tutorial plonk_tutorial.ipynb is WIP and contains essentially the same code but explains the steps in some detail.

Critique, contributions and suggestions are welcome.
