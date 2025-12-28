"""
Spyder Editor


-----------------------------
Creator: Nitay B.
Date:    27.12.2025
-----------------------------

Explanation: Full implementation of Grover's search algorithm on a 6-qubit register (64 states).

The circuit includes explicit construction of:
- Reversible oracle logic
- Phase kickback using an ancilla qubit
- Grover diffusion operator
- Amplitude amplification and measurement statistics

Designed for educational and research-level demonstration.
"""

from qiskit import *
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import MCXGate
from qiskit.circuit.library import ZGate


size = 6
nonce = list(range(size))
data = list(range(size, size * 2))
carry_in = (size * 2)
ancilla = (size * 2) + 1
carry_out = list(range(ancilla + 1, ancilla + size + 1))
grover_ancilla = carry_out[size-1] + 1


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
    
    #reset ancilla
    qc.ccx(data, nonce, ancilla)
    
    # sum = data XOR nonce XOR pre_carry
    qc.cx(nonce, data)
    qc.cx(pre_carry, data)
    
###################################################################################################################    
  


def one_bit_reverse(qc: QuantumCircuit, data: int, nonce: int, pre_carry: int, carry_out: int, ancilla: int):
    """
    Explanation: This function apply the reversible add of 3 qubits 
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
    qc.cx(pre_carry, data)
    qc.cx(nonce, data)
         
    qc.ccx(data, nonce, ancilla)

    qc.cx(ancilla, carry_out)

    qc.ccx(data, pre_carry, carry_out)

    qc.ccx(nonce, pre_carry, carry_out)

    qc.ccx(data, nonce, ancilla)

###################################################################################################################
    

def adder(qc, data, nonce, carry_in, carry_out, ancilla, size):
    """
    Explanation: This function apply add of:
                 X qubits as data 
                 X qubits as nonce
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


###################################################################################################################


