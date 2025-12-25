
from qiskit import *
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram



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

    # ✅ 2. עכשיו מחושבים carry → נחשב את הסכום
    # sum = state XOR value XOR pre_carry
    qc.cx(value, state)
    qc.cx(pre_carry, state)

    
    
    
def four_qubits_adder(qc, state, value, carry_in, carry_out, ancilla):

    add_one_bit_full(qc, state[3], value[3], carry_in, carry_out, ancilla)
    
    qc.reset(ancilla)
    qc.reset(carry_in)
    qc.swap(carry_in, carry_out)
     
    add_one_bit_full(qc, state[2], value[2], carry_in, carry_out, ancilla)
    
    qc.reset(ancilla)
    qc.reset(carry_in)
    qc.swap(carry_in, carry_out)
    
    add_one_bit_full(qc, state[1], value[1], carry_in, carry_out, ancilla)
    
    qc.reset(ancilla)
    qc.reset(carry_in)
    qc.swap(carry_in, carry_out)
    
    add_one_bit_full(qc, state[0], value[0], carry_in, carry_out, ancilla)

    
    
def add_with_carry():
    
    
    qc = QuantumCircuit(11, 5)

    value = [0,1,2,3]
    
    carry_out = 4
    
    state = [5,6,7,8]
    
    carry_in = 9
    
    ancilla = 10
    
    
    
    """
    #here i need to build the qubits as i want for example 1101 + 0101
    
    #state: 0101
    #value: 1010
    #Expected result: 1111
    
    qc.x(value[0])
    qc.x(value[2])
    
    qc.x(state[1])
    qc.x(state[3])
    
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    
    #another example:
    #state: 1001
    #value: 1111
    #Expected result: 11000

    
    qc.x(value[0])
    qc.x(value[1])
    qc.x(value[2])
    qc.x(value[3])
    
    qc.x(state[3])
    qc.x(state[0])
    
    
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    
    
    #another example with 2 possible outputs(one input with h)
    #state: 1010
    #value: 00H0
    #Expected result: 01010 / 01100

    qc.x(state[0])
    qc.x(state[2])
    
    qc.h(value[2])
    
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """
    #example of 2 inputs as h
    #state: H000
    #value: H000
    #Expected result: 00000 / 01000 / 10000

    qc.h(state[0])
    qc.h(value[0])
    
    
    four_qubits_adder(qc, state, value, carry_in, carry_out, ancilla)
    
   
    qc.measure([4,5,6,7,8],[0,1,2,3,4])

    
    #qc.draw('mpl')
    simulation = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, simulation)
    
    #run the simulation
    job = simulation.run(transpiled_qc, shots=1024)
    #get result
    result = job.result()
    counts = result.get_counts()
    
    #print the results
    #plot_histogram(counts)\
    flipped_counts = {key[::-1]: value for key, value in counts.items()}

    print(flipped_counts)
    

add_with_carry()





