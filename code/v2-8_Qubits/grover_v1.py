from qiskit import *
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import MCXGate
from qiskit.circuit.library import ZGate


size = 6
value = list(range(size))
state = list(range(size, size * 2))
carry_in = (size * 2)
ancilla = (size * 2) + 1
carry_out = list(range(ancilla + 1, ancilla + size + 1))
grover_ancilla = carry_out[size-1] + 1


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
    This function activate every action 
    xor -> rotation -> add -> rotation -> xor
"""
def quantum_hash_oracle(qc):
    
    step_one_xor(qc)
    #print("xor")    
    
    
    step_two_rotate(qc)
    #print("rotation")
    
    
    adder(qc, state, value, carry_in, carry_out, ancilla, size)
    #print("adder")
    
    
    step_two_rotate(qc)
    #print("rotate")
    
    
    step_one_xor(qc)
    #print("xor")
    qc.barrier()
    



"""
this function act as the reverse of the funtion: quantum_hash_oracle

"""
def quantum_hash_oracle_uncompute(qc):
    step_one_xor_uncompute(qc)
    #print("uncompute xor")
    
    step_two_rotate_uncompute(qc)
    #print("uncompute shift")
    
    adder_reverse(qc, state, value, carry_in, carry_out, ancilla, size)
    #print("uncompute adder")

    step_two_rotate_uncompute(qc)
    #print("uncompute shift")
    
    step_one_xor_uncompute(qc)
    #print("uncompute xor")
    
    
    
#this function activate xor
def step_one_xor(qc):
    for i in range(size):
        qc.cx(value[i], state[i])
    
    
#this function activate the opposite (revese xor)
def step_one_xor_uncompute(qc):
    for i in range(size - 1, -1, -1):
        qc.cx(value[i], state[i])


#this function activate rotation
def step_two_rotate(qc):
    
    # --- מחזור 1: q6 → q8 → q10 ---
    qc.swap(state[0], state[4])
    qc.swap(state[0], state[2])
    
    # --- מחזור 2: q7 → q9 → q11 ---
    qc.swap(state[1], state[5])
    qc.swap(state[1], state[3])
    
    

#this function activate reversed rotation
def step_two_rotate_uncompute(qc):
    qc.swap(state[1], state[3])
    qc.swap(state[1], state[5])
    qc.swap(state[0], state[2])
    qc.swap(state[0], state[4])

    
"""
Explanation: 
    this function flip the grover ancilla and actually decide how much 0 lead the output
"""



def flip_oracle(qc):
    
    qc.x(state[0])
    qc.x(state[1])
    qc.x(state[2])
    qc.x(state[3])
    
    qc.mcx([state[0],state[1], state[2], state[3]], grover_ancilla)
    qc.z(grover_ancilla)
    qc.mcx([state[0],state[1], state[2], state[3]], grover_ancilla)

    qc.x(state[3])
    qc.x(state[2])
    qc.x(state[1])
    qc.x(state[0])
    
    """
    5 qubit starting with 0
    
    qc.x(state[0])
    qc.x(state[1])
    qc.x(state[2])
    qc.x(state[3])
    qc.x(state[4])
    
    
    qc.mcx([state[0],state[1], state[2], state[3], state[4]], grover_ancilla)
    qc.z(grover_ancilla)
    qc.mcx([state[0],state[1], state[2], state[3], state[4]], grover_ancilla)

    qc.x(state[4])
    qc.x(state[3])
    qc.x(state[2])
    qc.x(state[1])
    qc.x(state[0])
    """
    
    qc.barrier()
    
    


            
"""
this function activate the diffuzer 
"""        
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
    

    qc.barrier()


"""
Explanatiin: 
    print every measure we did and display it

"""
def print_measurements(qc, value):
    
    list_to_measure = value
                       
    #qc.measure(list_to_measure, list(range(size)))
    qc.measure(list(range(size*2)), list(range(size*2)))
    
    
    
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
    sorted_flipped_counts = dict(sorted(flipped_counts.items(), key=lambda item: item[1], reverse=True))
    
    
    for k, v in sorted_flipped_counts.items():
        print(f"value: {k[:size]}: {v}")
    
    
    plot_histogram(counts)
    qc.draw('mpl')
    
    #print(flipped_counts)

    

def encoding(qc, input_bits):
    
    """
    for i in range(value[0], (value[size-1] + 1)):
        if input_bits[i] == '1':
            qc.x(value[i])           
    
    """
    
    for j in range(state[0], (state[size-1] + 1)):
        if input_bits[j] == '1':
            qc.x(state[j - size])
    
    
    
    for i in range(value[0], (value[size-1] + 1)):
        qc.h(value[i])
      
    
    qc.barrier()
    
    

def main():
    
    
    qc = QuantumCircuit(grover_ancilla + 1, size*2)

    
    #value_str = "101101"
    value_str = "000000"

    state_str = "110011"
    encoding(qc, value_str + state_str )
    
    quantum_hash_oracle(qc)
    flip_oracle(qc)
    quantum_hash_oracle_uncompute(qc)
    diffuser(qc)
    
    print_measurements(qc, state)
    
    
main()