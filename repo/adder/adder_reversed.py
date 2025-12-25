
from qiskit import *
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram


"""
explanation:
This function take 3 qubits(pre_carry, state, value), and calculate add
At the end the function reset ancilla and put the output in 2 qubits
state - the answer
carry_out - for the next row of adding
"""
def add_one_bit_full(qc: QuantumCircuit, state: int, value: int, pre_carry: int, carry_out: int, ancilla: int):
    # 💡 1. קודם מחשבים carry: majority(state, value, pre_carry)

    # temp = state AND value
    qc.ccx(state, value, ancilla)
    
    # carry_out = state AND pre_carry
    qc.ccx(value, pre_carry, carry_out)

    # carry_out ^= value AND pre_carry
    qc.ccx(state, pre_carry, carry_out)

    # carry_out ^= temp (from ancilla)
    qc.cx(ancilla, carry_out)

    #reset ancilla
    qc.ccx(state, value, ancilla)

    #calculate carry
    # sum = state XOR value XOR pre_carry
    qc.cx(value, state)
    qc.cx(pre_carry, state)



"""
explanation: 
This function is the reverse of add_one_bit_full
"""
def one_bit_reverse(qc: QuantumCircuit, state: int, value: int, pre_carry: int, carry_out: int, ancilla: int):
    
    qc.cx(pre_carry, state)
    qc.cx(value, state)
         
    qc.ccx(state, value, ancilla)

    qc.cx(ancilla, carry_out)

    qc.ccx(state, pre_carry, carry_out)

    qc.ccx(value, pre_carry, carry_out)

    qc.ccx(state, value, ancilla)

    
    
"""
Explanation:
    This function take the size of each bytes as we define it (size of 1/2/3...),
    and function as the brain who send each qubit to the add_one_bit_full
"""
def adder(qc, state, value, carry_in, carry_out, ancilla, size):
    
    for i in range(size - 1, -1, -1):
        
        if(i == size - 1):
            add_one_bit_full(qc, state[i], value[i], carry_in, carry_out[i], ancilla)
        else:
            add_one_bit_full(qc, state[i], value[i], carry_out[i+1], carry_out[i], ancilla)



"""
Explanation:
    This function the reverse of adder
"""
def adder_reverse(qc, state, value, carry_in, carry_out, ancilla, size):
    
    for i in range(size):
        if(i == size - 1):
            one_bit_reverse(qc, state[i], value[i],  carry_in, carry_out[i], ancilla)
        else:
            one_bit_reverse(qc, state[i], value[i], carry_out[i+1], carry_out[i], ancilla)


"""
Explanation:
    This function create the circuit we want
    changes the bits as we wish
"""
def build_circuit(qc, state, value, carry_in, size):
    
    
    qc.x(state[0])
    qc.x(state[4])
    qc.h(value[0])
    qc.x(value[3])
    #qc.x(carry_in)
    

  


"""
Explanation:
    this function is the main, it create the size of circuit, send the circuit to the adders
    print the output, and draw it.
"""
def add_with_carry():
    
    size = 6
    value = list(range(size))
    state = list(range(size, size * 2))
    carry_in = (size * 2)
    ancilla = (size * 2) + 1
    carry_out = list(range(ancilla + 1, ancilla + size + 1))
    
    
    #build the circuit          
    qc = QuantumCircuit(ancilla + size + 1, size + 1)

    #change the bits
    build_circuit(qc, state, value, carry_in, size)
    
    #send the to adder
    adder(qc, state, value, carry_in, carry_out, ancilla, size)
    
    #create berrier for better look and debug
    qc.barrier()
    
    #reverse the function
    adder_reverse(qc, state, value, carry_in, carry_out, ancilla, size)
    
    
    list_to_measure = [carry_out[0]]
    list_to_measure.extend(state)
                       
    qc.measure(list_to_measure, list(range(size + 1)))
    
    simulation = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, simulation)
    
    #run the simulation
    job = simulation.run(transpiled_qc, shots=1024)
    #get result
    result = job.result()
    counts = result.get_counts()
    
    #qiskit print reversed so we reversed it again
    #print the results
    flipped_counts = {key[::-1]: value for key, value in counts.items()}

    print(flipped_counts)
    #plot_histogram(counts)
    qc.draw('mpl')

add_with_carry()





