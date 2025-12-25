from qiskit import *
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram


state = [0,1,2,3,4,5]

carry_out = 6

value = [7,8,9,10,11,12]

carry_in = 13

ancilla = 14






def quantum_hash_oracle(qc):
    step_one_xor(qc)
    
    step_two_rotate(qc)
    
    step_three_adder(qc)
    
    reset_qubits(qc)
    
    step_three_adder(qc)
    
    reset_qubits(qc)
    
    step_two_rotate(qc)
    
    step_one_xor(qc)
    
    
def reset_qubits(qc):
    qc.reset(ancilla)
    qc.reset(carry_in)
    qc.reset(carry_out)
    
def step_one_xor(qc):
    #qc.cx(value, state)
    for i in range(6):
        qc.cx(i + value[0], i + state[0])
    
    
def step_two_rotate(qc):
    
    # --- מחזור 1: q6 → q8 → q10 ---
    qc.swap(state[0], state[4])
    qc.swap(state[0], state[2])
    
    # --- מחזור 2: q7 → q9 → q11 ---
    qc.swap(state[1], state[5])
    qc.swap(state[1], state[3])
    
def step_three_adder(qc):
    
    
    for i in range(6):
        qc.reset(ancilla)
        qc.reset(carry_in)
        qc.swap(carry_in, carry_out)
        
        add_one_bit_full(qc, state[5 - i], value[5 - i], carry_in, carry_out, ancilla)

        
        
        
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
        
    
    


    

def encoding(qc, input_bits):
    for i in range(6):
        if input_bits[i] == '1':
            qc.x(i)
            
    
    """
    for i in range(6, 12):
        if input_bits[i] == '1':
            qc.x(i + 1)
    """
    for i in range(6, 12):
        qc.h(i + 1)
    
    

def print_measurements(qc, state):
    #qc.measure([0,1,2,3,4,5,7,8,9,10,11,12], [0,1,2,3,4,5,6,7,8,9,10,11])
    qc.measure(state, state)
    
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



def main():
    
    qc = QuantumCircuit(15, 6)
    
    value_str = "000111"
    state_str = "010101"
    encoding(qc, state_str + value_str)
    
    
    quantum_hash_oracle(qc)
    
    
    print_measurements(qc, state)
    
    
main()