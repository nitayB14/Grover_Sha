# -*- coding: utf-8 -*-
"""
Spyder Editor


-----------------------------
Creator: Nitay B.
Date:    27.12.2025
-----------------------------

Explanation: This adder is implemented as a quantum circuit.
             This is the base model for qubits list addition.
"""

from qiskit import *
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

###################################################################################################################

def add_one_bit_full(qc: QuantumCircuit, data: int, nonce: int, pre_carry: int, carry_out: int, ancilla: int):
    """
    Explanation: This function apply add of 3 qubits 
                 (data + nonce + pre carry)
        
    Parameters
    ----------
    qc : QuantumCircuit
        object of quantum circuit.
    data : int
        data.
    nonce : int
        nonce.
    pre_carry : int
        informetion from last calculation.
    carry_out : int
        information for next calculation.
    ancilla : int
        help qubit.

    Returns
    -------
    None.

    """
    
    
    # ancilla(temp) = data AND nonce
    qc.ccx(data, nonce, ancilla)

    # carry_out = data AND pre_carry
    qc.ccx(nonce, pre_carry, carry_out)

    # carry_out ^= nonce AND pre_carry
    qc.ccx(data, pre_carry, carry_out)

    # carry_out ^= ancilla(temp)
    qc.cx(ancilla, carry_out)

    # sum = data XOR nonce XOR pre_carry
    qc.cx(nonce, data)
    qc.cx(pre_carry, data)
    
###################################################################################################################    
  
def add_with_carry():
    """
    Explanation:This function responsible for creating the circuit
                                              send parameters for the functio
                                              and show the calculations
    """
    
    qc = QuantumCircuit(5, 2)

    #give each qubit place number
    data = 0
    nonce = 1
    pre_carry = 2
    carry_out = 3
    ancilla = 4

    #         nonce  +  data   + pre_carry
    #example:   0    +    1    +    1
    qc.x(data)
    #qc.x(nonce)
    qc.x(pre_carry)
    
    
    
    """
      2            1         0                 0             2
    pre carry    nonce     data      ->      data        carry out
      0           0         0                 0             0 
      0           0         1                 1             0
      0           1         0                 1             0
      0           1         1                 0             1
      1           0         0                 1             0 
      1           0         1                 0             1
      1           1         0                 0             1
      1           1         1                 1             1
    """
        
    #send parameters to function
    add_one_bit_full(qc, data, nonce, pre_carry, carry_out, ancilla)

    #decide which qubite i want to measure
    qc.measure([3,0],[0,1])
    
    #create quantum beckend
    simulation = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, simulation)
    
    #run the simulation
    job = simulation.run(transpiled_qc, shots=1024)
    #get result
    result = job.result()
    counts = result.get_counts()
    
    #qiskit print reversed so we reversed it again
    #print the results
    flipped_counts = {key[::-1]: nonce for key, nonce in counts.items()}

    print(flipped_counts)
    
###################################################################################################################  
    
add_with_carry()

