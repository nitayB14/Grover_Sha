# -*- coding: utf-8 -*-
"""
Spyder Editor


-----------------------------
Creator: Nitay B.
Date:    27.12.2025
-----------------------------

Explanation: This adder is implemented as a quantum circuit.
             This is the model for qubits list addition.
             
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
  
    
    
    
def apply_adder(qc, data, nonce, carry_in, carry_out, ancilla, size):
    """
    Explanation: This function apply add of:
                 4 qubits as data 
                 4 qubits as nonce
                 1 qubit as pre carry
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
    size : int
        size of circuit.

    Returns
    -------
    None.

    """
    for i in range(size - 1, -1, -1):
        
        if(i == size - 1):
            add_one_bit_full(qc, data[i], nonce[i], carry_in, carry_out[i], ancilla)
        else:
            add_one_bit_full(qc, data[i], nonce[i], carry_out[i+1], carry_out[i], ancilla)


def build_circuit(qc, data, nonce, carry_in, size):
    """
    Explanation: This function create my circuit
        
    Parameters
    ----------
    qc : QuantumCircuit
        object of quantum circuit.
    data : int
        data.
    nonce : int
        nonce.
    carry_in : int
        informetion from last calculation.
    size : int
        size of circuit.

    Returns
    -------
    None.

    """
    
    """
    #here i need to build the qubits as i want for example 1101 + 0101
    
    #data: 0101
    #nonce: 1100
    #Expected result: 10001
    
    qc.x(data[1])
    qc.x(data[3])
    
    qc.x(nonce[0])
    qc.x(nonce[1])
    
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    
    #example of 2 inputs as h
    #data: H000
    #nonce: H000
    #Expected result: 00000 / 01000 / 10000

    qc.h(data[0])
    qc.h(nonce[0])
    
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """
    
    #example of nonce as H
    #data: 010100
    #nonce: 1H00H1
    #Expected result: 01101 / 01110 / 10001 / 10010
    
    qc.x(data[1])
    qc.x(data[3])
    
    qc.x(nonce[0])
    qc.h(nonce[1])
    qc.h(nonce[4])
    qc.x(nonce[5])
    
        
    
def add_with_carry():
    """
    Explanation:This function responsible for creating the circuit
                                              send parameters for the functio
                                              and show the calculations
    """
    
    size = 6 #size of date/nonce

    #give each qubit place number
    nonce = list(range(size))
    data = list(range(size, size * 2))
    carry_in = (size * 2)
    ancilla = (size * 2) + 1
    carry_out = list(range(ancilla + 1, ancilla + size + 1))
    
    #print(f"""              nonce: {nonce}
    #          data: {data}
    #          carry_in: {carry_in}
    #          ancilla: {ancilla}
    #          carry_out: {carry_out}
    #         ancila + size + 1: {ancilla + size + 1}""")
              
              
    qc = QuantumCircuit(ancilla + size + 1, size + 1)
        
    
    build_circuit(qc, data, nonce, carry_in, size)

    #send parameters to function
    apply_adder(qc, data, nonce, carry_in, carry_out, ancilla, size)
    
    #decide which qubite i want to measure
    list_to_measure = [carry_out[0]]
    list_to_measure.extend(data)
                       
    qc.measure(list_to_measure,list(range(size + 1)))

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
    #plot_histogram(counts)
    #qc.draw('mpl')

add_with_carry()





