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
    
    
    



    
    
    
    
def add_with_carry():
    
    qc = QuantumCircuit(5, 2)

    state = 0
    value = 1
    pre_carry = 2
    carry_out = 3
    ancilla = 4
    #         value  +  state  + ancilla
    #example:   0    +    1    +    1
    qc.x(state)
    qc.x(value)
    qc.x(pre_carry)
    
    """
     3            1         0                  4            2
    pre carry    value     state      ->      state        carry out
      0           0         0                 0             0 
      0           0         1                 1             0
      0           1         0                 1             0
      0           1         1                 0             1
      1           0         0                 1             0 
      1           0         1                 0             1
      1           1         0                 0             1
      1           1         1                 1             1
    """
        
    add_one_bit_full(qc, state, value, pre_carry, carry_out, ancilla)

    
   
    print("check")
    qc.measure([3,0],[0,1])

    
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

