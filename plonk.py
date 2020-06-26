import sys
import numpy as np
from setup import setup_algo
from prover import prover_algo
from verifier import verifier_algo


def permute_idices(circuit):
    # This function takes an array "circuit" of arbitrary values and returns an
    # array with shuffles the indices of "circuit" for repeating values
    size = len(circuit)
    permutation = [i + 1 for i in range(size)]
    for i in range(size):
        for j in range(i+1, size):
            if circuit[i] == circuit[j]:
                place_holder = permutation[i]
                permutation[i] = permutation[j]
                permutation[j] = place_holder
                break
        return permutation


def test_plonk():
    # We want to prove that we know x so that: x**3 + x + 5 == 35
    # A solution to this is x = 3. We manually construct a circuit that
    # represents the equation using these gates:
    #    	 L	R	M	O	C
    # add	 1	1	0	-1	0
    # mul	 0	0	1	-1	0
    # const	 0	1	0	0	-const
    # public 0	1	0	0	0

    # The computation consists of 6 gates. We allow the value 35 to be a public
    # input instead of a constant.
    # a = [x    , x * x    , x * x * x    , 1,  1, x * x * x + x]
    # b = [x    , x        , x            , 5, public(35), 5]
    # c = [x * x, x * x * x, x + x * x * x, 5, public(35), public(35)]
    # i.e. [mul, mul, add, const, public, add]

    # PLONK relies on permutations of connected wire indices. To get this
    # permutation, we first write down the circuit with all wire values.
    circuit = ["x"    , "x * x"        , "x * x * x"     , "1" ,  "1"                   , "x * x * x + x"      , "empty1", "empty2",
               "x"    , "x"            , "x"             ,  "5", "public(35)"           , "5"                   , "empty3", "empty4",
               "x * x", "x * x * x"    , "x * x * x + x" ,  "5", "public(35)"           , "public(35)"          , "empty5", "empty6"]

    # We take the circuit and look at entries that repeat somewhere. If we find
    # a repetition, we swap the indices. E.g. circuit[0] = circuit[8] so we set
    # permutation[0] = 8 and permutation[8] = 0. Note that permutation[8] will
    # be swapped again later on because there are more repetitions of its value
    permutation = permute_idices(circuit)

    # We can provide public input 35. For that we need to specify the position
    # of the gate in L and the value of the public input in p_i
    L = [4]
    p_i = 35

    # We are constructing a matrix that represents the gates using these
    # building blocks:
    add =          np.array([1, 1, 0, -1, 0])
    mul =          np.array([0, 0, 1, -1, 0])
    const5 =       np.array([0, 1, 0, 0, -5])
    public_input = np.array([0, 1, 0, 0, 0])
    empty =        np.array([0, 0, 0, 0, 0])

    # The number of gates is 6 right now but we need to have a number thats a
    # power of two. Therefore I add two empty gates. This makes it easier to
    # track whats happening.
    gates_matrix = np.array([mul, mul, add, const5,
                            public_input, add, empty, empty])
    n = len(gates_matrix)
    gates_matrix = gates_matrix.transpose()

    # To get the witness, the prover applies his private input x=3 to the
    # circuit and writes down the value of every wire.
    witness = [3, 9, 27, 1, 1, 30, 0, 0,
               3, 3, 3, 5, 35, 5, 0, 0,
               9, 27, 30, 5, 35, 35, 0, 0]

    # We start with a setup that computes the trusted setup and does some
    # precomputation
    CRS, Qs, p_i_poly, perm_prep, verifier_prep = setup_algo(gates_matrix,
                                                             permutation,
                                                             L,
                                                             p_i)
    # The prover calculates the proof
    proof_SNARK, u = prover_algo(witness, CRS, Qs, p_i_poly, perm_prep)

    # Verifier checks if proof checks out
    verifier_algo(proof_SNARK,
                  n,
                  p_i_poly,
                  verifier_prep,
                  perm_prep[2])


test_plonk()
