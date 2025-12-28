# Reversible Hash Oracle with Grover's Algorithm

A quantum implementation of Grover's search using a structured, reversible hash-based oracle,
demonstrating amplitude amplification beyond trivial state-marking examples.

## Overview

This project explores the integration of a reversible hash function into Grover’s algorithm.
Instead of directly marking a known target state, the oracle computes a hash-like condition
and uses ancilla-based phase kickback to mark valid preimages.

The implementation is fully reversible and designed for clarity, correctness, and extensibility.

## Project Structure

- `src/` - Core implementations
  - `v1_6_qubits/` - Grover search over 64 states
  - `v2_8_qubits/` - Extension to 256 states
- `experiments/` - Isolated tests (adder, diffuser, oracle components)
- `docs/` - Technical write-up and explanations

## Requirements

- Python 3.10+ (tested with Python 3.12.7)
- See `requirements.txt` for dependencies

## Usage

Run the 6-qubit Grover example:
```bash
python src/v1_6_qubits/grover.py
