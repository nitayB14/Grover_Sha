# Tests & Artifacts

This folder contains run artifacts for this version:
- `artifacts/counts_histogram.png` - measurement distribution (shots vs. outcomes)
- `artifacts/counts_list.png` - top measured candidates as a list
- `artifacts/circuit.png` - rendered Grover circuit for this version
- `artifacts/validation.png` - classical validation that the selected candidate satisfies the prefix condition

Multiple validation images correspond to different candidate nonces
obtained from repeated runs or top measurement outcomes.

To reproduce: run `grover.py`, take the most frequent candidate, and validate it using `hash_classic.py`.
