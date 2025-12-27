from qiskit import *
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import MCXGate
from qiskit.circuit.library import ZGate



state = [0,1,2,3,4,5]

carry_out = 6

value = [7,8,9,10,11,12]

carry_in = 13

ancilla = 14

groover_ancilla = 15






def quantum_hash_oracle(qc):
    print("starting")
    step_one_xor(qc)
    print("xor")    
    
    step_two_rotate(qc)
    print("rotation")
    
    """
    apear to have a problem - probably by trying to create reset
    
    """
    #step_three_adder(qc)
    #print("adder")
    
    """
    reset_qubits(qc)
    print("reset")
    step_three_adder(qc)
    print("adder")
    reset_qubits(qc)
    print("reset")
    step_two_rotate(qc)
    print("rotate")
    step_one_xor(qc)
    print("xor")
    qc.barrier()
    """
    
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
        
    
    


def flip_oracle(qc):
    
    
    
    qc.x(state[0])
    qc.x(state[1])
    qc.x(state[2])
    qc.x(state[3])
    qc.x(state[4])
    
    qc.mcx([state[0],state[1], state[2], state[3], state[4]], groover_ancilla)

    #qc.ccx(state[0], state[1], groover_ancilla)
    qc.z(groover_ancilla)
    #qc.ccx(state[0], state[1], groover_ancilla)
    qc.mcx([state[0],state[1], state[2], state[3], state[4]], groover_ancilla)

    qc.x(state[4])
    qc.x(state[3])
    qc.x(state[2])
    qc.x(state[1])
    qc.x(state[0])
    

    
    qc.barrier()
    
    
    

def encoding(qc, input_bits):
    
    
    for i in range(6):
        if input_bits[i] == '1':
            qc.x(i)
            
    
    """
    for i in range(6, 12):
        if input_bits[i] == '1':
            qc.x(i + 1)
    
    """
    for i in range(7, 13):
        qc.h(i)
        
    qc.barrier()
    
    
    
def uncompute(qc, input_bits):
    
    for i in range(6):
        qc.reset(i)
    
    for i in range(6):
        if input_bits[i] == '1':
            qc.x(i)
            
    qc.barrier()
            
            
def diffuser(qc):
    control_qubits = [value[0], value[1], value[2], value[3], value[4]]
    target_qubit = value[5] # One target qubit
    
    
    qc.h(value)
    qc.x(value)

    qc.h(target_qubit)
    qc.append(ZGate().control(5), control_qubits + [target_qubit])
    qc.h(target_qubit)
    
    qc.x(value)
    qc.h(value)
    
    """
    for i in range(6):
        qc.h(value[i])
        
    for i in range(6):
        qc.x(value[i])
        
    
    qc.ccx(value[0],value[1],ancilla)
    qc.ccx(value[2],value[3],carry_in)
    qc.ccx(ancilla, carry_in, carry_out)
    qc.ccx(value[4],carry_out ,value[5])
    
    qc.h(value[5])

    qc.z(value[5])

    qc.h(value[5])

    qc.ccx(value[4],carry_out ,value[5])
    qc.ccx(ancilla, carry_in, carry_out)
    qc.ccx(value[2],value[3],carry_in)
    qc.ccx(value[0],value[1],ancilla)

    
    for i in range(6):
        qc.x(value[i])
    
    for i in range(6):
        qc.h(value[i])
    """ 
    

    qc.barrier()

def print_measurements(qc, state):
    #qc.measure([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    #qc.measure([0,1,2,3,4,5,15],[0,1,2,3,4,5,6])
    #qc.measure([7,8,9,10,11,12,15], [0,1,2,3,4,5,6])
    #qc.measure(state, state)
    qc.measure(value, state)
    
    
    qc.draw(output="mpl")

    
    
    simulation = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, simulation)
    
    #run the simulation
    job = simulation.run(transpiled_qc, shots=4096)
    #get result
    result = job.result()
    counts = result.get_counts()
    
    #print the results
    #plot_histogram(counts)
    flipped_counts = {key[::-1]: value for key, value in counts.items()}
    plot_histogram(flipped_counts)

    print(flipped_counts)



def main():
    
    qc = QuantumCircuit(16, 6)
    
    value_str = "000101"
    state_str = "010101"
    encoding(qc, state_str + value_str)
    
    for i in range(1):
        quantum_hash_oracle(qc)
    
        flip_oracle(qc)
    
        uncompute(qc, state_str + value_str)
    
        diffuser(qc)
    
    print_measurements(qc, state)
    
    
main()