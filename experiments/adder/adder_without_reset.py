
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

    #reset ancilla
    qc.ccx(state, value, ancilla)

    #calculate carry
    # sum = state XOR value XOR pre_carry
    qc.cx(value, state)
    qc.cx(pre_carry, state)

    
    
    
def four_qubits_adder(qc, state, value, carry_in, carry_out, ancilla, size):
    
    for i in range(size - 1, -1, -1):
        
        if(i == size - 1):
            add_one_bit_full(qc, state[i], value[i], carry_in, carry_out[i], ancilla)
        else:
            add_one_bit_full(qc, state[i], value[i], carry_out[i+1], carry_out[i], ancilla)


def build_circuit(qc, state, value, carry_in, size):
    """
    #here i need to build the qubits as i want for example 1101 + 0101
    
    #state: 0101
    #value: 1100
    #Expected result: 10001
    
    qc.x(state[1])
    qc.x(state[3])
    
    qc.x(value[0])
    qc.x(value[1])
    
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    
    #example of 2 inputs as h
    #state: H000
    #value: H000
    #Expected result: 00000 / 01000 / 10000

    qc.h(state[0])
    qc.h(value[0])
    
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """
    
    #example of value as H
    #state: 010100
    #value: 1H00H1
    #Expected result: 01101 / 01110 / 10001 / 10010
    
    qc.x(state[1])
    qc.x(state[3])
    
    qc.x(value[0])
    qc.h(value[1])
    qc.h(value[4])
    qc.x(value[5])
    
        
    
def add_with_carry():
    
    size = 6
    value = list(range(size))
    state = list(range(size, size * 2))
    carry_in = (size * 2)
    ancilla = (size * 2) + 1
    carry_out = list(range(ancilla + 1, ancilla + size + 1))
    
    #print(f"""              value: {value}
    #          state: {state}
    #          carry_in: {carry_in}
    #          ancilla: {ancilla}
    #          carry_out: {carry_out}
    #         ancila + size + 1: {ancilla + size + 1}""")
              
              
    qc = QuantumCircuit(ancilla + size + 1, size + 1)
        
    
    build_circuit(qc, state, value, carry_in, size)
    four_qubits_adder(qc, state, value, carry_in, carry_out, ancilla, size)
    
    
    list_to_measure = [carry_out[0]]
    list_to_measure.extend(state)
                       
    #print(f"list to measure: {list_to_measure}, list_size: {list(range(size + 1))},")                   
    qc.measure(list_to_measure,list(range(size + 1)))

    
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
    #qc.draw('mpl')

add_with_carry()