def adder_reverse(qc, data, nonce, carry_in, carry_out, ancilla, size):
    """
    Explanation: This function apply reversible add of:
                 X qubits as data 
                 X qubits as nonce
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
    for i in range(size):
        if(i == size - 1):
            one_bit_reverse(qc, data[i], nonce[i],  carry_in, carry_out[i], ancilla)
        else:
            one_bit_reverse(qc, data[i], nonce[i], carry_out[i+1], carry_out[i], ancilla)

###################################################################################################################


def quantum_hash_oracle(qc):
    """
    Explanation: This function apply the oracle:

    Parameters
    ----------
    qc : QuantumCircuit
        object of quantum circuit.
    """
    step_one_xor(qc)
    #print("xor")    
    
    step_two_rotate(qc)
    #print("rotation")
    
    adder(qc, data, nonce, carry_in, carry_out, ancilla, size)
    #print("adder")
    
    step_two_rotate(qc)
    #print("rotate")
    
    step_one_xor(qc)
    #print("xor")
    qc.barrier()
    
###################################################################################################################


def quantum_hash_oracle_uncompute(qc):
    """
    Explanation: This function apply the reversible oracle:

    Parameters
    ----------
    qc : QuantumCircuit
        object of quantum circuit.
    """

    step_one_xor_uncompute(qc)
    #print("uncompute xor")
    
    step_two_rotate_uncompute(qc)
    #print("uncompute shift")
    
    adder_reverse(qc, data, nonce, carry_in, carry_out, ancilla, size)
    #print("uncompute adder")

    step_two_rotate_uncompute(qc)
    #print("uncompute shift")
    
    step_one_xor_uncompute(qc)
    #print("uncompute xor")
    
    
    
def step_one_xor(qc):
    """
    Explanation: This function apply xor:

    Parameters
    ----------
    qc : QuantumCircuit
        object of quantum circuit.
    """
    for i in range(size):
        qc.cx(nonce[i], data[i])
    
    
def step_one_xor_uncompute(qc):
    """
    Explanation: This function apply the reversible xor:

    Parameters
    ----------
    qc : QuantumCircuit
        object of quantum circuit.
    """
    for i in range(size - 1, -1, -1):
        qc.cx(nonce[i], data[i])


def step_two_rotate(qc):
    """
    Explanation: This function apply shift:

    Parameters
    ----------
    qc : QuantumCircuit
        object of quantum circuit.
    """
    qc.swap(data[0], data[4])
    qc.swap(data[0], data[2])
    
    qc.swap(data[1], data[5])
    qc.swap(data[1], data[3])
    
    

def step_two_rotate_uncompute(qc):
    """
    Explanation: This function apply reversible shift:

    Parameters
    ----------
    qc : QuantumCircuit
        object of quantum circuit.
    """
    qc.swap(data[1], data[3])
    qc.swap(data[1], data[5])
    qc.swap(data[0], data[2])
    qc.swap(data[0], data[4])


def flip_oracle(qc):
    """
    Explanation: Conditional ancilla flip used to induce phase kickback on the marked state.
    
    Parameters
    ----------
    qc : QuantumCircuit
        object of quantum circuit.
    """
    qc.x(data[0])
    qc.x(data[1])
    qc.x(data[2])
    qc.x(data[3])
    
    qc.mcx([data[0],data[1], data[2], data[3]], grover_ancilla)
    qc.z(grover_ancilla)
    qc.mcx([data[0],data[1], data[2], data[3]], grover_ancilla)

    qc.x(data[3])
    qc.x(data[2])
    qc.x(data[1])
    qc.x(data[0])
    
    """
    5 qubit starting with 0
    
    qc.x(data[0])
    qc.x(data[1])
    qc.x(data[2])
    qc.x(data[3])
    qc.x(data[4])
    
    
    qc.mcx([data[0],data[1], data[2], data[3], data[4]], grover_ancilla)
    qc.z(grover_ancilla)
    qc.mcx([data[0],data[1], data[2], data[3], data[4]], grover_ancilla)

    qc.x(data[4])
    qc.x(data[3])
    qc.x(data[2])
    qc.x(data[1])
    qc.x(data[0])
    """
    
    qc.barrier()
    
    


            
       
def diffuser(qc):
    """
    Explanation: Applies the Grover diffusion operator, reflecting the state about the uniform superposition.
    
    Parameters
    ----------
    qc : QuantumCircuit
        object of quantum circuit.
    """

    control_qubits = [nonce[0], nonce[1], nonce[2], nonce[3], nonce[4]]
    target_qubit = nonce[5] # One target qubit
    
    
    qc.h(nonce)
    qc.x(nonce)

    qc.h(target_qubit)
    qc.append(ZGate().control(5), control_qubits + [target_qubit])
    qc.h(target_qubit)
    
    qc.x(nonce)
    qc.h(nonce)
    

    qc.barrier()



def print_measurements(qc, nonce):
    """
    Explanation: This function measure and print the output
    Parameters
    ----------
    qc : QuantumCircuit
        object of quantum circuit.
    nonce : int
        nonce.
    """

    list_to_measure = nonce
                       
    #decide which qubite i want to measure
    qc.measure(list(range(size*2)), list(range(size*2)))
    
    
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
    sorted_flipped_counts = dict(sorted(flipped_counts.items(), key=lambda item: item[1], reverse=True))
    
    
    for k, v in sorted_flipped_counts.items():
        print(f"nonce: {k[:size]}: {v}")
    
    
    plot_histogram(counts)
    #draw circuit
    qc.draw('mpl')
    
    #print(flipped_counts)

    

def encoding(qc, input_bits):
    """
    Explanation: This function create my circuit
        
    Parameters
    ----------
    qc : QuantumCircuit
        object of quantum circuit.
    input_bits : string
        data + nonce.

    Returns
    -------
    None.
    """

    #encode data
    for j in range(data[0], (data[size-1] + 1)):
        if input_bits[j] == '1':
            qc.x(data[j - size])
    
    
    #encode nonce as Hadamard
    for i in range(nonce[0], (nonce[size-1] + 1)):
        qc.h(nonce[i])
      
    """
    for i in range(nonce[0], (nonce[size-1] + 1)):
        if input_bits[i] == '1':
            qc.x(nonce[i])           
    
    """

    qc.barrier()
    
    

def main():
    
    """
    Explanation:This function responsible for creating the circuit
                                              send parameters for the function
                                              call oracle and diffuser
                                              and show the calculations
    """

    qc = QuantumCircuit(grover_ancilla + 1, size*2)

    
    nonce_str = "000000"
    data_str = "101001"
    
    #encode data + nonce to qubits
    encoding(qc, nonce_str + data_str )
    
    #starting build the oracle
    quantum_hash_oracle(qc)
    flip_oracle(qc)
    quantum_hash_oracle_uncompute(qc)
    
    #call the diffuser
    diffuser(qc)
    
    #print measures
    print_measurements(qc, data)
    
    
main()