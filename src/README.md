# Source Code Structure

This directory contains the core implementations of Grover's algorithm
with a reversible hash-based oracle, organized by qubit count and version.

## Directory Overview

- `v1_6_qubits/`
  - Grover search over a 6-qubit register (64 states)
- `v2_8_qubits/`
  - Extended implementation over an 8-qubit register (256 states)

Each version is self-contained and follows the same logical structure.

## File Structure (per version)

- `grover.py`
  - Constructs and executes the full Grover circuit
- `hash_classic.py`
  - Classical reference implementation of the hash function

## Execution Flow

The program operates as follows:

1. Verify that the `data` string is identical in both the quantum and classical files.
   You may change `data` to test different inputs, but it must be updated in **both** files.
   If the values differ, the quantum result cannot be validated against the classical reference.

2. Run the `grover.py` script.
   This file constructs and executes the full Grover circuit.

3. Note that the `flip_oracle` function encodes the target prefix condition
   (i.e., the number of leading zeros being checked), and is currently defined over:
   - 4 prefix-condition qubits in `v1_6_qubits`
   - 5 prefix-condition qubits in `v2_8_qubits`

   These qubits define the oracle constraint and are not part of the search register.

4. After execution, inspect the measurement results and identify the states
   that appear with the highest frequency.

   **Note:** Due to the probabilistic nature of quantum measurement,
   the correct candidate is expected to appear with higher frequency,
   not necessarily as a single deterministic outcome.

5. Take the most frequently observed candidate and pass it as the `nonce` input to the
   classical reference implementation (`hash_classic.py`).

6. In the `main` function of `hash_classic.py`, replace the nonce value with
   the candidate obtained from the quantum run and verify whether it satisfies
   the target prefix condition (e.g., a leading zero prefix).

## Design Notes

- The oracle is implemented using fully reversible logic.
- Phase kickback is induced via an ancilla qubit.
- The diffuser performs inversion about the mean using a standard construction.